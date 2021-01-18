MyDataset=ones(69,4);
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