function D = generate_data()

RuntimesRep=double(load('RuntimesRep.mat').a);
Runtimes=double(load('Runtimes.mat').a);
Runtimes=Runtimes(:);
Probs=double(load('Probs.mat').a);
D = [Runtimes(1:21) ones(21,1);
Runtimes(22:end) 2*ones(size(Runtimes(22:end),1),1)];
end
