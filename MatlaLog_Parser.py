from shutil import copyfile, copy
import os
from datetime import datetime, date
from RowClass import RowClass
import matplotlib.pyplot as plt

original_log_path = "log_files/Matlab_Log.txt"
cleaned_log_path="log_files/Cleaned_Matlab_Log.txt"
SWF_log = "log_files/SWF_Matlab_Log.txt"
UserDict=dict()
with open (cleaned_log_path) as file:  # Generating a dictionary containing the user name (e.g user1@computer1) as a key and a list of 
    for line in file:                  # all the jobs he is involved in
        line_split=line.split()
        User=line_split[4]
        if User in UserDict.keys():
            UserDict[User].append(line)
        else:
            UserDict.setdefault(User,[]).append(line)
log_file = open(cleaned_log_path, "r")
log_file.seek(0)

if os.path.isfile(SWF_log):  # delete SWF file if already exists
    os.remove(SWF_log)

with open (original_log_path) as file:
    first_line = file.readline()
    started_time=datetime.strptime((first_line.split())[0], "%H:%M:%S").time()         ##calculate the start time of the system
    started_time=(started_time.hour)*3600+(started_time.minute)*60+(started_time.second) ## which is 10:55:26 converted to seconds=39326
    
job_number = 1
PrecedingJobNum=0
with open(SWF_log, "w") as swf_file:
    for row in log_file.readlines():
        row_split_list = row.split()
        if "IN" in row_split_list:     # we only read lines with "OUT"
            continue
        arrival_time=datetime.strptime(row_split_list[0], "%H:%M:%S").time()                # calculate the arrival time of the job
        arrival_time=(arrival_time.hour)*3600+(arrival_time.minute)*60+(arrival_time.second)# and converting it to seconds
        submit_time=arrival_time-started_time  # first column in the SWF fields sumbit time
        wait_time=0  ## not sure about it
        currentUser=UserDict[row_split_list[4]] # pull the list that contains all the jobs done by this user
        for job in currentUser:
            if "IN" + row_split_list[3] in job:                                # search for the "IN" request of the same job we have now
                endTime=datetime.strptime((job.split())[0], "%H:%M:%S").time() # in order to calculate the runtime which is the substraction
                endTime=(endTime.hour)*3600+(endTime.minute)*60+(endTime.second) # of the "IN" time and "OUT" time ;not sure about it
        RunTime=endTime-arrival_time
        NumOfProc=-1 #couldn't find information about the number of processors requested
        AverageCPUtime=RunTime #not sure
        AverageMem=-1 # no information found
        RequestedProc=1 
        RequestedRunTime=RunTime 
        RequestedMem=-1
        Status=1
        UserID=list(UserDict.keys()).index(row_split_list[4]) #get the index of the user from the keys of the users dictionary
        GroupID=-1
        #Executable=list(ApplicationsDict.keys()).index(row_split_list[3]) #TODO:create a dictionary for each request type (e.g "MATLAB"...) 
        Queue=-1
        Partition=-1
        ThinkTime=-1
        #TODO write to the SWF file
        
        job_number+=1
        PrecedingJobNum+=1
#Lines like 156-182 in the original file shouldn't be removed due to description of memory used, runtime in ms...
#information may be lost (not sure about this thing) should discuss it with the group
        