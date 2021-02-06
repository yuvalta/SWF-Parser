function Data = expectation(Data, Param)
%{ 
This function calculates the first step of the EM algorithm, Expectation.
It calculates the probability of each specific data point belong to each
cluster or class
Input: 
    Data : nx3 (number of data points , [x, y, label])
    Param: (mu, sigma, lambda)
Output: 
    Data: the dataset with updated labels
%}
loglogistic=pdf('LogLogistic',Data(:,1),Param.mu(2),Param.sigma(2));
gauss=normpdf(Data(:,1),Param.mu(1),Param.sigma(1));
for i = 1: size(Data,1)

    p_cluster1 = gauss(i)*Param.lambda(1);
    p_cluster2 = loglogistic(i)*Param.lambda(2);
    
    if p_cluster1 > p_cluster2
        Data(i, 2) = 1;
    else
        Data(i, 2) = 2;
    end
end
end