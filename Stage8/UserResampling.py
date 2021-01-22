import math

def ParseDistribution(row):
    row_split_list=row.split()
    retdict=dict()
    for i in range(len(row_split_list)):
        if i==0:
            continue
        retdict.setdefault(row_split_list[i].split(':')[0],row_split_list[i].split(':')[1])
    return retdict

trace1=[]
trace2=[]
trace3=[]
data=[]
cfg_file = "config_file.txt"
ResidenceTimes=dict()
NewUsersPerWeek=dict()
UsersDict=dict()
UsersWeek=dict()
# first we collect the residence times distribution and new users arrivals distribution and make users dict where each 
# element of the dictionary is made of  User# : [job1,job2,....,jobn]
with open(cfg_file, "r") as cfg_file:
    for row in cfg_file.readlines():
        row_split_list = row.split()
        if row_split_list[0]=="Residence":
            ResidenceTimes==ParseDistribution(row)
            continue
        if row_split_list[0]=="Activity":
            NewUsersPerWeek=ParseDistribution(row)
            continue
        if row_split_list[0]=="Random_Seed":
            RandomSeed=int(row_split_list[1])
            continue
        UserID= row_split_list[11]
        submittime=row_split_list[1]
        submittime=math.floor(int(submittime)/604800)
        if UserID in UsersDict:
            UsersDict[UserID].append(row)   
            UsersWeek[UserID].append(submittime)
        else:
            UsersDict.setdefault(UserID,[]).append(row)
            UsersWeek.setdefault(UserID,[]).append(submittime)

# now we start the initializing part of the User resampling method as described in the book page 425 of the pdf.
with open(cfg_file, "r") as cfg_file:
    for row in cfg_file.readlines():
        row_split_list = row.split()
        
        if row_split_list[0]=="Residence":
            # already handled this line
            continue
        if row_split_list[0]=="Activity":
            # already handled this line
            continue
        if row_split_list[0]=="Seed":
            continue
        
        trace1.append(row)            
        trace2.append(row)   
        trace3.append(row)
        data.append(row)            
        

