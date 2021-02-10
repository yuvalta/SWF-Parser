import numpy as np
import math
import matplotlib.pyplot as plt
from hurst import compute_Hc
from statsmodels.distributions.empirical_distribution import ECDF
outputload80_1="Output2\\outputload80_1.txt"
outputload80_2="Output2\\outputload80_2.txt"
outputload80_3="Output2\\outputload80_3.txt"
outputload100_1="Output2\\outputload100_1.txt"
outputload100_2="Output2\\outputload100_2.txt"
outputload100_3="Output2\\outputload100_3.txt"
outputload120_1="Output2\\outputload120_1.txt"
outputload120_2="Output2\\outputload120_2.txt"
outputload120_3="Output2\\outputload120_3.txt"
original_log="..\\Stage8\\NASA-iPSC-1993-3.1-cln.SWF"
Log_load80_1=[]
Log_load80_2=[]
Log_load80_3=[]
Log_load100_1=[]
Log_load100_2=[]
Log_load100_3=[]
Log_load120_1=[]
Log_load120_2=[]
Log_load120_3=[]
Original_Log=[]

def AdjustWaitTimes2(Trace):
  AvailableProcs=np.zeros(15000000)
  AvailableProcs=[i+128 for i in AvailableProcs]
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

def PlotSubmission(SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF,Days,Load,Log):
    fig,(ax1,ax2,ax3,ax4)=plt.subplots(1,4)
    ax1.set_title("Load "+str(Load)+", Log "+str(Log))
    ax1.set_xlabel(str(Days)+"days scale")
    ax1.set_ylabel("PDF")
    ax1.plot(SubmissionRatePDF.keys(),SubmissionRatePDF.values())
    ax2.set_xlabel(str(Days)+"days scale")
    ax2.set_ylabel("CDF")
    ax2.plot(SubmissionRateCDF.keys(),SubmissionRateCDF.values())
    ax3.set_xlabel(str(Days)+"days scale")
    ax3.set_ylabel("ECDF")
    ax3.plot(SubmissionRateECDF.x,SubmissionRateECDF.y)
    ax4.set_xlabel(str(Days)+" days scale")
    ax4.set_ylabel("Submissions")
    ax4.plot(SubmissionRate.keys(),SubmissionRate.values())

def AdjustThinkTimes(Log):
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

def Interarrivals(Log):
    Prev_submit=0
    n=0
    Interarrivals_data=[]
    Interarrivals_counter=dict()
    Interarrivals_pdf=dict()
    for Job in Log:
        Submit_time=int(Job.split()[1])
        interarrival_time=Submit_time-Prev_submit
        Interarrivals_data.append(interarrival_time)
        if interarrival_time in Interarrivals_counter:
            Interarrivals_counter[interarrival_time]+=1
        else:
            Interarrivals_counter.setdefault(interarrival_time,1)
        n+=1
        Prev_submit=Submit_time
    for time in Interarrivals_counter:
        Interarrivals_pdf.setdefault(time,Interarrivals_counter[time]/n)
    X=[]
    Y=[]
    for i in sorted (Interarrivals_pdf.keys()) : 
        X.append(i)
        Y.append(Interarrivals_pdf[i])
    i=1
    while i < len(Y):
        Y[i]=Y[i]+Y[i-1]
        i+=1
    return Interarrivals_data,X,Y

def Consumption(Log,boool):
    if boool:
        Last=int(Log[-1].split()[1])+ int(Log[-1].split()[3]) + 1
    else:
        Last=int(Log[-1].split()[1])+int(Log[-1].split()[2]) + int(Log[-1].split()[3]) + 1
    ConsumptionData=np.zeros(Last)
    for Job in Log:
        if boool:
            Time=int(Job.split()[1])+int(Job.split()[3])
            sub_time=int(Job.split()[1])
        else:
            Time=int(Job.split()[1])+int(Job.split()[2])+int(Job.split()[3])
            sub_time=int(Job.split()[1])+int(Job.split()[2])
        NumOfProcs=int(Job.split()[4])
        while sub_time < Time:
            if sub_time < Last:
                ConsumptionData[sub_time]+=NumOfProcs
            sub_time+=1
    ConsumptionData = [(i/128)*100 for i in ConsumptionData] 
    avg=0
    n=len(ConsumptionData)
    for num in ConsumptionData:
        avg+=(num/n)
    return ConsumptionData,avg

def Runtimes(Log):
    n=0
    Runtime_data=[]
    Runtimes_counter=dict()
    Runtimes_pdf=dict()
    for Job in Log:
        Runtime=int(Job.split()[3])
        Runtime_data.append(Runtime)
        if Runtime in Runtimes_counter:
            Runtimes_counter[Runtime]+=1
        else:
            Runtimes_counter.setdefault(Runtime,1)
        n+=1
    for key in Runtimes_counter:
        Runtimes_pdf.setdefault(key,Runtimes_counter[key]/len(Runtime_data))
    X=[]
    Y=[]
    for i in sorted (Runtimes_pdf.keys()) : 
        X.append(i)
        Y.append(Runtimes_pdf[i])
    i=1
    while i < len(Y):
        Y[i]=Y[i]+Y[i-1]
        i+=1
    return Runtime_data,X,Y

def UserDistribution(Log):
    UsersIDs=[]
    NewUserArrival=np.zeros(math.floor(int(Log[-1].split()[1])/86400)+1) # get the number of days in the log
    for Job in Log:
        UserID= Job.split()[11]
        week=math.floor((int(Job.split()[1])/86400))
        if UserID not in UsersIDs:
            UsersIDs.append(UserID)
            while(week<len(NewUserArrival)):
               NewUserArrival[week]+=1
               week+=1
    return NewUserArrival    
    
