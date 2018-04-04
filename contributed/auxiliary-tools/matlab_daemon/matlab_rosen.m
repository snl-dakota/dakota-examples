function f = matlab_rosen(X)
%% rosenbrock implemented in Matlab
x1 = X.x1;
x2 = X.x2;
f = 100 .* (x2-x1.^2).^2 + (1-x1).^2;
