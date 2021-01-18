MyDataset=ones(69,4);
load('UsersDataframe.mat')
fn = fieldnames(Interarrival_Time);
for k=1:numel(fn)
    if( isnumeric(Interarrival_Time.(fn{k})) )
        MyDataset(k,1)=Interarrival_Time.(fn{k});
    end
end
fn = fieldnames(Runtime);
for k=1:numel(fn)
    if( isnumeric(Runtime.(fn{k})) )
        MyDataset(k,2)=Runtime.(fn{k});
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
ds = array2table(MyDataset);
ds.Properties.VariableNames{1} = 'Interarrival_Time';
ds.Properties.VariableNames{2} = 'Runtimes';
ds.Properties.VariableNames{3} = 'Job_Size';
ds.Properties.VariableNames{4} = 'Think_Time';
RuntimesData=load('Runtimes.mat');
InterarrivalstimesData=load('Interarrivals.mat');
JobSizesData=load('JobSizes.mat');
ThinktimesData=load('Thinktimes.mat');

Data=ones(18239,4);
fn = fieldnames(RuntimesData);
lastuserposition=0;
for k=1:numel(fn)
    for i=1:numel(RuntimesData.(fn{k}))
        Data(i+lastuserposition,1)=RuntimesData.(fn{k})(i);
    end
    lastuserposition=lastuserposition+i;
end

fn = fieldnames(InterarrivalstimesData);
lastuserposition=0;
for k=1:numel(fn)
    for i=1:numel(InterarrivalstimesData.(fn{k}))
        Data(i+lastuserposition,2)=InterarrivalstimesData.(fn{k})(i);
    end
    lastuserposition=lastuserposition+i;
end

fn = fieldnames(JobSizesData);
lastuserposition=0;
for k=1:numel(fn)
    for i=1:numel(JobSizesData.(fn{k}))
        Data(i+lastuserposition,3)=JobSizesData.(fn{k})(i);
    end
    lastuserposition=lastuserposition+i;
end

fn = fieldnames(ThinktimesData);
lastuserposition=0;
for k=1:numel(fn)
    for i=1:numel(ThinktimesData.(fn{k}))
        Data(i+lastuserposition,4)=ThinktimesData.(fn{k})(i);
    end
    lastuserposition=lastuserposition+i;
end

X=[ds.Runtimes ds.Interarrival_Time ds.Job_Size ds.Think_Time];
idx=knnsearch(X,Data,'K',7);
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
fileID = fopen('TopUsers.txt','w');
for i=1:7
    fprintf(fileID,'%d \n',Users(69-(i-1),2));

end
fclose(fileID);
