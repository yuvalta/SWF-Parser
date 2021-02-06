clc, clear, close all

% number of points in each cluster
num_points = 100; 

% generate random data using two 2D Normal distributions with 100 data points 
Data = generate_data();



% make some initial guess
Param = make_initial_guess();





% run EM to find the parameters 
[Data_f, Param_f] = EM(Data, Param);