def ThinkTimes(Log):
    n=0
    Thinktime_data=[]
    Thinktimes_counter=dict()
    Thinktimes_pdf=dict()
    for Job in Log:
        Thinktime=int(Job.split()[17])
        Thinktime_data.append(Thinktime)
        if Thinktime in Thinktimes_counter:
            Thinktimes_counter[Thinktime]+=1
        else:
            Thinktimes_counter.setdefault(Thinktime,1)
        n+=1
    for time in Thinktimes_counter:
        Thinktimes_pdf.setdefault(time,Thinktimes_counter[time]/n)
    return Thinktime_data,Thinktimes_pdf

def CrossCorellation(X,Y,title,Xlabel,Ylabel):
    axes=plt.subplots()[1]
    CC=np.corrcoef(X, Y)[1,0]
    CC="{:.3f}".format(CC)
    axes.scatter(X, Y)
    axes.set_title(title)
    axes.set_xlabel(Xlabel)
    axes.set_ylabel(Ylabel)
    axes.text(max(X)-max(X)/9, max(Y), 'CC='+str(CC))
    plt.show()

def JobSizes(Log):
    n=0
    JobSizes_data=[]
    JobSizes_counter=dict()
    JobSizes_pdf=dict()
    for Job in Log:
        JobSizes=int(Job.split()[4])
        JobSizes_data.append(JobSizes)
    if JobSizes in JobSizes_counter:
        JobSizes_counter[JobSizes]+=1
    else:
        JobSizes_counter.setdefault(JobSizes,1)
    n+=1
    for time in JobSizes_counter:
        JobSizes_pdf.setdefault(time,JobSizes_counter[time]/n)
    return JobSizes_data,JobSizes_pdf 

def SubmitTimes(Log):
    n=0
    SubmitTime_data=[]
    SubmitTimes_counter=dict()
    SubmitTimes_pdf=dict()
    for Job in Log:
        SubmitTime=int(Job.split()[1])
        SubmitTime_data.append(SubmitTime)
    if SubmitTime in SubmitTimes_counter:
        SubmitTimes_counter[SubmitTime]+=1
    else:
        SubmitTimes_counter.setdefault(SubmitTime,1)
    n+=1
    for time in SubmitTimes_counter:
        SubmitTimes_pdf.setdefault(time,SubmitTimes_counter[time]/n)
    return SubmitTime_data,SubmitTimes_pdf  

def WaitTimes(Log):
    n=0
    WaitTime_data=[]
    WaitTimes_counter=dict()
    WaitTimes_pdf=dict()
    for Job in Log:
        WaitTime=int(Job.split()[2])
        WaitTime_data.append(WaitTime)
    if WaitTime in WaitTimes_counter:
        WaitTimes_counter[WaitTime]+=1
    else:
        WaitTimes_counter.setdefault(WaitTime,1)
    n+=1
    for time in WaitTimes_counter:
        WaitTimes_pdf.setdefault(time,WaitTimes_counter[time]/n)
    return WaitTime_data,WaitTimes_pdf 

def SelfSimilarity(s,lab,x,y):
    H, c, val = compute_Hc(s)
    axes = plt.subplots()[1]
    axes.plot(val[0], c*val[0]**H, color="blue")
    axes.scatter(val[0], val[1], color="red")
    axes.text(x,y,"Hurst exponent = {:.3f}".format(H))
    axes.set_title(lab)
    axes.set_xscale('log')
    axes.set_yscale('log')
    axes.set_xlabel('Time interval')
    axes.set_ylabel('R/S ratio')
    axes.grid(True)
    plt.show()
    return

def LoadMeasurment(Data1,Data2,Data3,Original,title):
    fig,(ax1,ax2,ax3,ax4)=plt.subplots(1,4)
    fig.suptitle(title)
    ax1.plot(Data1)
    ax1.set_title("First Trace")
    ax1.set_xlabel("Time In Seconds")
    ax1.set_ylabel("Load Percentage")
    ax2.plot(Data2)
    ax2.set_title("Second Trace")
    ax2.set_xlabel("Time In Seconds")
    ax2.set_ylabel("Load Percentage")
    ax3.plot(Data3)
    ax3.set_title("Third Trace")
    ax3.set_xlabel("Time In Seconds")
    ax3.set_ylabel("Load Percentage")
    ax4.plot(Original)
    ax4.set_title("Original Trace")
    ax4.set_xlabel("Time In Seconds")
    ax4.set_ylabel("Load Percentage")
    plt.show()
    return

def CDFsCompare(X1,Y1,X2,Y2,X3,Y3,X,Y,load,attrib):
    fig, (ax1, ax2,ax3,ax4) = plt.subplots(1, 4)
    fig.suptitle('CDF Of '+attrib+' with '+str(load)+'% Load')
    ax1.set_title('cdf for the first trace')
    ax2.set_title('cdf for the second trace')
    ax3.set_title('cdf for the third trace')
    ax4.set_title('cdf for the original trace')
    ax1.plot(X1,Y1,label='Trace1')
    ax2.plot(X2,Y2,label='Trace2')
    ax3.plot(X3,Y3,label='Trace3')
    ax4.plot(X,Y,label='Original Trace')
    ax1.set_xlabel('Time In Seconds')
    ax2.set_xlabel('Time In Seconds')
    ax3.set_xlabel('Time In Seconds')
    ax4.set_xlabel('Time In Seconds')
    ax1.set_ylabel('Probability')
    ax1.set_xscale('log',base=2)
    ax2.set_xscale('log',base=2)
    ax3.set_xscale('log',base=2)
    ax4.set_xscale('log',base=2)
    plt.show()
    # fig, ax1 = plt.subplots()
    # fig.suptitle('CDF Of '+attrib+' with '+str(load)+'% Load')
    # ax1.plot(X1,Y1,label='CDF for the first trace')
    # ax1.plot(X2,Y2,label='CDF for the second trace')
    # ax1.plot(X3,Y3,label='CDF for the third trace')
    # ax1.plot(X,Y,label='CDF for the original trace')
    # ax1.set_xlabel('Time In Seconds')
    # ax1.set_ylabel('Probability')
    # ax1.set_xscale('log',base=2)
    # plt.show()
    return

