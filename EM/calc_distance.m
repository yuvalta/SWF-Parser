function d = calc_distance(Param, Param_)
%{ 
This function calculates the distance between two sets of parameters. 
Input: 
    Param : old parameters
    Param_: new parameters
Output: 
    d: semi-Euclidean distance
%}

d = norm(Param.mu(1) - Param_.mu(1)) + norm(Param.mu(2) - Param_.mu(2));

% d= sqrt((Param.mu1(1,1) - Param_.mu1(1,1))^2 + (Param.mu1(1,2) - Param_.mu1(1,2))^2 + ...
%     (Param.mu2(1,1) - Param_.mu2(1,1))^2 + (Param.mu2(1,2) - Param_.mu2(1,2))^2);
end