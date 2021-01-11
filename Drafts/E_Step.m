function Belongs = E_Step(dist1,dist2)

Belongs=zeros(1,size(dist1));
for i = 1: size(dist1)
    p_cluster1 = dist1(i);
    p_cluster2 = dist2(i);
    
    if p_cluster1 > p_cluster2
        Belongs(i) = 1;
    else
        Belongs(i) = 2;
    end
end
end