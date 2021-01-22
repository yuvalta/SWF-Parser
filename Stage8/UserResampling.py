import math
import numpy as np

def ParseDistribution(row):
    row_split_list=row.split()
    retdict=dict()
    for i in range(len(row_split_list)):
        if i==0:
            continue
        retdict.setdefault(row_split_list[i].split(':')[0],row_split_list[i].split(':')[1])
    return retdict

def GetJobsAfterTime(time,Jobs):
    ReturnedJobs=[]
    for Job in Jobs:
        row=Jobs.split()
        if int(row[1]>=time):
            ReturnedJobs.append(row)
    return ReturnedJobs

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

# loop to remove duplicates
for key in UsersWeek:
    UsersWeek[key]=list(set(UsersWeek[key]))

# Create the initial workload by combining the activity of all the
# users, where each user starts from a random week during his or her logged activity
for key in UsersDict:
    np.random.seed(RandomSeed)
    Rand_Week1=np.random.choice(UsersWeek[UsersDict[key]])
    Rand_Week1*=604800
    RandomSeed+=1
    np.random.seed(RandomSeed)
    Rand_Week2=np.random.choice(UsersWeek[UsersDict[key]])
    Rand_Week2*=604800
    RandomSeed+=1
    np.random.seed(RandomSeed)
    Rand_Week3=np.random.choice(UsersWeek[UsersDict[key]])
    Rand_Week3*=604800
    RandomSeed+=1
    Jobs1=GetJobsAfterTime(Rand_Week1,UsersDict[key])
    Jobs2=GetJobsAfterTime(Rand_Week2,UsersDict[key])
    Jobs3=GetJobsAfterTime(Rand_Week3,UsersDict[key])
    trace1+=Jobs1
    trace2+=Jobs2
    trace3+=Jobs3
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# with open(cfg_file, "r") as cfg_file:
#     for row in cfg_file.readlines():
#         row_split_list = row.split()
        
#         if row_split_list[0]=="Residence":
#             # already handled this line
#             continue
#         if row_split_list[0]=="Activity":
#             # already handled this line
#             continue
#         if row_split_list[0]=="Random_Seed":
#             continue
        