def ECDFsCompare(Data1,Data2,Data3,Data,load,attrib):
    fig, ax = plt.subplots()
    fig.suptitle('PDF Of '+attrib+' with '+str(load)+'% Load')
    ecdf1=ECDF(Data1)
    ecdf2=ECDF(Data2)
    ecdf3=ECDF(Data3)
    ecdf=ECDF(Data)
    ax.plot(ecdf1.x,ecdf1.y,label='Trace1')
    ax.plot(ecdf2.x,ecdf2.y,label='Trace2')
    ax.plot(ecdf3.x,ecdf3.y,label='Trace3')
    ax.plot(ecdf.x,ecdf.y,label='Original Trace')
    ax.legend()
    plt.show()
    return
    
def ScatterPlot(X1,Y1,X2,Y2,X3,Y3,load):
    fig,(ax1,ax2,ax3)=plt.subplots(1,3)
    fig.suptitle("Scatter Plot Of Wait Times As Function Of Subtimes")
    ax1.set_title("First Trace With "+str(load)+"% Load")
    ax2.set_title("Second Trace With "+str(load)+"% Load")
    ax3.set_title("Third Trace With "+str(load)+"% Load")
    ax1.set_xlabel('Wait Times')
    ax1.set_ylabel('Submit Times')
    ax2.set_xlabel('Wait Times')
    ax2.set_ylabel('Submit Times')
    ax3.set_xlabel('Wait Times')
    ax3.set_ylabel('Submit Times')
    ax1.scatter(X1,Y1)
    ax2.scatter(X2,Y2)
    ax3.scatter(X3,Y3)
    plt.show()
    return

def WaitTimesECDF(load80_1,load80_2,load80_3,load100_1,load100_2,load100_3,load120_1,load120_2,load120_3):
    ecdfload80_1 = ECDF(load80_1)
    ecdfload80_2 = ECDF(load80_2)
    ecdfload80_3 = ECDF(load80_3)
    ecdfload100_1 = ECDF(load100_1)
    ecdfload100_2 = ECDF(load100_2)
    ecdfload100_3 = ECDF(load100_3)
    ecdfload120_1 = ECDF(load120_1)
    ecdfload120_2 = ECDF(load120_2)
    ecdfload120_3 = ECDF(load120_3)
    fig,(ax1,ax2,ax3)=plt.subplots(1,3)
    fig.suptitle('ECDF Of Waittimes under different loads')        
    ax1.set_title('ECDF for the first trace of each load')
    ax2.set_title('ECDF for the second trace of each load')
    ax3.set_title('ECDF for the third trace of each load')
    ax1.plot(ecdfload80_1.x,ecdfload80_1.y,label='80% Load')
    ax1.plot(ecdfload100_1.x,ecdfload100_1.y,label='100% Load')
    ax1.plot(ecdfload120_1.x,ecdfload120_1.y,label='120% Load')
    ax2.plot(ecdfload80_2.x,ecdfload80_2.y,label='80% Load')
    ax2.plot(ecdfload100_2.x,ecdfload100_2.y,label='100% Load')
    ax2.plot(ecdfload120_2.x,ecdfload120_2.y,label='120% Load')
    ax3.plot(ecdfload80_3.x,ecdfload80_3.y,label='80% Load')
    ax3.plot(ecdfload100_3.x,ecdfload100_3.y,label='100% Load')
    ax3.plot(ecdfload120_3.x,ecdfload120_3.y,label='120% Load')
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax1.set_xscale('log',base=10)
    ax1.set_yscale('log',base=10)
    ax2.set_xscale('log',base=10)
    ax2.set_yscale('log',base=10)
    ax3.set_xscale('log',base=10)
    ax3.set_yscale('log',base=10)
    plt.show()
    
def GetJobsPerHour(Log):
    lastHour=math.floor((int(Log[-1].split()[1])+int(Log[-1].split()[3]))/3600)+1
    LogHours=np.zeros(lastHour)
    for Job in Log:   
        submit_t=math.floor(int(Job.split()[1])/3600)
        if submit_t<lastHour:  
            LogHours[submit_t]+=1
    return LogHours

def TrendsGraph(Data1,Data2,Data3,Data,load):
    fig,(ax1,ax2,ax3,ax4)=plt.subplots(1,4)
    fig.suptitle("Number Of Jobs Per Hour")
    ax1.set_title("First Trace With "+str(load)+"% Load")
    ax2.set_title("Second Trace With "+str(load)+"% Load")
    ax3.set_title("Third Trace With "+str(load)+"% Load")
    ax4.set_title("Original Log")
    ax1.set_ylabel('Number Of Jobs')
    ax1.set_xlabel('Time in Hours')
    ax2.set_xlabel('Time in Hours')
    ax3.set_xlabel('Time in Hours')
    ax4.set_xlabel('Time in Hours')
    ax1.plot(Data1)
    ax2.plot(Data2)
    ax3.plot(Data3)
    ax4.plot(Data)
    return

def DailyCycles(Log):
    DailyCycle=np.zeros(24)
    for job in Log:
        sub=(math.floor(int(job.split()[1])/3600)) % 24
        DailyCycle[sub]+=1
    return DailyCycle

def WeeklyCycles(Log):
    WeeklyCycle=np.zeros(7)
    for job in Log:
        sub=(math.floor(int(job.split()[1])/86400)) % 7
        WeeklyCycle[sub]+=1
    return WeeklyCycle

