#import pickle
import re
import scipy.io
#import math
import pandas as pd
#from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
#import seaborn as sns
#from sklearn.cluster import SpectralClustering
#from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings("ignore")

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
        


NewUserArrival=list()
i=0
while(i<14):
  NewUserArrival.append(0)
  i+=1

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
            SubmitInMinutes=round((int(row_split_list[1])/604800))
            while(SubmitInMinutes<len(NewUserArrival)):
                NewUserArrival[SubmitInMinutes]+=1
                SubmitInMinutes+=1  
              
InterarrivalsDict=dict()
RuntimesDict=dict()
JobSizesDict=dict()
ThinkTimesDict=dict()
NewUsersPerWeek=dict()
i=13
while i>0:
    NewUserArrival[i]=NewUserArrival[i]-NewUserArrival[i-1]
    NewUsersPerWeek.setdefault("Week"+str(i+1),str(NewUserArrival[i]))   
    i-=1
NewUsersPerWeek.setdefault("Week1",str(NewUserArrival[0]))    
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
wholesum=0
for key in RuntimesDict.keys():
    wholesum+=len(RuntimesDict[key])
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
    

features = ['Runtime','Interarrival_Time','Job_Size','Think_Time']
df=pd.DataFrame(Users)
df_=df.T
df_.columns =['Runtime','Interarrival_Time','Job_Size','Think_Time']
cluster0=dict()
cluster1=dict()
cluster2=dict()
cluster3=dict()
cluster4=dict()
cluster5=dict()
cluster6=dict()
ResidenceTimes = scipy.io.loadmat('ResidenceTimes.mat')
NewUserArrivals=scipy.io.loadmat('NewUsersPerWeek.mat')
dic=ResidenceTimes
i=0
for key in list(dic):
    if i<3:
        ResidenceTimes.pop(key)
    i+=1
    
dic=NewUserArrivals

i=0
for key in list(dic):
    if i<3:
        NewUserArrivals.pop(key)
    i+=1
    
#DBSCAN 
# dbscan=DBSCAN(eps=1000000,min_samples=2).fit(df_)
# df_['DBSCAN_clusters']=dbscan.labels_
# sns.pairplot(df_,hue='DBSCAN_clusters',palette='tab10')
# print('DBSCAN Score:',silhouette_score(df_[['Runtime', 'Interarrival_Time', 'Job_Size', 'Think_Time']],df_['DBSCAN_clusters']))

#spectral clustering
# spectral_clustering = SpectralClustering(n_clusters=7, assign_labels="discretize",random_state=0).fit(df_[features])
# df_['spectral_cluster'] = spectral_clustering.labels_
# sns.pairplot(df_,hue='spectral_cluster',palette='tab10')
# print('spectral Score:',silhouette_score(df_[['Runtime', 'Interarrival_Time', 'Job_Size', 'Think_Time']],df_['spectral_cluster']))

kmeans = KMeans(n_clusters=7, random_state=0).fit(df_[features])
df_['kmeans_cluster'] = kmeans.labels_
#sns.pairplot(df_,hue='kmeans_cluster',palette='tab10')
print('Kmean Score:',silhouette_score(df_[['Runtime', 'Interarrival_Time', 'Job_Size', 'Think_Time']],df_['kmeans_cluster']))
i=0
for j in df_.iterrows(): 
    if df_.loc[df_.index[i],'kmeans_cluster']==0:
        cluster0.setdefault("User"+str(i+1),(ResidenceTimes["User"+str(i+1)][0][0]).item())
    if df_.loc[df_.index[i],'kmeans_cluster']==1:
        cluster1.setdefault("User"+str(i+1),ResidenceTimes["User"+str(i+1)][0][0].item())
    if df_.loc[df_.index[i],'kmeans_cluster']==2:
        cluster2.setdefault("User"+str(i+1),ResidenceTimes["User"+str(i+1)][0][0].item())
    if df_.loc[df_.index[i],'kmeans_cluster']==3:
        cluster3.setdefault("User"+str(i+1),ResidenceTimes["User"+str(i+1)][0][0].item())
    if df_.loc[df_.index[i],'kmeans_cluster']==4:
        cluster4.setdefault("User"+str(i+1),ResidenceTimes["User"+str(i+1)][0][0].item())
    if df_.loc[df_.index[i],'kmeans_cluster']==5:
        cluster5.setdefault("User"+str(i+1),ResidenceTimes["User"+str(i+1)][0][0].item())
    if df_.loc[df_.index[i],'kmeans_cluster']==6:
        cluster6.setdefault("User"+str(i+1),ResidenceTimes["User"+str(i+1)][0][0].item())
    i+=1

