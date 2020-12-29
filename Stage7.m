RuntimesRep=double(load('RuntimesRep.mat').a);
Runtimes=double(load('Runtimes.mat').a);
Probs=double(load('Probs.mat').a);
col=RuntimesRep(174:end);
loglogistic = fitdist(col(:),'LogLogistic');
gauss=fitdist(RuntimesRep(:),'Normal');
loglogistic=pdf('LogLogistic',Runtimes,loglogistic.mu,loglogistic.sigma);
gauss=pdf('Normal',Runtimes,gauss.mu,gauss.sigma);
for i=1:1000
E_step_dist1=[size(Runtimes)];
E_step_dist2=[size(Runtimes)];
for i=1:size(Runtimes)
    p1=loglogistic(i);
    p2=gauss(i);
    p=p1+p2;
    E_step_dist1(i)=p1/p;
    E_step_dist2(i)=p2/p2;
end

NormalParams = mle(RuntimesRep(1:3197));
LogLogisticParams = mle(RuntimesRep(3197:end),'distribution','LogLogistic');
loglogistic = pdf('LogLogistic',Runtimes(21:end),LogLogisticParams(1),LogLogisticParams(2));
gauss=pdf('Normal',Runtimes(1:21),NormalParams(1),NormalParams(2));

end


