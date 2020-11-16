from datetime import datetime
import matplotlib.pyplot as plt
ConsumptionsDict=dict()
UserDict=dict()
X=list()
NumberOfRequests=list()
cleaned_log_path="log_files/Cleaned_Matlab_Log.txt"
original_log_path = "log_files/Matlab_Log.txt"
with open (original_log_path) as file:
    first_line = file.readline()
    started_time=datetime.strptime((first_line.split())[0], "%H:%M:%S").time()         ##calculate the start time of the system
    started_time=(started_time.hour)*3600+(started_time.minute)*60+(started_time.second) ## which is 10:55:26 converted to seconds=39326
    
with open (cleaned_log_path) as file:  # Generating a dictionary containing the user name (e.g user1@computer1) as a key and a list of 
    for line in file:                  # all the jobs he is involved in
        line_split=line.split()
        User=line_split[4]
        if User in UserDict.keys():
            UserDict[User].append(line)
        else:
            UserDict.setdefault(User,[]).append(line)

with open(cleaned_log_path) as file:
    for line in file:
        line_split=line.split()
        Request=line_split[3]
        if "IN:" in line_split:     # we only read lines with "OUT"
            continue
        currentUser=UserDict[line_split[4]] # pull the list that contains all the jobs done by this user
        arrival_time=datetime.strptime(line_split[0], "%H:%M:%S").time()                # calculate the arrival time of the job
        arrival_time=(arrival_time.hour)*3600+(arrival_time.minute)*60+(arrival_time.second) - started_time# and converting it to seconds
        for job in currentUser:
            if  "IN: "+ line_split[3] in job:                               
                endTime=datetime.strptime((job.split())[0], "%H:%M:%S").time() 
                endTime=(endTime.hour)*3600+(endTime.minute)*60+(endTime.second) - started_time
        if Request in ConsumptionsDict.keys():
            ConsumptionsDict[Request].append([arrival_time,endTime])
        else:
            ConsumptionsDict.setdefault(Request,[]).append([arrival_time,endTime])
i=0
while i<43752:
    NumberOfRequests.append(0)
    X.append(i)
    i+=1
for Request in ConsumptionsDict.values():
    for Interval in Request:
       i=Interval[0]
       while i<Interval[1]:
           NumberOfRequests[i]+=1
           i+=1
plt.title("Resources Consumption")
plt.plot(X,NumberOfRequests)
plt.xlim(0,45000)
plt.ylim(0,100)   
plt.xlabel("Seconds since the system started")
plt.ylabel("Number of allocated resources")
plt.show()             
#x axis should be limited to 44000