def ShowCyclesGraph(load80_1,load80_2,load80_3,load100_1,load100_2,load100_3,load120_1,load120_2,load120_3,Data):
    fig,(ax1,ax2,ax3)=plt.subplots(1,3)
    fig.suptitle("Daily Cycle Graph")
    ax1.set_title("Traces With 80% Load")
    ax2.set_title("Traces With 100% Load")
    ax3.set_title("Traces With 120% Load")
    ax1.set_ylabel('Number Of Jobs')
    ax1.set_xlabel('Time Of The Day')
    ax2.set_xlabel('Time Of The Day')
    ax3.set_xlabel('Time Of The Day')
    ax1.plot(load80_1,label="Trace1")
    ax1.plot(load80_2,label="Trace2")
    ax1.plot(load80_3,label="Trace3")
    ax1.plot(Data,label="Original Trace")
    ax2.plot(load100_1,label="Trace1")
    ax2.plot(load100_2,label="Trace2")
    ax2.plot(load100_3,label="Trace3")
    ax2.plot(Data,label="Original Trace")
    ax3.plot(load120_1,label="Trace1")
    ax3.plot(load120_2,label="Trace2")
    ax3.plot(load120_3,label="Trace3")
    ax3.plot(Data,label="Original Trace")
    plt.plot()
    return 

def ShowWeeklyCyclesGraph(load80_1,load80_2,load80_3,load100_1,load100_2,load100_3,load120_1,load120_2,load120_3,Data):
    fig,(ax1,ax2,ax3)=plt.subplots(1,3)
    fig.suptitle("Weekly Cycle Graph")
    ax1.set_title("Traces With 80% Load")
    ax2.set_title("Traces With 100% Load")
    ax3.set_title("Traces With 120% Load")
    ax1.set_ylabel('Number Of Jobs')
    ax1.set_xlabel('Day Of The Week')
    ax2.set_xlabel('Day Of The Week')
    ax3.set_xlabel('Day Of The Week')
    ax1.plot(load80_1,label="Trace1")
    ax1.plot(load80_2,label="Trace2")
    ax1.plot(load80_3,label="Trace3")
    ax1.plot(Data,label="Original Trace")
    ax2.plot(load100_1,label="Trace1")
    ax2.plot(load100_2,label="Trace2")
    ax2.plot(load100_3,label="Trace3")
    ax2.plot(Data,label="Original Trace")
    ax3.plot(load120_1,label="Trace1")
    ax3.plot(load120_2,label="Trace2")
    ax3.plot(load120_3,label="Trace3")
    ax3.plot(Data,label="Original Trace")
    plt.plot()
    return 

def UserDistributionGraphs(Data1,Data2,Data3,Data,load):
    fig,ax1=plt.subplots()
    fig.suptitle("User Distribution Graph")
    ax1.set_ylabel('Number Of Users')
    ax1.set_xlabel('Time in Days')
    ax1.plot(Data1,label="First Trace With "+str(load)+"% Load")
    ax1.plot(Data2,label="Second Trace With "+str(load)+"% Load")
    ax1.plot(Data3,label="Third Trace With "+str(load)+"% Load")
    ax1.plot(Data,label="Original Log")
    plt.plot()
    return 

def LocalityOfSampling(Time,attr,title):
    fig,(ax1,ax2)=plt.subplots(1,2)
    fig.suptitle("Plot of job sizes as function of submit times "+title)
    ax1.set_title('Original Data')
    ax2.set_title('Scrambled Data')
    ax1.scatter(Time,attr,marker='.',color='crimson',alpha=0.1)
    ax1.set_xlabel('Time in Seconds')
    ax2.set_xlabel('Time in Seconds')
    ax1.set_ylabel('Job Size')
    np.random.shuffle(attr)
    ax2.scatter(Time,attr,marker='.',color='crimson',alpha=0.1)
   # ax1.set_xscale('log',base=2)
    # c=list(zip(Time,attribute))
    # random.shuffle(c)
    # Time, attribute = zip(*c)
    # ax2.set_title('Scrambled Data')
    # ax2.plot(Time,attribute)
    # ax2.set_xscale('log',base=2)    
    plt.show()

def CreateSubmissionRate(Data,Rate):
  PeriodOfTime=1
  SubmissionRate=dict()
  SubmissionRatePDF=dict()
  SubmissionRateCDF=dict()
  SubmissionRateECDF=dict()
  for r in Data:      
      row_split_list=r.split()
      if Rate*PeriodOfTime>=int(row_split_list[1]):
          if PeriodOfTime in SubmissionRate:
              SubmissionRate[PeriodOfTime]+=1
          else:
              SubmissionRate.setdefault(PeriodOfTime,1)    
      else:
          PeriodOfTime+=1
          SubmissionRate.setdefault(PeriodOfTime,1)

  for key in SubmissionRate:
      SubmissionRatePDF.setdefault(key,SubmissionRate[key]/len(Data))
  i=0
  for key in SubmissionRate:
      if i==0:
       SubmissionRateCDF.setdefault(key,SubmissionRatePDF[key])
       SubmissionRateECDF.setdefault(key,1-SubmissionRateCDF[key]) 
      else:
       SubmissionRateCDF.setdefault(key,SubmissionRatePDF[key]+SubmissionRateCDF[key-1])
       SubmissionRateECDF.setdefault(key,1-SubmissionRateCDF[key]) 
      i+=1  
  SubmissionRateECDF=ECDF(list(SubmissionRate.values()))           
  return SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF       

# load all traces to lists
with open(outputload80_1, "r") as output1:
    for row in output1.readlines():
        Log_load80_1.append(row)
with open(outputload80_2, "r") as output1:
    for row in output1.readlines():
        Log_load80_2.append(row)
with open(outputload80_3, "r") as output1:
    for row in output1.readlines():
        Log_load80_3.append(row)
with open(outputload100_1, "r") as output1:
    for row in output1.readlines():
        Log_load100_1.append(row)
