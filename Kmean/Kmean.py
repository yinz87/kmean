# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 23:44:05 2018

@author: yinz
"""
import math
from pylab import *
import numpy
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Centroids:
    def __init__(self):
        self.centroid = ""
        
    def getCentroids(self,k,xmax,xmin,ymax,ymin):
        validated = False
        while validated == False:
            self.centroid = ""
            conditionCheck = []
            initialx = numpy.random.uniform(low = xmin, high = xmax, size = k)
            initialy = numpy.random.uniform(low = ymin, high = ymax, size = k)
            for i in range (k):
                for j in range (i+1,k):            
                    distance = math.sqrt(math.pow((initialx[i] - initialx[j]), 2) + math.pow((initialy[i] - initialy[j]), 2))
                    conditionCheck.append(distance)
            validated = True
            for i in (conditionCheck):
                if i < 0.5:
                    validated = False
        self.centroid = pd.DataFrame({"x":initialx, "y":initialy})
        return self.centroid 

class Kmeans(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.master = master
        self.dataMaps = ""
        self.dataPath = "null"
        self.centroid = []
        self.k = 0
        self.cluster = []
        self.findPath = Button(master, text = "open data file", width = 50, command = self.KMeanTest)
        self.findPath.grid(sticky = "w")
        
        Label(master, text = "kValue").grid(row = 0, column = 0)
        self.kValue = Entry(master, width = 20) # word text box for seraching single word
        self.kValue.grid(row = 1, column = 0)

        fig=plt.figure(figsize=(16,8))
        self.canvas=FigureCanvasTkAgg(fig,master)
        self.canvas.get_tk_widget().grid()
        self.canvas.show()
        
    def getKValue(self):
        self.k = self.kValue.get().strip()
        if len(self.k) == 0:
            self.k = 0
        self.k = int(self.k)
        if self.k <= 0:
            messagebox.showerror("error", "please enter a non-zero postive integer from 1-6\ntry again")
        if self.k > 6:
            messagebox.showerror("error", "please choose k between 1-6")
        return self.k

    def getDataLoc(self):
        self.dataPath = filedialog.askopenfilename(filetypes = [("csv file","*.csv")])
        self.dataPath = self.dataPath.replace("/","\\\\")
        return self.dataPath
    
    def importData(self):
        self.dataMaps = []
        try:    
            self.dataMaps = pd.read_csv(self.getDataLoc())
            self.dataMaps.columns = ['x','y']
            return self.dataMaps
        except FileNotFoundError:
            messagebox.showerror ("Error", "import data again")
        except TypeError:
            messagebox.showerror ("Error", "wrong data file, import data again")

    def initCentroid(self):
        xmax = max(self.dataMaps["x"])
        ymax = max(self.dataMaps["y"])
        xmin = min(self.dataMaps["x"])
        ymin = min(self.dataMaps["y"])
        self.centroid = Centroids.getCentroids(self,self.k,xmax,xmin,ymax,ymin)
        self.centroid = self.centroid.round(1)
        return self.centroid

    def initClusters(self):
        self.cluster =[]
        for i in range(self.k):
            self.cluster.append([])
        return self.cluster

    def dataProcess(self):
        for i in range(len(self.dataMaps)):
            compares = []
            dX = self.dataMaps.loc[i]['x']
            dY = self.dataMaps.loc[i]['y']
            for j in range(self.k):
                cX = self.centroid.loc[j]['x']
                cY = self.centroid.loc[j]['y']
                a = self.getDistance(dX,dY,cX,cY)
                compares.append(a)
            self.cluster[compares.index(min(compares))].append((dX,dY))
        return

    def updateCentroid(self):
        # sum of column / total 
        for i in range(len(self.centroid)):
            temp = pd.DataFrame(self.cluster[i], columns = ['x','y'])
            if len(temp['x']) != 0 or len(temp['y']) != 0:
                self.centroid.loc[i]['x'] = temp['x'].sum()/len(temp['x'])
                self.centroid.loc[i]['y'] = temp['y'].sum()/len(temp['y'])
                
    def getDistance(self, dX,dY,cX,cY): 
        return math.sqrt(math.pow((dX - cX), 2) + math.pow((dY - cY), 2))
    
    def KMeanTest(self):
        try:
            # get data from data file
            self.importData()
            # get K value
            self.getKValue()
            # random generate centroid
            self.initCentroid()
            self.initClusters()
            steady = False
            while steady == False:
                self.initClusters()
                oldCentroid = self.centroid.copy()
                self.dataProcess()
                self.updateCentroid()
                steady = True
                if oldCentroid.equals(self.centroid) != True:
                    steady = False
            self.scatterPlot()
        except TypeError:
            pass
        except ValueError:
            pass
        
    def scatterPlot(self):
        color = ['red','green','grey','blue','purple','black']
        plt.clf()
        self.canvas.draw()
        m = 0
        while m < self.k:
            plt.scatter( self.centroid["x"][m], self.centroid["y"][m],s = 100, c= (color[m]), marker = "+")
            plt.scatter([i[0] for i in self.cluster[m]], [i[1] for i in self.cluster[m]], c =(color[m]))
            m = m + 1
        self.canvas.draw()

c = Kmeans(Tk())
c.mainloop()