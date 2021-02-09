import math
import numpy as np

def mergeSort(arr):
    if len(arr) > 1:
         # Finding the mid of the array
        mid = len(arr)//2
        # Dividing the array elements
        L = arr[:mid]
 
        # into 2 halves
        R = arr[mid:]
 
        # Sorting the first half
        mergeSort(L)
 
        # Sorting the second half
        mergeSort(R)
 
        i = j = k = 0
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if int(L[i].split()[1]) < int(R[j].split()[1]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            
def ExportTraces(trace,output_file):
    output_=open("..\\Stage9\\TEST\\"+output_file,'w')
    for job in trace:
        output_.write(job+'\n')
    output_.close()
        
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
            ReturnedJobs.append(Job)
    return ReturnedJobs

def GetJobsAfterTime(time,Jobs,ID):
    ReturnedJobs=[]
    for Job in Jobs:
        row=Job.split()
        if int(row[1])>=time:
            row[11]=str(ID)
            r=""
            for v in row:
                r+=(v+"     ")
            ReturnedJobs.append(r)
    return ReturnedJobs

def GetLongTermUsers(row):
    row_split_list=row.split()
    retlist=[]
    for i in range(len(row_split_list)):
        if i==0:
            continue
        retlist.append(int(row_split_list[i].replace('User','')))
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

def AdjustWaitTimes2(Trace):
  AvailableProcs=dict()
  i=0
  while i<=15000000:
      AvailableProcs.setdefault(i,128)
  i=1
  Trace1=[]
  row=Trace[0].split()
  row[2]='0'
  end_time=int(row[1])+int(row[3])
  submit_time=int(row[1])
  numofprocs=int(row[4])
  while submit_time <= end_time:
      AvailableProcs[submit_time]+=numofprocs
      submit_time+=1
  r=''
  for v in row:
      r+=(v+"   ")
  Trace1.append(r)    
  while i < len(Trace):
      row_split=Trace[i].split()
      run_time=int(row_split[3])
      submit_time=int(row_split[1])
      numofprocs=int(row_split[4])
      waittime=0
      while True:
         if (AvailableProcs[submit_time+waittime]-numofprocs) >= 0:
             break
         else:
             waittime+=1
      starttime=submit_time+waittime
      while starttime<=(starttime+run_time):
          if starttime < len(AvailableProcs):
              AvailableProcs[starttime]+=numofprocs
          starttime+=1
      row_split[2]=str(waittime)
      r=''
      for v in row_split:
          r+=(v+"   ")
      Trace1.append(r)   
      i+=1
  return Trace1

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
     row_split1=Trace1[i-1].split()
     row_split2=Trace[i].split()
     WaitTime=int(row_split1[1])+int(row_split1[2])+int(row_split1[3])-int(row_split2[1])
     if WaitTime>=0:
         row_split2[2]=str(WaitTime)
     else:
         row_split2[2]='0'
     r=""    
     for v in row_split2:
        r+=(v+"   ")
     Trace1.append(r)   
     i+=1    
  return Trace1
 
def Sync(week,Jobs,UsersWeeks,CurrentUsers,ID):
    NewJobs=[]
    for num in UsersWeeks:
        CurrentUsers[num-week]+=1
    comp=UsersWeeks[0] - week
    for j in Jobs:
        row=j.split()
        row[1]=str(int(row[1])-(comp*604800))
        row[11]=str(ID%69)
        r=""
        for v in row:
           r+=(v+"     ")
        NewJobs.append(r)
    return NewJobs

def ThinkTimes(Log):
    NewLog=[]
    Users=dict()
    for job in Log:
        job_splitted=job.split()
        UserID=job_splitted[11]
        if UserID in Users:
            Users[UserID].append(job) 
        else:
            Users.setdefault(UserID,[]).append(job)
    for key in Users:
        end_time=0
        for i in range(len(Users[key])):
            jobsplitted=Users[key][i].split()
            sub_time=int(jobsplitted[1])
            think=sub_time-end_time
            end_time=sub_time+int(jobsplitted[1])
            jobsplitted[17]=str(think)
            r=""    
            for v in jobsplitted:
                r+=(v+"   ")
            NewLog.append(r)  
    return NewLog

ID1=1
ID2=1
ID3=1
trace1=[]
trace2=[]
trace3=[]
CurrentUsers1=[4,4,3,3,3,2,2,3,3,2,3,4,2,2]
CurrentUsers2=[4,4,3,3,3,2,2,3,3,2,3,4,2,2]
CurrentUsers3=[4,4,3,3,3,2,2,3,3,2,3,4,2,2]
data=[]
cfg_file = "Input2//config_file3.txt"
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
    splittednum=math.modf((NewUsersPerWeek[key]*load))
    NewUsersPerWeek[key]=int(splittednum[1])
    probability=splittednum[0]
    if np.random.random()<=probability:
        NewUsersPerWeek[key]+=1
    
# loop to remove duplicates
for key in UsersWeek:
    UsersWeek[key]=list(set(UsersWeek[key]))
    UsersWeek[key].sort()
    


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
    Jobs1=GetJobsAfterTime(Rand_Week1,UsersDict[key],ID1)
    ID1+=1
    Jobs2=GetJobsAfterTime(Rand_Week2,UsersDict[key],ID2)
    ID2+=1
    Jobs3=GetJobsAfterTime(Rand_Week3,UsersDict[key],ID3)
    ID3+=1
    trace1+=Jobs1
    trace2+=Jobs2
    trace3+=Jobs3
    
i=0
# select at random a certain number of new temporary users to add
# in each week of the generated workload. Randomize the actual number of new users,
# with the average being the number of new users per week in the original workload log.
for key in NewUsersPerWeek:
    #tempDict=GenerateUsers(UsersNumbers, UsersDict, UsersWeek)
    index=int(key.replace('Week',''))
    NumOfUsers1=(NewUsersPerWeek[key])-CurrentUsers1[i]
    NumOfUsers2=(NewUsersPerWeek[key])-CurrentUsers2[i]
    NumOfUsers3=(NewUsersPerWeek[key])-CurrentUsers3[i]
    if NumOfUsers1>0:
        for j in range(int(NumOfUsers1)):
            User1=np.random.choice(list(UsersDict.keys()))
            jobs1=Sync(i,UsersDict[str(User1)],UsersWeek[str(User1)],CurrentUsers1,ID1)
            trace1+=jobs1
            ID1+=1
    if NumOfUsers2>0:
        for j in range(int(NumOfUsers2)):
            User2=np.random.choice(list(UsersDict.keys()))
            jobs2=Sync(i,UsersDict[str(User2)],UsersWeek[str(User2)],CurrentUsers2,ID2)
            trace2+=jobs2
            ID2+=1
    if NumOfUsers3>0:
        for j in range(int(NumOfUsers3)):
            User3=np.random.choice(list(UsersDict.keys()))
            jobs3=Sync(i,UsersDict[str(User3)],UsersWeek[str(User3)],CurrentUsers3,ID3)
            trace3+=jobs3
            ID3+=1
    i+=1
trace1=ThinkTimes(trace1)
trace2=ThinkTimes(trace2)
trace3=ThinkTimes(trace3)
mergeSort(trace1)
mergeSort(trace2)
mergeSort(trace3)
trace1=AddWaitTimes(trace1)
trace2=AddWaitTimes(trace2)
trace3=AddWaitTimes(trace3)
ExportTraces(trace1, "outputload80_1.txt") #the file will be routed to Stage9/Output
ExportTraces(trace2, "outputload80_2.txt")
ExportTraces(trace3, "outputload80_3.txt")


