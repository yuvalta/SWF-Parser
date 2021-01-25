import math
import numpy as np

def ParseDistribution(row):
    row_split_list=row.split()
    retdict=dict()
    for i in range(len(row_split_list)):
        if i==0:
            continue
        retdict.setdefault(row_split_list[i].split(':')[0],int(row_split_list[i].split(':')[1]))
    return retdict

def GetJobsInWeek(week,Jobs):
    ReturnedJobs=[]
    for Job in Jobs:
        row=Job.split()
        WeekSubmit=math.floor(int(row[1])/604800)
        if week==WeekSubmit:
            ReturnedJobs.append(row)
    return ReturnedJobs

def GetJobsAfterTime(time,Jobs):
    ReturnedJobs=[]
    for Job in Jobs:
        row=Job.split()
        if int(row[1])>=time:
            ReturnedJobs.append(row)
    return ReturnedJobs

def GetLongTermUsers(row):
    row_split_list=row.split()
    retlist=[]
    for i in range(len(row_split_list)):
        if i==0:
            continue
        retlist.append(int(row_split_list[i][-1]))
    return retlist

def SortTrace(trace):
    trace1=[]
    i=len(trace)-1
    while i>=0:
     min=int(trace[0].split()[1])   
     row2=trace[0]
     for row in trace:
        row_split=row.split()
        if int(row_split[1])<min:
            min=int(row_split[1])
            row2=row
     trace1.append(row2)
     trace.remove(row2)
     i-=1
    return trace1
    
def GenerateUsers(ShortTermUsers,UsersDict_,UsersWeek_):
    newdict=dict()
    for number in ShortTermUsers:
        Rand_Week=np.random.choice(UsersWeek_[str(number)])
        newdict.setdefault(str(number),GetJobsInWeek(Rand_Week, UsersDict_[str(number)]))
    return newdict
   
def AddWaitTimes(Trace):
  i=1
  Trace1=[]
  row=Trace[0].split()
  row[2]='0'
  r=''
  for v in row:
      r+=(v+"   ")
  Trace1.append(r)    
  while i<len(Trace):
     row_split1=Trace[i-1].split()
     row_split2=Trace[i].split()
     WaitTime=int(row_split1[1])+int(row_split1[3])-int(row_split2[1])
     if WaitTime>=0:
         row_split1[2]=str(WaitTime)
     else:
         row_split1[2]='0'
     r=""    
     for v in row_split1:
        r+=(v+"   ")
     Trace1.append(r)   
     i+=1    
  return Trace1
 
def Sync(week,Jobs):
    NewJobs=[]
    for j in Jobs:
        row=j.split()
        row[1]=str(int(row[1])%604800+week*604800)
        r=""
        for v in row:
           r+=(v+"     ")
        NewJobs.append(r)
    return NewJobs
 
trace1=[]
trace2=[]
trace3=[]
data=[]
cfg_file = "Input2//config_file1.txt"
ResidenceTimes=dict()
NewUsersPerWeek=dict()
UsersDict=dict()
UsersWeek=dict()
Long_Term_Pool=[]
UsersNumbers=[]
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
        if row_split_list[0]=="Load":
            load=int(row_split_list[1])
            continue
        if row_split_list[0]=="Long-Term":
            Long_Term_Pool=GetLongTermUsers(row)
            continue
        UserID= row_split_list[11]
        submittime=row_split_list[1]
        submittime=math.floor(int(submittime)/604800)
        if UserID in UsersDict:
            UsersDict[UserID].append(row)   
            UsersWeek[UserID].append(submittime)
        else:
            if int(UserID) not in Long_Term_Pool:
                UsersNumbers.append(int(UserID))
            UsersDict.setdefault(UserID,[]).append(row)
            UsersWeek.setdefault(UserID,[]).append((submittime))

# Multiply the number of new users per week with the given load to generate more load on the system
load/=100
for key in NewUsersPerWeek:
    NewUsersPerWeek[key]=round(NewUsersPerWeek[key]*load)
    
# loop to remove duplicates
for key in UsersWeek:
    UsersWeek[key]=list(set(UsersWeek[key]))

# Create the initial workload by combining the activity of all the
# users, where each user starts from a random week during his or her logged activity
for key in UsersDict:
    np.random.seed(RandomSeed)
    Rand_Week1=np.random.choice(UsersWeek[key])
    Rand_Week1*=604800
    Rand_Week2=np.random.choice(UsersWeek[key])
    Rand_Week2*=604800
    Rand_Week3=np.random.choice(UsersWeek[key])
    Rand_Week3*=604800
    RandomSeed+=1
    Jobs1=GetJobsAfterTime(Rand_Week1,UsersDict[key])
    Jobs2=GetJobsAfterTime(Rand_Week2,UsersDict[key])
    Jobs3=GetJobsAfterTime(Rand_Week3,UsersDict[key])
    trace1+=Jobs1
    trace2+=Jobs2
    trace3+=Jobs3
    
i=0
# select at random a certain number of new temporary users to add
# in each week of the generated workload. Randomize the actual number of new users,
# with the average being the number of new users per week in the original workload log.
for key in NewUsersPerWeek:
    tempDict=GenerateUsers(UsersNumbers, UsersDict, UsersWeek)
    NumOfUsers=np.random.normal(NewUsersPerWeek[key],2,1)
    for j in range(int(NumOfUsers)):
        User1=np.random.choice(tempDict.keys())
        User2=np.random.choice(tempDict.keys())
        User3=np.random.choice(tempDict.keys())
        jobs1=Sync(i,tempDict[User1])
        jobs2=Sync(i,tempDict[User2])
        jobs3=Sync(i,tempDict[User3])
        trace1+=jobs1
        trace2+=jobs2
        trace3+=jobs3
    i+=1
trace1=SortTrace(trace1)
trace2=SortTrace(trace2)
trace3=SortTrace(trace3)
trace1=AddWaitTimes(trace1)
trace2=AddWaitTimes(trace2)
trace3=AddWaitTimes(trace3)