cluster0=dict(sorted(cluster0.items(), key=lambda item: item[1]))
cluster1=dict(sorted(cluster1.items(), key=lambda item: item[1]))
cluster2=dict(sorted(cluster2.items(), key=lambda item: item[1]))
cluster3=dict(sorted(cluster3.items(), key=lambda item: item[1]))
cluster4=dict(sorted(cluster4.items(), key=lambda item: item[1]))
cluster5=dict(sorted(cluster5.items(), key=lambda item: item[1]))
cluster6=dict(sorted(cluster6.items(), key=lambda item: item[1]))

j=1
for i in range(3):
    
    config_file=open("Input1\\config_file"+str(i+1)+".txt","w")
    config_file.write("Residence ")
    for user in ResidenceTimes.keys():
        res_time=str(ResidenceTimes[user][0][0].item())
        config_file.write(user+":"+res_time+" ")
    
    config_file.write("\nActivity  ")
    for week in NewUserArrivals.keys():
        newusers=str(NewUserArrivals[week].item())
        config_file.write(week+":"+newusers+" ")
        
    config_file.write("\nRandom_Seed "+str(j)+"\n")
    j+=1
    if i==0:
        config_file.write("Load 100\n")
    if i==1:
        config_file.write("Load 120\n")
    if i==2:
        config_file.write("Load 80\n")

    
    chosenusers=list()
    
    config_file.write("Long-Term User4 User25 User17\n")
    chosenusers.append(list(cluster0)[len(cluster0)-1])#long term
    chosenusers.append(list(cluster0)[0])#short term
    chosenusers.append(list(cluster0)[2])#short term
    chosenusers.append(list(cluster1)[1])#short term
    chosenusers.append(list(cluster2)[0])#short term
    chosenusers.append(list(cluster3)[len(cluster3)-1])#long term
    chosenusers.append(list(cluster3)[2])#short term
    chosenusers.append(list(cluster3)[3])#short term
    chosenusers.append(list(cluster4)[2])#short term
    chosenusers.append(list(cluster5)[1])#short term
    chosenusers.append(list(cluster6)[0])#long term
    
  
    swf_lines=list()
    temp = re.compile("([a-zA-Z]+)([0-9]+)") 
    
    for user in chosenusers:
        res = temp.match(user).groups() 
        swf_lines.append(UsersDict[res[1]])
        
        
    for lines in swf_lines:
        for line in lines:
            config_file.write(line)

    
    

    config_file.close()
    
    
    
    