with open(outputload100_2, "r") as output1:
    for row in output1.readlines():
        Log_load100_2.append(row)
with open(outputload100_3, "r") as output1:
    for row in output1.readlines():
        Log_load100_3.append(row)
with open(outputload120_1, "r") as output1:
    for row in output1.readlines():
        Log_load120_1.append(row)
with open(outputload120_2, "r") as output1:
    for row in output1.readlines():
        Log_load120_2.append(row)
with open(outputload120_3, "r") as output1:
    for row in output1.readlines():
        Log_load120_3.append(row)
with open(original_log, "r") as swf_file:
    for row in swf_file.readlines():
        row_split_list = row.split()
        if row_split_list[0]==";":
            continue
        Original_Log.append(row)

Original_Log=AdjustThinkTimes(Original_Log)
#Generate interarrivals lists and pdf
# Interarrivals_data_load80_1,Xload80_1,Y_load80_1=Interarrivals(Log_load80_1)
# Interarrivals_data_load80_2,Xload80_2,Y_load80_2=Interarrivals(Log_load80_2)
# Interarrivals_data_load80_3,Xload80_3,Y_load80_3=Interarrivals(Log_load80_3)
# Interarrivals_data_load100_1,Xload100_1,Y_load100_1=Interarrivals(Log_load100_1)
# Interarrivals_data_load100_2,Xload100_2,Y_load100_2=Interarrivals(Log_load100_2)
# Interarrivals_data_load100_3,Xload100_3,Y_load100_3=Interarrivals(Log_load100_3)
# Interarrivals_data_load120_1,Xload120_1,Y_load120_1=Interarrivals(Log_load100_1)
# Interarrivals_data_load120_2,Xload120_2,Y_load120_2=Interarrivals(Log_load120_2)
# Interarrivals_data_load120_3,Xload120_3,Y_load120_3=Interarrivals(Log_load120_3)
# Interarrivals_data,X,Y=Interarrivals(Original_Log)
# CDFsCompare(Xload80_1,Y_load80_1, Xload80_2,Y_load80_2, Xload80_3,Y_load80_3, X,Y, 80, 'Interarrival Times')
# CDFsCompare(Xload100_1,Y_load100_1, Xload100_2,Y_load100_2, Xload100_3,Y_load100_3, X,Y, 100, 'Interarrival Times')
# CDFsCompare(Xload120_1,Y_load120_1, Xload120_2,Y_load120_2, Xload120_3,Y_load120_3, X,Y, 120, 'Interarrival Times')

# Generate Consumption lists and pdf
# ConsumptionData_load80_1,avg_load80_1=Consumption(Log_load80_1,False)
# ConsumptionData_load80_2,avg_load80_2=Consumption(Log_load80_2,False)
# ConsumptionData_load80_3,avg_load80_3=Consumption(Log_load80_3,False)
# ConsumptionData_load100_1,avg_load100_1=Consumption(Log_load100_1,False)
# ConsumptionData_load100_2,avg_load100_2=Consumption(Log_load100_2,False)
# ConsumptionData_load100_3,avg_load100_3=Consumption(Log_load100_3,False)
# ConsumptionData_load120_1,avg_load120_1=Consumption(Log_load120_1,False)
# ConsumptionData_load120_2,avg_load120_2=Consumption(Log_load120_2,False)
# ConsumptionData_load120_3,avg_load120_3=Consumption(Log_load120_3,False)
# ConsumptionData,avg_Original=Consumption(Original_Log,True)
# LoadMeasurment(ConsumptionData_load80_1, ConsumptionData_load80_2, ConsumptionData_load80_3, ConsumptionData,'Consumption Graph Of Each One Of The Realistic Traces With 80% Load And The Original Trace')
# LoadMeasurment(ConsumptionData_load100_1, ConsumptionData_load100_2, ConsumptionData_load100_3, ConsumptionData,'Consumption Graph Of Each One Of The Realistic Traces With 100% Load And The Original Trace')
# LoadMeasurment(ConsumptionData_load120_1, ConsumptionData_load120_2, ConsumptionData_load120_3, ConsumptionData,'Consumption Graph Of Each One Of The Realistic Traces With 120% Load And The Original Trace')

# # Generate Runtime lists and pdf
# Runtime_data_load80_1,Xload80_1,Y_load80_1=Runtimes(Log_load80_1)
# Runtime_data_load80_2,Xload80_2,Y_load80_2=Runtimes(Log_load80_2)
# Runtime_data_load80_3,Xload80_3,Y_load80_3=Runtimes(Log_load80_3)
# Runtime_data_load100_1,Xload100_1,Y_load100_1=Runtimes(Log_load100_1)
# Runtime_data_load100_2,Xload100_2,Y_load100_2=Runtimes(Log_load100_2)
# Runtime_data_load100_3,Xload100_3,Y_load100_3=Runtimes(Log_load100_3)
# Runtime_data_load120_1,Xload120_1,Y_load120_1=Runtimes(Log_load120_1)
# Runtime_data_load120_2,Xload120_2,Y_load120_2=Runtimes(Log_load120_2)
# Runtime_data_load120_3,Xload120_3,Y_load120_3=Runtimes(Log_load120_3)
# Runtime_data,X,Y=Runtimes(Original_Log)
# CDFsCompare(Xload80_1,Y_load80_1, Xload80_2,Y_load80_2, Xload80_3,Y_load80_3, X,Y, 80, 'Runtimes')
# CDFsCompare(Xload100_1,Y_load100_1, Xload100_2,Y_load100_2, Xload100_3,Y_load100_3, X,Y, 100, 'Runtimes')
# CDFsCompare(Xload120_1,Y_load120_1, Xload120_2,Y_load120_2, Xload120_3,Y_load120_3, X,Y, 120, 'Runtimes')


# Generate User Distribution lists and pdf

