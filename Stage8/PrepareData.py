import pickle
import scipy.io
import math
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
#import numpy as np
SWF_log = "NASA-iPSC-1993-3.1-cln.SWF"
UsersDict=dict()

def Interarrivals(User):
    Prev_submit=0
    n=0
    Interarrivals_data=[]
    Interarrivals_counter=dict()
    Interarrivals_pdf=dict()
    for Job in User:
        Submit_time=int(Job.split()[1])
        interarrival_time=Submit_time-Prev_submit
        Interarrivals_data.append(interarrival_time)
        if interarrival_time in Interarrivals_counter:
            Interarrivals_counter[interarrival_time]+=1
        else:
            Interarrivals_counter.setdefault(interarrival_time,0)
        n+=1
        Prev_submit=Submit_time
    for time in Interarrivals_counter:
        Interarrivals_pdf.setdefault(time,Interarrivals_counter[time]/n)
    return Interarrivals_data,Interarrivals_pdf
    
def GenerateData(User,index):
    Runtime_data=[]
    for Job in User:
        Runtime=int(Job.split()[index])
        Runtime_data.append(Runtime)
    return Runtime_data
   
def GenerateThinkTimes(User):
    Prev_endtime=0
    submit_time=0
    thinktimes=[]
    for Job in User:
        submit_time=int(Job.split()[1])
        endtime=int(submit_time)+int(Job.split()[3])
        thinktimes.append(submit_time-Prev_endtime)
        Prev_endtime=endtime
    thinktimes[0]=0
    return thinktimes
        


# NewUserArrival=list()
# i=0
# active=0
# while(i<66242):
#   NewUserArrival.append(0)
#   i+=1

with open(SWF_log, "r") as swf_file:
    for row in swf_file.readlines():
        row_split_list = row.split()
        if row_split_list[0]==";":
            continue
        UserID= row_split_list[11]
        if UserID in UsersDict:
            UsersDict[UserID].append(row)            
        else:
            UsersDict.setdefault(UserID,[]).append(row)
            #SubmitInMinutes=math.ceil((int(row_split_list[1])/120))
            #while(SubmitInMinutes<len(NewUserArrival)):
            #    NewUserArrival[SubmitInMinutes]+=1
            #    SubmitInMinutes+=1  
#NewUserArrivalStrings=list()
#for a in NewUserArrival:
#    NewUserArrivalStrings.append(str(a))                
InterarrivalsDict=dict()
RuntimesDict=dict()
JobSizesDict=dict()
ThinkTimesDict=dict()
for User in UsersDict.values():
    InterarrivalData,PDF=Interarrivals(User)
    RuntimesData=GenerateData(User,3)
    JobSizesData=GenerateData(User,4)
    ThinkTimesData=GenerateThinkTimes(User)
    InterarrivalsDict.setdefault("User"+User[0].split()[11],InterarrivalData)
    RuntimesDict.setdefault("User"+User[0].split()[11],RuntimesData)
    JobSizesDict.setdefault("User"+User[0].split()[11],JobSizesData)
    ThinkTimesDict.setdefault("User"+User[0].split()[11],ThinkTimesData)
Users=dict()

for key in RuntimesDict.keys():
    avg=[]
    sum_=0
    sum_=sum(RuntimesDict[key])
    avg.append(sum_/len(RuntimesDict[key]))
    sum_=sum(InterarrivalsDict[key])
    avg.append(sum_/len(InterarrivalsDict[key]))
    sum_=sum(JobSizesDict[key])
    avg.append(sum_/len(JobSizesDict[key]))
    sum_=sum(ThinkTimesDict[key])
    avg.append(sum_/len(ThinkTimesDict[key]))
    Users.setdefault(key,avg)
    
#Created a Dataframe - each column is a feature vector
    

        
df=pd.DataFrame(Users)
df_=df.T
df_.columns =['Runtime','Interarrival_Time','Job_Size','Think_Time']
scipy.io.savemat('UsersDataframe.mat',df)
#scipy.io.savemat('Interarrivals.mat',InterarrivalsDict)
#scipy.io.savemat('Runtimes.mat',RuntimesDict)
#scipy.io.savemat('JobSizes.mat',JobSizesDict)
#scipy.io.savemat('ThinkTimes.mat',ThinkTimesDict)
#scipy.io.savemat('NewUserArrival.mat',NewUserArrivalStrings)