j=1
for i in range(3):
    
    config_file=open("Input2\\config_file"+str(i+1)+".txt","w")
    config_file.write("Residence ")
    for user in ResidenceTimes.keys():
        res_time=str(ResidenceTimes[user][0][0].item())
        config_file.write(user+":"+res_time+" ")
    
    config_file.write("\nActivity  ")
    for week in NewUserArrivals.keys():
        newusers=str(NewUserArrivals[week].item())
        config_file.write(week+":"+newusers+" ")
        
    config_file.write("\nRandom_Seed "+str(j)+"\n")
    j+=1
    if i==0:
        config_file.write("Load 100\n")
    if i==1:
        config_file.write("Load 120\n")
    if i==2:
        config_file.write("Load 80\n")

    
    chosenusers=list()
    
    config_file.write("Long-Term User9 User7 User25 User18\n")
    chosenusers.append(list(cluster0)[len(cluster0)-3])#long term
    chosenusers.append(list(cluster0)[len(cluster0)-4])#long term    
    chosenusers.append(list(cluster0)[4])#short term
    chosenusers.append(list(cluster0)[5])#short term
    chosenusers.append(list(cluster1)[1])#short term
    chosenusers.append(list(cluster2)[0])#short term
    chosenusers.append(list(cluster3)[len(cluster3)-1])#long term
    chosenusers.append(list(cluster3)[5])#short term
    chosenusers.append(list(cluster3)[9])#short term
    chosenusers.append(list(cluster3)[10])#short term
    chosenusers.append(list(cluster4)[2])#short term
    chosenusers.append(list(cluster5)[1])#short term
    chosenusers.append(list(cluster6)[1])#long term
    
    swf_lines=list()
    temp = re.compile("([a-zA-Z]+)([0-9]+)") 
    
    for user in chosenusers:
        res = temp.match(user).groups() 
        swf_lines.append(UsersDict[res[1]])
        
        
    for lines in swf_lines:
        for line in lines:
            config_file.write(line)

    
    

    config_file.close()
#scipy.io.savemat('UsersDataframe.mat',df_)
#scipy.io.savemat('Interarrivals.mat',InterarrivalsDict)
#scipy.io.savemat('Runtimes.mat',RuntimesDict)
#scipy.io.savemat('JobSizes.mat',JobSizesDict)
#scipy.io.savemat('ThinkTimes.mat',ThinkTimesDict)

#scipy.io.savemat('NewUsersPerWeek.mat',NewUsersPerWeek)

# -*- coding: utf-8 -*-
# """Kmeans.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/1HRmqEEju0mlN1jpunOOGi-QJ459EcVX1

# Hello! In this post I will teach you how to do a simple data classification using the KMeans algorithm. We will go through the concept of Kmeans first, and then dive into the Python code used to perform the classification.

# ## What is KMeans algorithm?

# Kmeans is a **classifier** algorithm. This means that it can attribute labels to data by identifying certain (hidden) patterns on it. It is also am **unsupervised** learning algorithm. It applies the labels without having a target, i.e a previously known label. Therefore, at the end of the training, it is up to the human behind the machine to understand what does the labels attributed mean and how this information can be interpreted.

# ### KMeans algorithm

# KMeans performs data clustering by separating it into groups. Each group is clearly separated and do not overlap. A set of data points is said to belong to a group depending on its distance a point called the centroid.

# A centroid consists in a point, with the same dimension is the data (1D, 2D, 3D, etc). It is placed on the center of the cluster, thus being called a centroid. 

# To exemplify, consider a point $x$ which we want to classify as label "banana", "apple" or "orange". KMeans works by measuring the distance of the point $x$ to the centroids of each cluster "banana", "apple" or "orange". Let's say these distances are b1 (distance from $x$ to "banana" centroid), a1 (distance from $x$ to "apple" centroid) and o1 (distance from $x$ to "orange" centroid). If a1 is the smallest distance, then Kmeans says that $x$ belongs to "apple". On the other hand, if b1 is the smallest, then $x$ belongs to "banana", and so on.

# The distance we refer here can be measured in different forms. A very simple way, and very popular is the **Euclidean Distance**. In a 2D space, the Euclidean distance between a point at coordinates (x1,y1) and another point at (x2,y2) is:

# $$
# d = \sqrt{(x_1-x_2)^2 + (y_1 - y_2)^2}
# $$

# Similarly, in a 3D space, the distance between point (x1,y1,z1) and point (x2,y2,z2) is:

# $$
# d = \sqrt{(x_1-x_2)^2 + (y_1 - y_2)^2 + (z_1 - z_2)^2}
# $$

# Before going through how the training is done, let's being to code our problem.

