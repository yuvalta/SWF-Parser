MyDataset=ones(69,4);
RandomJobs=ones(69,4);
RandomIndices=zeros(69,2);

load('UsersDataframe.mat')
fn = fieldnames(Runtime);
for k=1:numel(fn)
    if( isnumeric(Runtime.(fn{k})) )
        MyDataset(k,1)=Runtime.(fn{k});
    end
end
fn = fieldnames(Interarrival_Time);
for k=1:numel(fn)
    if( isnumeric(Interarrival_Time.(fn{k})) )
        MyDataset(k,2)=Interarrival_Time.(fn{k});
    end
end

fn = fieldnames(Job_Size);
for k=1:numel(fn)
    if( isnumeric(Job_Size.(fn{k})) )
        MyDataset(k,3)=Job_Size.(fn{k});
    end
end
fn = fieldnames(Think_Time);
for k=1:numel(fn)
    if( isnumeric(Think_Time.(fn{k})) )
        MyDataset(k,4)=Think_Time.(fn{k});
    end
end
% ds = array2table(MyDataset);
% ds.Properties.VariableNames{1} = 'Interarrival_Time';
% ds.Properties.VariableNames{2} = 'Runtimes';
% ds.Properties.VariableNames{3} = 'Job_Size';
% ds.Properties.VariableNames{4} = 'Think_Time';
RuntimesData=load('Runtimes.mat');
InterarrivalstimesData=load('Interarrivals.mat');
JobSizesData=load('JobSizes.mat');
ThinktimesData=load('Thinktimes.mat');

Data=ones(18239,5);
fn = fieldnames(RuntimesData);
lastuserposition=0;

for k=1:numel(fn)
    RandomIndices(k,1)=ceil((numel(RuntimesData.(fn{k})))*rand);
    RandomIndices(k,2)=k;
end

for k=1:numel(fn)
    for i=1:numel(RuntimesData.(fn{k}))
        Data(i+lastuserposition,2)=RuntimesData.(fn{k})(i);
        Data(i+lastuserposition,1)=k;
    end
    RandomJobs(k,1)=RuntimesData.(fn{k})(RandomIndices(k,1));
    RandomIndices(k,1)=ceil((numel(RuntimesData.(fn{k})))*rand);
    RandomIndices(k,2)=k;
    lastuserposition=lastuserposition+i;
end

fn = fieldnames(InterarrivalstimesData);
lastuserposition=0;
for k=1:numel(fn)
    for i=1:numel(InterarrivalstimesData.(fn{k}))
        Data(i+lastuserposition,3)=InterarrivalstimesData.(fn{k})(i);
    end
        RandomJobs(k,2)=InterarrivalstimesData.(fn{k})(RandomIndices(k,1));
    lastuserposition=lastuserposition+i;
end

fn = fieldnames(JobSizesData);
lastuserposition=0;
for k=1:numel(fn)
    for i=1:numel(JobSizesData.(fn{k}))
        Data(i+lastuserposition,4)=JobSizesData.(fn{k})(i);
    end
            RandomJobs(k,3)=JobSizesData.(fn{k})(RandomIndices(k,1));

    lastuserposition=lastuserposition+i;
end

fn = fieldnames(ThinktimesData);
lastuserposition=0;
for k=1:numel(fn)
    for i=1:numel(ThinktimesData.(fn{k}))
        Data(i+lastuserposition,5)=ThinktimesData.(fn{k})(i);
    end
    RandomJobs(k,4)=ThinktimesData.(fn{k})(RandomIndices(k,1));
    lastuserposition=lastuserposition+i;
end



    
ds = array2table(Data);
ds.Properties.VariableNames{1}='User';
ds.Properties.VariableNames{2} = 'Runtimes';
ds.Properties.VariableNames{3} = 'Interarrival_Time';
ds.Properties.VariableNames{4} = 'Job_Size';
ds.Properties.VariableNames{5} = 'Think_Time';


X=RandomJobs;
%X=[ds.Runtimes ds.Interarrival_Time ds.Job_Size ds.Think_Time];

idx=knnsearch(X,Data(:,2:5),'K',7);
for i=1:69
for j=1:7
    idx(i,j)=Data(idx(i,j),1);
end
end

Users=zeros(69,2);
for i=1:69
    Users(i,2)=i;
end

for k=1:numel(idx(:,1))
    for i=1:7
        Users(idx(k,i),1)=Users(idx(k,i))+1;
    end
end

Users=sortrows(Users);
fileID = fopen('TopUsers - 3.txt','w');
for i=1:7
    fprintf(fileID,'%d \n',Users(69-(i-1),2));

end
fclose(fileID);