# Users_Distribution_load80_1=UserDistribution(Log_load80_1)
# Users_Distribution_load80_2=UserDistribution(Log_load80_2)
# Users_Distribution_load80_3=UserDistribution(Log_load80_3)
# Users_Distribution_load100_1=UserDistribution(Log_load100_1)
# Users_Distribution_load100_2=UserDistribution(Log_load100_2)
# Users_Distribution_load100_3=UserDistribution(Log_load100_3)
# Users_Distribution_load120_1=UserDistribution(Log_load120_1)
# Users_Distribution_load120_2=UserDistribution(Log_load120_2)
# Users_Distribution_load120_3=UserDistribution(Log_load120_3)
# Users_Distribution=UserDistribution(Original_Log)
# UserDistributionGraphs(Users_Distribution_load80_1, Users_Distribution_load80_2, Users_Distribution_load80_3, Users_Distribution, 80)
# UserDistributionGraphs(Users_Distribution_load100_1, Users_Distribution_load100_2, Users_Distribution_load100_3, Users_Distribution, 100)
# UserDistributionGraphs(Users_Distribution_load120_1, Users_Distribution_load120_2, Users_Distribution_load120_3, Users_Distribution, 120)

#Users_Distribution_load80_1=UserDistribution(Log_load80_1)
#Users_Distribution_load80_2=UserDistribution(Log_load80_2)
#Users_Distribution_load80_3=UserDistribution(Log_load80_3)
#Users_Distribution_load100_1=UserDistribution(Log_load100_1)
#Users_Distribution_load100_2=UserDistribution(Log_load100_2)
#Users_Distribution_load100_3=UserDistribution(Log_load100_3)
#Users_Distribution_load120_1=UserDistribution(Log_load120_1)
#Users_Distribution_load120_2=UserDistribution(Log_load120_2)
#Users_Distribution_load120_3=UserDistribution(Log_load120_3)
#Users_Distribution=UserDistribution(Original_Log)
#UserDistributionGraphs(Users_Distribution_load80_1, Users_Distribution_load80_2, Users_Distribution_load80_3, Users_Distribution, 80)
#UserDistributionGraphs(Users_Distribution_load100_1, Users_Distribution_load100_2, Users_Distribution_load100_3, Users_Distribution, 100)
#UserDistributionGraphs(Users_Distribution_load120_1, Users_Distribution_load120_2, Users_Distribution_load120_3, Users_Distribution, 120)


# Generate Think Times lists and pdf
# Thinktime_data_load80_1,Thinktimes_pdf_load80_1=ThinkTimes(Log_load80_1)
# Thinktime_data_load80_2,Thinktimes_pdf_load80_2=ThinkTimes(Log_load80_2)
# Thinktime_data_load80_3,Thinktimes_pdf_load80_3=ThinkTimes(Log_load80_3)
# Thinktime_data_load100_1,Thinktimes_pdf_load100_1=ThinkTimes(Log_load100_1)
# Thinktime_data_load100_2,Thinktimes_pdf_load100_2=ThinkTimes(Log_load100_2)
# Thinktime_data_load100_3,Thinktimes_pdf_load100_3=ThinkTimes(Log_load100_3)
# Thinktime_data_load120_1,Thinktimes_pdf_load120_1=ThinkTimes(Log_load120_1)
# Thinktime_data_load120_2,Thinktimes_pdf_load120_2=ThinkTimes(Log_load120_2)
# Thinktime_data_load120_3,Thinktimes_pdf_load120_3=ThinkTimes(Log_load120_3)
# Thinktime_data,Thinktimes_pdf=ThinkTimes(Original_Log)
# ECDFsCompare(Thinktime_data_load80_1, Thinktime_data_load80_2, Thinktime_data_load80_3, Thinktime_data, 80, 'Think Times')
# ECDFsCompare(Thinktime_data_load100_1, Thinktime_data_load100_2, Thinktime_data_load100_3, Thinktime_data, 100, 'Think Times')
# ECDFsCompare(Thinktime_data_load120_1, Thinktime_data_load120_2, Thinktime_data_load120_3, Thinktime_data, 120, 'Think Times')

# Generate Job Sizes lists and pdf
# JobSizes_data_load80_1,JobSizes_pdf_load80_1=JobSizes(Log_load80_1)
# JobSizes_data_load80_2,JobSizes_pdf_load80_2=JobSizes(Log_load80_2)
# JobSizes_data_load80_3,JobSizes_pdf_load80_3=JobSizes(Log_load80_3)
# JobSizes_data_load100_1,JobSizes_pdf_load100_1=JobSizes(Log_load100_1)
# JobSizes_data_load100_2,JobSizes_pdf_load100_2=JobSizes(Log_load100_2)
# JobSizes_data_load100_3,JobSizes_pdf_load100_3=JobSizes(Log_load100_3)
# JobSizes_data_load120_1,JobSizes_pdf_load120_1=JobSizes(Log_load120_1)
# JobSizes_data_load120_2,JobSizes_pdf_load120_2=JobSizes(Log_load120_2)
# JobSizes_data_load120_3,JobSizes_pdf_load120_3=JobSizes(Log_load120_3)
# JobSizes_data,JobSizes_pdf=JobSizes(Original_Log)