# ## Using Python to code KMeans algorithm

# The Python libraries that we will use are:
# - numpy -> for numerical computations;
# - matplotlib -> for data visualization
# """

# import numpy as np
# import matplotlib.pyplot as plt

# """In this exercise we will work with an hypothetical dataset generated using random values. The distinction between the groups are made by shifting the first part of the dataset a bit higher in the feature space, while shifting the second part a bit lower. This will create two more or less distinguishible groups."""

# X= -0.5 + np.random.rand(100,2)
# X1 = 0.5 + np.random.rand(50,2)
# X[50:100, :] = X1

# plt.scatter(X[ : , 0], X[ :, 1], s = 20, c = 'k')

# """Now we place the centroids randomly in the feature space above (2D), by using the `rand()` function from Numpy."""

# centroids = np.random.rand(2,2)
# centroids

# """Let's visualize the dataset and the centroids in the same plot. Notice that the randomly positioning of the centroids initially did not put them in the center of the spac, but a bit shifted to the left. This is not a big problem, since we will train the KMeans algorithm to correctly place the centroids to have a meaningful classification."""

# plt.scatter(X[ : , 0], X[ :, 1], s = 20, c = 'k')
# plt.scatter(centroids[:,0],centroids[:,1],s = 50, c = 'b',marker = '+')

# """Using the function `np.linalg.norm()` from numpy we can calculate the Euclidean distance from each point to each centroid. For instance, the following code is used to calculate the distances from all the points stored in the variable $X$ to the first centroid. Then we print the first 10 distances."""

# dist = np.linalg.norm(X - centroids[0,:],axis=1).reshape(-1,1)
# dist[:10,:]

# """Now we add the distance from all the points to the second centroid to the variable `dist` defined above. This will give as a matrix with N rows and 2 columns, where each row refers to one point of $X$, and each column is the distance value from one point to one of the centroids."""

# dist = np.append(dist,np.linalg.norm(X - centroids[1,:],axis=1).reshape(-1,1),axis=1)
# dist[:10,:]

# """### How to train KMeans algorithm?

# The training is done by repeating the following algorithm, until convergence:
# - Find the distance of each point to each cluster;
# - Attribute each point to a cluster by finding the minimum distance;
# - Update the position of each centroid by placing it at the average position of the cluster, according the point belonging to that cluster. This can be interpreted mathematically as:

# $$
# c_j = \frac{1}{n}\sum x_j
# $$

# Where $n$ is the number of points belonging to to the cluster $j$ and $c_j$ are the coordinates of the centroid of cluster $j$. $x_j$ are the points belonging to cluster $j$.

# - Check if the centroid position is almost the same as in the previous iteration. If yes, then assume convergence. Otherwise, repeat the steps.

# ### Implementing the Kmeans training algorithm

# First we attribute each point of $X$ to a cluster by using the `np.argmin()` function, which will tell which column of `dist` is the lowest one, thus returning 0 (for the first cluster) or 1 (second cluster).
# """

# classes = np.argmin(dist,axis=1)
# classes

# """Visualize how the points are being currently classified."""

# plt.scatter(X[classes == 0, 0], X[classes == 0, 1], s = 20, c = 'b')
# plt.scatter(X[classes == 1, 0], X[classes == 1, 1], s = 20, c = 'r')

# """Now we update the position of each centroid, by calculating it at the mean position of the cluster. For instance, if a certain point has the points (1,0), (2,1) and (0.5,0.5), then the updated position of the centroid is:

# $$
# c_j = ((1 + 2 + 0.5)/3, (0 + 1 + 0.5)/3)
# $$
# """

# # update position
# for class_ in set(classes):
#     centroids[class_,:] = np.mean(X[classes == class_,:],axis=0)
# centroids

# """To understand what is happening here, let's visualize the dataset with the updated positioning of the centroids."""

