import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt, animation
import numpy as np
import random
from datetime import datetime, timedelta
from matplotlib.ticker import AutoLocator
import pandas as pd
import os

class DuplicatedFigure:
    def __init__(self, master):
        self.fig = plt.Figure(dpi=100)
        self.ax = self.fig.add_subplot(xlim=(0, 120), ylim=(2, 8))
        self.ax.grid()
        self.line, = self.ax.plot([], [], lw=1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        #variable
        self.group = 1
        self.interval_check = 100
        self.index = 0
        self.active = 1
        self.phase = "00"
        self.column = "Tx_power"
        self.fname = 'data.csv'
        #config animation
        self.Frame = 25
        self.bound = 30

        self.init_phase = "00"
        master.after(self.interval_check, self.graph)
    
    def map2time(self,start_x, cur_x):
        result = []
        current_datetime = datetime.strptime(start_x[:8], "%H:%M:%S")
        for i in range(len(cur_x)):
            new_datetime = current_datetime + timedelta(seconds=cur_x[i]*self.group)
            new_time_str = new_datetime.strftime("%H:%M:%S")
            result.append(new_time_str)
        return result
    
    def time2int(self,time):
        time_object = datetime.strptime(time, "%H:%M:%S")
        total_seconds = time_object.hour * 3600 + time_object.minute * 60 + time_object.second
        return total_seconds
    
    def change_bound(self):
        self.n = int(self.data_length/(self.bound*self.group))+1
        self.ax.set_xlim(self.bound * (self.n-1) - self.bound, self.bound * self.n)
        self.ax.xaxis.set_major_locator(AutoLocator())
        cur_x = self.ax.get_xticks()
        map_time = self.map2time(self.start_time,cur_x)
        self.ax.set_xticks(cur_x, map_time)
        self.canvas.draw()
    
    def graph(self):
        if self.init_phase == "11" :
            if os.path.getmtime(self.fname) != self.lastmod :
                self.lastmod = os.path.getmtime(self.fname)
                data = pd.read_csv(self.fname)
                new_data_length = len(data)
                #buildgraph
                for i in range(new_data_length-self.data_length) :
                    i += self.data_length
                    dataTime = data["Time"][i]
                    dataColumn = data[self.column][i]
                    Condition = type(dataTime) == type("")
                    Count = i % self.group
                    if Condition :
                        self.sum_y += dataColumn
                    if Count == 0 :
                        if self.sum_y == 0 :
                            self.x.append(self.size_x)
                            self.y.append(None)
                            self.size_x += 1
                            self.sum_y = 0
                        else :
                            result = dataColumn
                            self.x.append(self.size_x)
                            self.y.append(result)
                            self.size_x += 1
                            #scale_y
                            if result > self.max_y : self.max_y = result 
                            elif result < self.min_y : self.min_y = result
                            self.sum_y = dataColumn
                    elif type(dataTime) == type("") :
                        if Condition :
                            result = self.sum_y/(Count+1)
                            self.y[-1] = result
                            #scale_y
                            if result > self.max_y : self.max_y = result 
                            elif result < self.min_y : self.min_y = result
                empty_bound = (self.max_y-self.min_y)/2
                self.ax.set_ylim(self.min_y-empty_bound, self.max_y+empty_bound)
                self.data_length = new_data_length
                #changeframe
                if self.data_length > self.n*self.bound*self.group :
                    self.change_bound()
                #draw
                self.line.set_data(self.x,self.y)
                self.canvas.draw()

        elif self.init_phase == "00" :
            if os.path.isfile(self.fname) :
                self.init_phase = "01"
        elif self.init_phase == "01" :
            data = pd.read_csv(self.fname)
            self.data_length = len(data)
            self.x = []
            self.y = []
            self.sum_y = 0
            self.size_x = 1
            #setbound
            self.n = int(self.data_length/self.bound)+1
            self.ax.set_xlim(self.bound * (self.n-1) - self.bound, self.bound * self.n)
            cur_x = self.ax.get_xticks()
            self.start_time = data["Time"][0]
            map_time = self.map2time(self.start_time,cur_x)
            self.ax.set_xticks(cur_x, map_time)
            self.max_y = 0
            self.min_y = 10000
            self.x.append(0)
            self.y.append(data[self.column][0])
            #buildgraph
            for i in range(0,self.data_length) :
                dataTime = data["Time"][i]
                dataColumn = data[self.column][i]
                Condition = type(dataTime) == type("")
                Count = i % self.group
                if Condition :
                    self.sum_y += dataColumn
                if Count == 0 :
                    if self.sum_y == 0 :
                        self.x.append(self.size_x)
                        self.y.append(None)
                        self.size_x += 1
                        self.sum_y = 0
                    else :
                        result = dataColumn
                        self.x.append(self.size_x)
                        self.y.append(result)
                        self.size_x += 1
                        #scale_y
                        if result > self.max_y : self.max_y = result 
                        elif result < self.min_y : self.min_y = result
                        self.sum_y = dataColumn
                elif type(dataTime) == type("") :
                    if Condition :
                        result = self.sum_y/(Count+1)
                        self.y[-1] = result
                        #scale_y
                        if result > self.max_y : self.max_y = result 
                        elif result < self.min_y : self.min_y = result
            print(self.x,self.y)
            empty_bound = (self.max_y-self.min_y)/2
            self.ax.set_ylim(self.min_y-empty_bound, self.max_y+empty_bound)
            #draw
            self.line.set_data(self.x,self.y)
            self.canvas.draw()
            self.init_phase = "11"
            self.lastmod = os.path.getmtime(self.fname)
            print(self.lastmod)
        if self.active :
            root.after(self.interval_check, self.graph)
        else :
            return

# Main Application
plt.rcParams["figure.figsize"] = [7.00, 3.50]
root = tkinter.Tk()
root.wm_title("Embedding in Tk")


duplicate_figure = DuplicatedFigure(master=root)
button = tkinter.Button(master=root, text="Quit")
button.pack()

tkinter.mainloop()
