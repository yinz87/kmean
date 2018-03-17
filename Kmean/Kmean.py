# -*- coding: utf-8 -*-
"""
@author: yinz
@version: 1.0
K-means project
"""

import math
from pylab import *
import numpy
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Kmeans(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)  #set up UI framework
        self.master = master
        self.dataPath = "null" #data location
        self.centroid = [] #store set of centroids
        self.cluster = [] #store k sets of tuples
        self.dataMaps = [] #store data location
        
        self.importFile = Button(master, text = "open data fileProcess", width = 50, command = self.importData) #UI button to call importData function to read data
        self.importFile.grid(sticky = "w")
        
        self.processKMeans = Button(master, text = "K-Means Test", width = 50, command = self.KMeansTest) #UI button to call KmeansTest for cluster and centroids determination
        self.processKMeans.grid(sticky = "e")
        
        Label(master, text = "kValue").grid(row = 0, column = 0)
        self.kValue = Entry(master, width = 20) # word text box for user to input K value
        self.kValue.grid(row = 1, column = 0)

        fig=plt.figure(figsize=(16,8))
        self.canvas=FigureCanvasTkAgg(fig,master) # display clusters
        self.canvas.get_tk_widget().grid()
        self.canvas.show()
        
    #randomly generated centroids based on k, range of data imported, O(15)
    def getCentroids(self,k,xmax,xmin,ymax,ymin):
        validated = False
        # contiue if condition is not met
        while validated == False:
            #store generated distance between two centroids
            conditionCheck = []
            #randomly generated k number of x and y. The range of x and y are between smallest and largest x and y cooridate in the data set
            initialx = numpy.random.uniform(low = xmin, high = xmax, size = k)
            initialy = numpy.random.uniform(low = ymin, high = ymax, size = k)
            #check Euclidean distance between any two centroids that are not the same and order does not matter, O(5)
            for i in range (k):
                # O(15)
                for j in range (i+1,k):
                    # check distacne in 2 decimal places between two centroids 
                    distance = math.sqrt(math.pow((initialx[i] - initialx[j]), 2) + math.pow((initialy[i] - initialy[j]), 2))
                    # add to a list
                    conditionCheck.append(distance)
            validated = True
            # check for condition where the distance between all of two centorids should be greater than 0.5 unit, O(15)
            for a in (conditionCheck):
                if a < 0.5:
                    validated = False
        # store in a list
        self.centroid = pd.DataFrame({"x":initialx, "y":initialy})
        return self.centroid    
        
    # obtain user input K value
    def getKValue(self):
        k = self.kValue.get().strip()
        return k

    # obtain file locaiton and convert to unix format
    def getDataLoc(self):
        self.dataPath = filedialog.askopenfilename(filetypes = [("csv file","*.csv")])
        self.dataPath = self.dataPath.replace("/","\\\\")
        return self.dataPath
    
    # validate the data to ensure proper format of data file
    def validateData(self):
        validated = True
        try:
            # check if each column beside header is int or float
            self.dataMaps.x.astype(float)
            self.dataMaps.y.astype(float) 
        except ValueError:
            validated = False
        return validated
    
    # initiate centroid and get a list of centroid
    def initCentroid(self,k):
        xmax = max(self.dataMaps["x"])
        ymax = max(self.dataMaps["y"])
        xmin = min(self.dataMaps["x"])
        ymin = min(self.dataMaps["y"])
        self.centroid = self.getCentroids(k,xmax,xmin,ymax,ymin)
        self.centroid = self.centroid.round(1)
        return self.centroid

    # using the dataPath from getDataLoc() to retrive the data file and read the data into dataMaps list
    def importData(self):
        # clear list for each import
        self.dataMaps = []
        try:    
            # rad the data file into dataMaps list
            self.dataMaps = pd.read_csv(self.getDataLoc())
            # modify heading for uniform process
            self.dataMaps.columns = ['x','y']
            # to check for correct file used
            if self.validateData() == True:
                return self.dataMaps
            else:
                self.dataMaps = []
                # display error content in pop-up window
                messagebox.showerror("error", "data file should only contain numbers in first two columns")
        except FileNotFoundError:
            self.dataMaps = []
            messagebox.showerror ("Error", "please import data")

    # initalize k set of empty list in cluster list for data storage
    def initClusters(self,k):
        self.cluster =[]
        for i in range(k):
            # add set of empty list to cluster
            self.cluster.append([])
        return self.cluster
    
    # compute, compare and categorize each data set based on distacne between each data set with centroid
    def dataProcess(self,k):
        # for each set of dataMaps and centorid, measure Euclidean distance, O(n)
        for i in range(len(self.dataMaps)):
            compares = []
            # dX and dY are the x and y distacne for each set
            dX = self.dataMaps.loc[i]['x']
            dY = self.dataMaps.loc[i]['y']
            # loop for all centroids in the lis, O(5) 
            for j in range(k):
                cX = self.centroid.loc[j]['x']
                cY = self.centroid.loc[j]['y']
                # caluate the distance using dX,dY,cX and xY
                a = self.getDistance(dX,dY,cX,cY)
                # add each distance into a compare list
                compares.append(a)
            #find smallest distance and add to corresponding list
            self.cluster[compares.index(min(compares))].append((dX,dY))
        return self.cluster

    # update and re-calcuate the centroids
    def updateCentroid(self,k):
        # check each centorid and update only if its corresponding list contain data
        for i in range(len(self.centroid)):
            temp = pd.DataFrame(self.cluster[i], columns = ['x','y'])
            # check if the corresponding list is not empty
            if len(temp['x']) != 0 or len(temp['y']) != 0:
                # update x and y cooridate of the centroid by average all element in the list
                self.centroid.loc[i]['x'] = temp['x'].sum()/len(temp['x'])
                self.centroid.loc[i]['y'] = temp['y'].sum()/len(temp['y'])
            # graphically show the updateing progress
            self.scatterPlot(k)
                
    # calculate Euclidean distance between centroid and data point
    def getDistance(self, dX,dY,cX,cY): 
        return math.sqrt(math.pow((dX - cX), 2) + math.pow((dY - cY), 2))
    
    # process and calculate KMeans
    def KMeansTest(self):
        # get k value
        k = self.getKValue()
        # check if data file has been imported
        if len(self.dataMaps) == 0:
            messagebox.showerror ("error","please import data")
        else:
            try:
                # convert k into integer and ignore conversion if user entered a non-numerical value 
                k = int(k)
            except ValueError:
                pass
            # check if user entered a non-numerical value, less than or equal to 0 or greater than 6.
            if type(k) == str or int(k) <= 0 or int(k) > 6:
                messagebox.showerror("erorr","K has to be an integer between 1-6")
            # if k is 1, display dataset withtout process
            elif k == 1:
                plt.clf() # clear graph
                plt.scatter(self.dataMaps["x"],self.dataMaps["y"]) # plot all data point
                self.canvas.draw() # display the scatter plot
            else:
                self.initCentroid(k)  
                self.initClusters(k)
                converge = False
                while converge == False:
                    self.initClusters(k)
                    # making a copy of the centroid
                    oldCentroid = self.centroid.copy()
                    # process the data by adding data into list corresponding to its centroid
                    self.dataProcess(k)
                    self.updateCentroid(k)
                    converge = True
                    # compair old centroid with updated centorid, if not equal continue process data and update centorid
                    if oldCentroid.equals(self.centroid) != True:
                        converge = False
    
    # plot the data point and centroid with color and display the result
    def scatterPlot(self,k):
        # pre-define color
        color = ['red','green','grey','blue','purple','black']
        # clear graph
        plt.clf() 
        m = 0
        # plot centroids and clusteres
        while m < k:
            plt.scatter( self.centroid["x"][m], self.centroid["y"][m],s = 150, c= (color[m]), marker = "+")
            plt.scatter([i[0] for i in self.cluster[m]], [i[1] for i in self.cluster[m]], c =(color[m]))
            m = m + 1
        self.canvas.draw() #display graph

c = Kmeans(Tk())
c.mainloop()