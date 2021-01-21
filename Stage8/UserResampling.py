


trace1=[]
trace2=[]
trace3=[]
cfg_file = "config_file.txt"
with open(cfg_file, "r") as cfg_file:
    for row in cfg_file.readlines():
        row_split_list = row.split()
        if row_split_list[0]=="Residence":
            continue
        if row_split_list[0]=="Activity":
            continue
        trace1.append(row)            
        trace2.append(row)   
        trace3.append(row)            
        

