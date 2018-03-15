# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 23:44:05 2018

@author: yinz
"""
import math
from pylab import *
import numpy
import pandas as pd
from tkinter import filedialog
from tkinter import *
from matplotlib import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Centroids:
    def __init__(self):
        self.centroid = ""
        
    def getCentroids(self, xmax,xmin,ymax,ymin):
        self.centroid = ""
        distAtoB = 0
        distAtoC = 0
        distBtoC = 0
        while distAtoB < 1 or distAtoC < 1 or distBtoC < 1:
            initialx = numpy.random.uniform(low = xmin, high = xmax,size = 3)
            initialy = numpy.random.uniform(low = ymin, high = ymax, size = 3)
            distAtoB = math.sqrt(math.pow((initialx[0] - initialx[1]), 2) + math.pow((initialy[0] - initialy[1]), 2))
            distAtoC = math.sqrt(math.pow((initialx[0] - initialx[2]), 2) + math.pow((initialy[0] - initialy[2]), 2))
            distBtoC = math.sqrt(math.pow((initialx[1] - initialx[2]), 2) + math.pow((initialy[1] - initialy[2]), 2))
        self.centroid = pd.DataFrame({"x":initialx, "y":initialy})
        return self.centroid 

class Kmeans(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.master = master
        self.dataMaps = ""
        self.dataPath = "null"
        self.centroid = []
        self.color = ["red","green","blue"]
        self.findPath = Button(master, text = "open data file", width = 20, command = self.KMeanTest)
        self.findPath.grid()
        self.cluster0 = []
        self.cluster1 = []
        self.cluster2 = []
        fig=plt.figure(figsize=(16,8))
        self.canvas=FigureCanvasTkAgg(fig,master)
        self.canvas.get_tk_widget().grid()
        self.canvas.show()

    def getDataLoc(self):
        self.dataPath = filedialog.askopenfilename(filetypes = [("csv file","*.csv")])
        self.dataPath = self.dataPath.replace("/","\\\\")
        return self.dataPath
    
    def importData(self):
        try:    
            self.dataMaps = pd.read_csv(self.getDataLoc())
            self.dataMaps.columns = ['x','y']
            return self.dataMaps
        except FileNotFoundError:
            print ("import file again")

    def initCentroid(self):
        xmax = max(self.dataMaps["x"])
        ymax = max(self.dataMaps["y"])
        xmin = min(self.dataMaps["x"])
        ymin = min(self.dataMaps["y"])
        self.centroid = Centroids.getCentroids(self,xmax,xmin,ymax,ymin)
        self.centroid = self.centroid.round(1)
        return self.centroid

    def dataProcess(self):
        self.cluster0 = []
        self.cluster1 = []
        self.cluster2 = []
        for i in range(len(self.dataMaps)):
            compares = []
            dX = self.dataMaps.loc[i]['x']
            dY = self.dataMaps.loc[i]['y']
            for j in range(3):
                cX = self.centroid.loc[j]['x']
                cY = self.centroid.loc[j]['y']
                a = self.getDistance(dX,dY,cX,cY)
                compares.append(a)
            name = "cluster" + str(compares.index(max(compares)))
            getattr(self,name).append((dX,dY))
        self.cluster0 = pd.DataFrame(self.cluster0, columns = ['x','y'])
        self.cluster1 = pd.DataFrame(self.cluster1, columns = ['x','y'])        
        self.cluster2 = pd.DataFrame(self.cluster2, columns = ['x','y'])
        return

    def updateCentroid(self):
        # sum of column / total 
        for i in range(len(self.centroid)):
            name = "cluster" + str(i)
            temp = getattr(self,name)
            if len(temp['x']) != 0 and len(temp['y']) != 0:
                self.centroid.loc[i]['x'] = temp['x'].sum()/len(temp['x'])
                self.centroid.loc[i]['y'] = temp['y'].sum()/len(temp['y'])

    def getDistance(self, dX,dY,cX,cY): 
        return math.sqrt(math.pow((dX - cX), 2) + math.pow((dY - cY), 2))
    
    def KMeanTest(self):
        self.importData()
        self.initCentroid()
        #print (self.centroid)
        steady = False
        while steady == False:
            oldCentroid = self.centroid.copy()
            #print (oldCentroid)
            self.dataProcess()
            self.updateCentroid()
            steady = True
            if (oldCentroid.equals(self.centroid)) == True:
                #print (oldCentroid)
                #print (self.centroid)
                print ("done")
                return False
#pd.DataFrame.plot(kind = "scatter", x = ["sepal_width"], y  = maps["petal_width"])
#scatter(maps["sepal_width"], maps["petal_width"],s = 1)
#scatter(maps["sepal_width"], maps["petal_width"],s = 1, c = 'red')
#scatter(maps["sepal_width"], maps["petal_width"],s = 1)

#print (maps.loc[[1]])
c = Kmeans(Tk())
c.mainloop()


# =============================================================================
#         #print (self.cetnroids["sepal_width"])
#        # plt.clf()
#        # self.canvas.draw()
#       #  m = 0
#        # while m < 3:  
#       #      plt.scatter( self.centroid["x"][m], self.centroid["y"][m],s = 50, c= (self.color[m]), marker = "+")
#      #       m = m + 1
#      #   plt.scatter( self.dataMaps["x"], self.dataMaps["y"],s = 5, c = ("black"))
#        # self.canvas.draw()
#         #pd.DataFrame.plot(kind = "scater", x =self.cetnroids["sepal_width"], y = self.cetnroids["petal_width"]
# =============================================================================