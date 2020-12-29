function Param = maximization(Data, Param)
%{ 
This function calculates the second step of the EM algorithm, Maximization.
It updates the parameters of the Normal distributions according to the new 
labled dataset.
Input: 
    Data : nx3 (number of data points , [x, y, label])
    Param: (mu, sigma, lambda)
Output: 
    Param: updated parameters 
%}

points_in_cluster1 = Data(Data(:,2) == 1,:);
points_in_cluster2 = Data(Data(:,2) == 2,:);

percent_cluster1 = size(points_in_cluster1,1) / size(Data,1);
percent_cluster2 = 1 - percent_cluster1;

% calculate the weights
Param.lambda = [percent_cluster1, percent_cluster2];

NormalParams = mle(points_in_cluster1(:,1));
LogLogisticParams = mle(points_in_cluster2(:,1),'distribution','LogLogistic');

Param.mu=[NormalParams(1),LogLogisticParams(1)];
Param.sigma=[NormalParams(2),LogLogisticParams(2)];

end