# Generate Submit Times lists and pdf
# SubmitTimes_data_load80_1,SubmitTimes_pdf_load80_1=SubmitTimes(Log_load80_1)
# SubmitTimes_data_load80_2,SubmitTimes_pdf_load80_2=SubmitTimes(Log_load80_2)
# SubmitTimes_data_load80_3,SubmitTimes_pdf_load80_3=SubmitTimes(Log_load80_3)
# SubmitTimes_data_load100_1,SubmitTimes_pdf_load100_1=SubmitTimes(Log_load100_1)
# SubmitTimes_data_load100_2,SubmitTimes_pdf_load100_2=SubmitTimes(Log_load100_2)
# SubmitTimes_data_load100_3,SubmitTimes_pdf_load100_3=SubmitTimes(Log_load100_3)
# SubmitTimes_data_load120_1,SubmitTimes_pdf_load120_1=SubmitTimes(Log_load120_1)
# SubmitTimes_data_load120_2,SubmitTimes_pdf_load120_2=SubmitTimes(Log_load120_2)
# SubmitTimes_data_load120_3,SubmitTimes_pdf_load120_3=SubmitTimes(Log_load120_3)
# SubmitTimes_data,SubmitTimes_pdf=SubmitTimes(Original_Log)

# LocalityOfSampling(SubmitTimes_data_load80_1, JobSizes_data_load80_1, "80% load first trace")
# LocalityOfSampling(SubmitTimes_data_load80_2, JobSizes_data_load80_2, "80% load second trace")
# LocalityOfSampling(SubmitTimes_data_load80_3, JobSizes_data_load80_3, "80% load third trace")
# LocalityOfSampling(SubmitTimes_data_load100_1, JobSizes_data_load100_1, "100% load first trace")
# LocalityOfSampling(SubmitTimes_data_load100_2, JobSizes_data_load100_2, "100% load second trace")
# LocalityOfSampling(SubmitTimes_data_load100_3, JobSizes_data_load100_3, "100% load third trace")
# LocalityOfSampling(SubmitTimes_data_load120_1, JobSizes_data_load120_1, "120% load first trace")
# LocalityOfSampling(SubmitTimes_data_load120_2, JobSizes_data_load120_2, "120% load second trace")
# LocalityOfSampling(SubmitTimes_data_load120_3, JobSizes_data_load120_3, "120% load third trace")
# LocalityOfSampling(SubmitTimes_data, JobSizes_data, "the original trace")

# Generate Wait Times lists and pf
# WaitTimes_data_load80_1,WaitTimes_pdf_load80_1=WaitTimes(Log_load80_1)
# WaitTimes_data_load80_2,WaitTimes_pdf_load80_2=WaitTimes(Log_load80_2)
# WaitTimes_data_load80_3,WaitTimes_pdf_load80_3=WaitTimes(Log_load80_3)
# WaitTimes_data_load100_1,WaitTimes_pdf_load100_1=WaitTimes(Log_load100_1)
# WaitTimes_data_load100_2,WaitTimes_pdf_load100_2=WaitTimes(Log_load100_2)
# WaitTimes_data_load100_3,WaitTimes_pdf_load100_3=WaitTimes(Log_load100_3)
# WaitTimes_data_load120_1,WaitTimes_pdf_load120_1=WaitTimes(Log_load120_1)
# WaitTimes_data_load120_2,WaitTimes_pdf_load120_2=WaitTimes(Log_load120_2)
# WaitTimes_data_load120_3,WaitTimes_pdf_load120_3=WaitTimes(Log_load120_3)
# WaitTimes_data,WaitTimes_pdf=SubmitTimes(Original_Log)

# WaitTimesECDF(WaitTimes_data_load80_1, WaitTimes_data_load80_2, WaitTimes_data_load80_3,WaitTimes_data_load100_1, WaitTimes_data_load100_2, WaitTimes_data_load100_3,WaitTimes_data_load120_1, WaitTimes_data_load120_2, WaitTimes_data_load120_3)
# ScatterPlot(WaitTimes_data_load80_1, SubmitTimes_data_load80_1, WaitTimes_data_load80_2, SubmitTimes_data_load80_2, WaitTimes_data_load80_3, SubmitTimes_data_load80_3, 80)
# ScatterPlot(WaitTimes_data_load100_1, SubmitTimes_data_load100_1, WaitTimes_data_load100_2, SubmitTimes_data_load100_2, WaitTimes_data_load100_3, SubmitTimes_data_load100_3, 100)
# ScatterPlot(WaitTimes_data_load120_1, SubmitTimes_data_load120_1, WaitTimes_data_load120_2, SubmitTimes_data_load120_2, WaitTimes_data_load120_3, SubmitTimes_data_load120_3, 120)

# CrossCorellation(Runtime_data,JobSizes_data,'Original Trace Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load80_1,JobSizes_data_load80_1,'Realistic Trace 80% Load 1 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load80_2,JobSizes_data_load80_2,'Realistic Trace 80% Load 2 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load80_3,JobSizes_data_load80_3,'Realistic Trace 80% load 3 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load100_1,JobSizes_data_load100_1,'Realistic Trace 100% Load 1 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load100_2,JobSizes_data_load100_2,'Realistic Trace 100% Load 2 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load100_3,JobSizes_data_load100_3,'Realistic Trace 100% Load 3 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load120_1,JobSizes_data_load120_1,'Realistic Trace 120% Load 1 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load120_2,JobSizes_data_load120_2,'Realistic Trace 120% Load 2 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')
# CrossCorellation(Runtime_data_load120_3,JobSizes_data_load120_3,'Realistic Trace 120% Load 3 Cross-Correlation Runtimes & Job Sizes','Runtimes','JobSizes')

# CrossCorellation(Runtime_data,Thinktime_data,'Original Trace Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load80_1,Thinktime_data_load80_1,'Realistic Trace 80% Load 1 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load80_2,Thinktime_data_load80_2,'Realistic Trace 80% Load 2 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load80_3,Thinktime_data_load80_3,'Realistic Trace 80% Load 3 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load100_1,Thinktime_data_load100_1,'Realistic Trace 100% Load 1 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load100_2,Thinktime_data_load100_2,'Realistic Trace 100% Load 2 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load100_3,Thinktime_data_load100_3,'Realistic Trace 100% Load 3 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load120_1,Thinktime_data_load120_1,'Realistic Trace 120% Load 1 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load120_2,Thinktime_data_load120_2,'Realistic Trace 120% Load 2 Cross-Correlation Runtimes & Think times','Runtimes','Think times')
# CrossCorellation(Runtime_data_load120_3,Thinktime_data_load120_3,'Realistic Trace 120% Load 3 Cross-Correlation Runtimes & Think times','Runtimes','Think times')

