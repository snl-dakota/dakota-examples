#-------------------------------------------------------------------------------
# Dakota Graphical User Interface (Dakota GUI)
# Copyright 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
#   
# This software is distributed under the Eclipse Public License.  For more
# information see the files copyright.txt and license.txt included with the software.
#-------------------------------------------------------------------------------

###################################################################################################
#
#                            Dakota GUI:  Generated Driver Mapping Script
#
#   The following Python script allows you to perform arbitrary mappings between a Dakota study
#   and an external computational model.  The process of mapping input is based on character
#   replacements in an example input file (see the ppp module).  The process of mapping output
#   is based on simplified regular expression detection that scans your model's generated output
#   for quantities of interest (see the qoi module).
#
#   The specific mappings are hard-coded at the time of script generation (see the "Global script
#   variables" section in this script).
#
#   For questions related to this script, contact Elliott Ridgway.
#
###################################################################################################


#############
#  Imports  #
#############

# Common imports
import collections
import ntpath
import os
import shlex
import sys
import subprocess
import traceback
import uuid

# Dakota imports
from dakota.interfacing import interfacing as di

import qoi


#############################
#  Global script variables  #
#############################

mdl_out_option_stdout = "stdout"
mdl_out_option_output_file = "output_file"
mdl_out_file_default = "dak_py_driver.out"

# Below are hard-coded values that were inserted when this script was generated
mdl_in_path = "cantilever.template"
mdl_out_option = mdl_out_option_stdout
qois = [
    qoi.QoiAnchor("mass", 1, qoi.FIELDS, 2, qoi.LINES, qoi.AFTER, "MASS"),
    qoi.QoiAnchor("stress", 1, qoi.FIELDS, 2, qoi.LINES, qoi.AFTER, "STRESS"),
    qoi.QoiAnchor("displacement", 1, qoi.FIELDS, 2, qoi.LINES, qoi.AFTER, "DISPLACEMENT"),
]

cmd_line = "python cantilever ${input_file}"
cmd_in_repl = "${input_file}"
cmd_out_repl = ""
cmd_echo = True
cmd_prepend_eval_id = True


###############
#  Functions  #
###############

# subFile(file)
#   Convenience function that generates a unique substitute file name.  Used for saving substituted model input as new files,
#   so we don't have to worry about overwriting our original template.  This function observes any path information
#   preceding the file name.
#
#   file - The original file path (may be absolute or relative).
#
#   return - The new file name.    
    
def subFile(file):
    try:
        filenameonly = ntpath.basename(file)
        dir_path = os.path.dirname(file)
        if not dir_path.endswith('/') and len(dir_path) > 0:
            dir_path = str(dir_path + '/')
                
        id = uuid.uuid1()
        newName = str(dir_path + str(id) + "_" + filenameonly)
        while os.path.isfile(newName):
            id = uuid.uuid1()
            newName = str(dir_path + str(id) + "_" + file)
        return newName
    except:
        raise Exception("Error generating sub file")


################
#  Main logic  #
################

# Initial setup - get the Dakota Parameters and Response objects, and name the new model input and output files.
params, results = di.read_parameters_file()

sub_in_file_path  = subFile(mdl_in_path);
sub_out_file_path = subFile(mdl_out_file_default);

try:
    # Pre-processing:  Substitute values from the Dakota parameter file to the model's input file.
    di.dprepro(template=mdl_in_path, parameters=params, output=sub_in_file_path)
    
    # Execution:  Run the simulation model as a separate process.
    if len(cmd_in_repl) > 0:
        cmd_line = cmd_line.replace(cmd_in_repl, sub_in_file_path)
    if len(cmd_out_repl) > 0 and mdl_out_option != mdl_out_option_stdout:
        cmd_line = cmd_line.replace(cmd_out_repl, sub_out_file_path)
    
    model_exec = subprocess.Popen(shlex.split(cmd_line), bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout_stream = ""
    for line in iter(model_exec.stdout.readline, ''):
        if cmd_echo:
            if cmd_prepend_eval_id:
                print("***", params.eval_id, "***   ", line, end=' ')
            else:
                print(line, end=' ')
        stdout_stream += line        
        sys.stdout.flush()
    model_exec.wait()
    errcode = model_exec.returncode    
    if errcode:
        raise Exception("Error was encountered")
    
    # Post-processing:  Find quantities of interest in the model's output, and write to the Dakota response file format.
    output_map = collections.OrderedDict()
    if mdl_out_option == mdl_out_option_stdout:
        for qoi in qois:
            output_map[qoi.name] = qoi.extract(stdout_stream)
    else:
        out_file_str = ""
        with open(sub_out_file_path, "r") as out_file:
            out_file_str = out_file.read()
        for qoi in qois:
            output_map[qoi.name] = qoi.extract(out_file_str)    
    
    for r, val in list(output_map.items()):
        results[r].function = val
    results.write(ignore_asv=True)
    
except:
    traceback.print_exc()
    exit(-1)

exit(0)