# plt.scatter(X[classes == 0, 0], X[classes == 0, 1], s = 20, c = 'b')
# plt.scatter(X[classes == 1, 0], X[classes == 1, 1], s = 20, c = 'r')
# plt.scatter(centroids[:,0],centroids[:,1],s = 50, c = 'k',marker = '+')

# """Then the complete training consists of running the same update over and over again, until the positions of the centroid stop changing significantly. In the following code, we define a class `KMeans` aggregating all the code explained above and runnign the training until convergence. The initialization consists in settinga a number `k` of classes. Then the method `train()` performs the training over a dataset, while the method `predict()` labels a new point according the positioning of the centroids stored in the object."""

# class KMeans:
#     def __init__(self,k):
#         self.k = k

#     def train(self,X,MAXITER = 100, TOL = 1e-3):
#         centroids = np.random.rand(self.k,X.shape[1])
#         centroidsold = centroids.copy()
#         for iter_ in range(MAXITER):
#             dist = np.linalg.norm(X - centroids[0,:],axis=1).reshape(-1,1)
#             for class_ in range(1,self.k):
#                 dist = np.append(dist,np.linalg.norm(X - centroids[class_,:],axis=1).reshape(-1,1),axis=1)
#             classes = np.argmin(dist,axis=1)
#             # update position
#             for class_ in set(classes):
#                 centroids[class_,:] = np.mean(X[classes == class_,:],axis=0)
#             if np.linalg.norm(centroids - centroidsold) < TOL:
#                 break
#                 print('Centroid converged')
#         self.centroids = centroids
    
#     def predict(self,X):
#         dist = np.linalg.norm(X - self.centroids[0,:],axis=1).reshape(-1,1)
#         for class_ in range(1,self.k):
#             dist = np.append(dist,np.linalg.norm(X - self.centroids[class_,:],axis=1).reshape(-1,1),axis=1)
#         classes = np.argmin(dist,axis=1)
#         return classes

# """Let's test our class by defining a KMeans classified with two centroids (k=2) and training in dataset $X$, as it was done step-by-step above."""

# kmeans = KMeans(7)
# kmeans.train(X)

# """Check how each point of $X$ is being classified after complete training by using the `predict()` method we implemented above. Each poitn will be attributed to cluster 0 or cluster 1."""

# classes = kmeans.predict(X)
# classes

# """Let's create a visualization of the final result, showing different colors for each cluster and the final position of the clusters (crosses in the plot)."""

# plt.scatter(X[classes == 0, 0], X[classes == 0, 1], s = 20, c = 'b')
# plt.scatter(X[classes == 1, 0], X[classes == 1, 1], s = 20, c = 'r')
# plt.scatter(kmeans.centroids[:,0],kmeans.centroids[:,1],s = 50, c = 'k',marker = '+')

# """Notice that it converged to a meaningful classification. The centroid is placed in the average position of each part of the dataset initially created, whith clear separation between each class.

# For illustrative purposes, check how the same algorithm can work on a higher-dimensional problem with no modification of code.
# """

# # X= -0.5 + np.random.rand(100,3)
# # X1 = 0.5 + np.random.rand(33,3)
# # X2 = 2 + np.random.rand(33,3)
# # X[33:66, :] = X1
# # X[67:, :] = X2


# # from mpl_toolkits.mplot3d import Axes3D
# # fig = plt.figure(figsize = (8,5))
# # ax = fig.add_subplot(111, projection='3d')
# # ax.scatter(X[:,0],X[:,1],X[:,2])

# # kmeans = KMeans(3)
# # kmeans.train(X)

# # kmeans.centroids

# # classes = kmeans.predict(X)
# # classes

# # fig = plt.figure(figsize = (8,5))
# # ax = fig.add_subplot(111, projection='3d')
# # ax.scatter(X[classes == 0,0],X[classes == 0,1],X[classes == 0,2])
# # ax.scatter(X[classes == 1,0],X[classes == 1,1],X[classes == 1,2])
# # ax.scatter(X[classes == 2,0],X[classes == 2,1],X[classes == 2,2])