# SelfSimilarity(SubmitTimes_data_load80_1,"Load 80% First Realistic Trace",60,1465)
# SelfSimilarity(SubmitTimes_data_load80_2,"Load 80% Second Realistic Trace",60,1366)
# SelfSimilarity(SubmitTimes_data_load80_3,"Load 80% Third Realistic Trace",60,1667)
# SelfSimilarity(SubmitTimes_data, "Original Trace",60,3068)

# SelfSimilarity(SubmitTimes_data_load100_1,"Load 100% First Realistic Trace",60,1465)
# SelfSimilarity(SubmitTimes_data_load100_2,"Load 100% Second Realistic Trace",60,1366)
# SelfSimilarity(SubmitTimes_data_load100_3,"Load 100% Third Realistic Trace",60,1667)
# SelfSimilarity(SubmitTimes_data, "Original Trace",60,3068)

# SelfSimilarity(SubmitTimes_data_load120_1,"Load 120% First Realistic Trace",60,1465)
# SelfSimilarity(SubmitTimes_data_load120_2,"Load 120% Second Realistic Trace",60,1366)
# SelfSimilarity(SubmitTimes_data_load120_3,"Load 120% Third Realistic Trace",60,1667)
# SelfSimilarity(SubmitTimes_data, "Original Trace",60,3068)

# JobNumberLoad80_1=GetJobsPerHour(Log_load80_1)
# JobNumberLoad80_2=GetJobsPerHour(Log_load80_2)
# JobNumberLoad80_3=GetJobsPerHour(Log_load80_3)
# JobNumberLoad100_1=GetJobsPerHour(Log_load100_1)
# JobNumberLoad100_2=GetJobsPerHour(Log_load100_2)
# JobNumberLoad100_3=GetJobsPerHour(Log_load100_3)
# JobNumberLoad120_1=GetJobsPerHour(Log_load120_1)
# JobNumberLoad120_2=GetJobsPerHour(Log_load120_2)
# JobNumberLoad120_3=GetJobsPerHour(Log_load120_3)
# JobNumber=GetJobsPerHour(Original_Log)
# TrendsGraph(JobNumberLoad80_1, JobNumberLoad80_2, JobNumberLoad80_3, JobNumber, 80)
# TrendsGraph(JobNumberLoad100_1, JobNumberLoad100_2, JobNumberLoad100_3, JobNumber, 100)
# TrendsGraph(JobNumberLoad120_1, JobNumberLoad120_2, JobNumberLoad120_3, JobNumber, 120)

# DailyCyclesLoad80_1=DailyCycles(Log_load80_1)
# DailyCyclesLoad80_2=DailyCycles(Log_load80_2)
# DailyCyclesLoad80_3=DailyCycles(Log_load80_3)
# DailyCyclesLoad100_1=DailyCycles(Log_load100_1)
# DailyCyclesLoad100_2=DailyCycles(Log_load100_2)
# DailyCyclesLoad100_3=DailyCycles(Log_load100_3)
# DailyCyclesLoad120_1=DailyCycles(Log_load120_1)
# DailyCyclesLoad120_2=DailyCycles(Log_load120_2)
# DailyCyclesLoad120_3=DailyCycles(Log_load120_3)
# DailyCyclesO=DailyCycles(Original_Log)
# ShowCyclesGraph(DailyCyclesLoad80_1, DailyCyclesLoad80_2, DailyCyclesLoad80_3, DailyCyclesLoad100_1, DailyCyclesLoad100_2, DailyCyclesLoad100_3, DailyCyclesLoad120_1, DailyCyclesLoad120_2, DailyCyclesLoad120_3, DailyCyclesO)

# WeeklyCyclesLoad80_1=WeeklyCycles(Log_load80_1)
# WeeklyCyclesLoad80_2=WeeklyCycles(Log_load80_2)
# WeeklyCyclesLoad80_3=WeeklyCycles(Log_load80_3)
# WeeklyCyclesLoad100_1=WeeklyCycles(Log_load100_1)
# WeeklyCyclesLoad100_2=WeeklyCycles(Log_load100_2)
# WeeklyCyclesLoad100_3=WeeklyCycles(Log_load100_3)
# WeeklyCyclesLoad120_1=WeeklyCycles(Log_load120_1)
# WeeklyCyclesLoad120_2=WeeklyCycles(Log_load120_2)
# WeeklyCyclesLoad120_3=WeeklyCycles(Log_load120_3)
# WeeklyCyclesO=WeeklyCycles(Original_Log)
# ShowWeeklyCyclesGraph(WeeklyCyclesLoad80_1, WeeklyCyclesLoad80_2, WeeklyCyclesLoad80_3, WeeklyCyclesLoad100_1, WeeklyCyclesLoad100_2, WeeklyCyclesLoad100_3, WeeklyCyclesLoad120_1, WeeklyCyclesLoad120_2, WeeklyCyclesLoad120_3, WeeklyCyclesO)

# Days=1
# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load100_1, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,100,1)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load100_2, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,100,2)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load100_3, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,100,3)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load80_1, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,80,1)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load80_2, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,80,2)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load80_3, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,80,3)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load120_1, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,120,1)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load120_2, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,120,2)

# SubmissionRate,SubmissionRatePDF,SubmissionRateCDF,SubmissionRateECDF  =CreateSubmissionRate(Log_load120_3, Days*24*60*60)
# PlotSubmission(SubmissionRate, SubmissionRatePDF, SubmissionRateCDF, SubmissionRateECDF, Days,120,3)

