function dakota_daemon(function_handle,varargin)
% dakota_daemon - Matlab code to listen for Dakota jobs
%
% Usage:
% 
%     dakota_daemon(function_handle);
%     dakota_daemon(function_handle,...,'option',value)
%     
% Inputs:
%     
%     function_handle
%         Function hanle for the matlab function. See below for options for how
%         this code will call it. And see example for how to use it
%     
% Options: Specify as 'option',value pairs
% 
%     'mode'  [Default: 'struct']
%         Specify how dakota_daemon will call your function:
%             'struct' - 
%                 Will pass a matlab structre of each parameter specified in 
%                 Dakota. For example, parameter 'v' will be 'params.v'. 
%                 WARNING: Names must be valid matlab field names.
%             
%             'array'
%                 Will pass a vector of parameter values *in the order from
%                 Dakota*. See Dakota documentation for ordering
%             
%             'filename'
%                 Will pass the Dakota parameter filename to the function
%         
%         All functions must return the output (any number of outputs is fine)
% 
%     'eval_path' [Default '.']
%         Specify where the code should look for the queued runs
%     
%     'poll' [Default 0.25]
%         Minimum time before polling for new runs
%
%     'use_parfor' [Default 0]
%         Tell the code to run in parfor when it can
%     
% Notes:
% 
% * Can support any number of output variables. If an array is returned, the 
%   array is flattened and written as such. Useful for field quantities
% * Advanced output such as derivatives and hessians are not supported
%
% Last Updated: 2018-04-04

%% Parse
% defaults
mode = 'struct';
eval_path = '.';
poll = 0.25;
use_parfor = 0;

allowed = {'mode','eval_path','poll','use_parfor'};

for iv = 1:2:length(varargin)
    param_ = varargin{iv};
    % Optional check:
    if ~ismember(param_,allowed); 
        error(sprintf('Unrecognized Parameter: %s',param_));  % Or warning
    end
    eval(sprintf('%s = varargin{iv+1} ;',param_));  
end

%% Start working
savedir = fullfile(eval_path,'DAKOTA_MATLAB_TMP');

read_ids = {};

T0 = datetime('now');
while 1
    run_files = {};
    if exist(savedir) == 7 % folder
        files = dir(savedir);
        nfiles = length(files);
        
        for ifile = 1:nfiles
            file = files(ifile);
            if file.isdir
                continue
            end
            
            [~,id,ext] = fileparts(file.name);
            file.id = id;
            if ~strcmp(ext,'.in')
                continue
            end
            
            if ismember(id,read_ids)
                continue % already done
            end 
            
            run_files = [run_files;file]; 
        end
        
        if use_parfor
            for ifile = 1:length(run_files)
                file = run_files{ifile};
                run(function_handle,file,mode);
                read_ids = [read_ids;file.id];
                fprintf('ran id: %s\n',file.id);
            end        
        else
            for ifile = 1:length(run_files)
                file = run_files{ifile};
                run(function_handle,file,mode);
                read_ids = [read_ids;file.id];
                fprintf('ran id: %s\n',file.id);
            end
        end
        
    end
    
    if length(run_files)>0
        fprintf('\n  Polling every %0.2f sec. CTRL-C to break\n\n',poll)
    end
    
    % Figure out how much longer to wait    
    dt = seconds(datetime('now') - T0);
    pause(max(0,poll-dt));
    
    T0 = datetime('now');

end


function run(function_handle,file,mode)

fileID = fopen(fullfile(file.folder,file.name),'r');
filename = textscan(fileID,'%s',1); filename = filename{1};
N = textscan(fileID,'%f',1); N = N{1};

X = zeros(1,N);
params = struct();
for ii = 1:N
    line = textscan(fileID,'%s %f',1);
    params.(line{1}{1}) = line{2};
    X(ii) = line{2};
end

switch lower(mode)
case 'struct'
    varargout = feval(function_handle,params);
case {'x','array'}
    varargout = feval(function_handle,X);
case {'filename'}
    varargout = feval(function_handle,filename);
otherwise
    error('Uncrecognized mode')
end


if iscell(varargout)
    results = [];
    for iv = 1:length(varargout)
        res = varargout{iv};
        results = [results;res(:)];
    end
else
    results = varargout(:);
end
        
% write results
outfile = fullfile(file.folder,[file.id '.out']);
save(outfile,'results','-ascii','-double');


        




























 
