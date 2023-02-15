from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import numpy as np
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import time
from settings import COLOR_PAPER, COLOR_ROCK, COLOR_SCISSOR, SIZE_BOX, TIMEOUT
    
class Application(tk.Frame):
    def __init__(self,master,initial_state: list,queue):
        master.protocol("WM_DELETE_WINDOW", lambda args=master:self.on_closing(args))
        self.queue = queue
        self.initial_state = initial_state
        self.init_time = time.time()
        tk.Frame.__init__(self,master)
        self.createWidgets(master)
        
        
    def createWidgets(self,master):
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.canvas=FigureCanvasTkAgg(self.fig,master=master)
        self.canvas.get_tk_widget().grid(row=0,column=1)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()
        
        self.first_plot()
        self.update_plot(master)
        
    def first_plot(self):
        self.X = np.zeros(len(self.initial_state))
        self.Y = np.zeros(len(self.initial_state))
        self.color = len(self.initial_state)*["k"]
        self.area = 5*np.ones(len(self.initial_state))
        
        for i in range(len(self.initial_state)):
            self.X[i] = self.initial_state[i]._x
            self.Y[i] = self.initial_state[i]._y
        
            if self.initial_state[i].sort == "r":
                self.color[i] = COLOR_ROCK
            elif self.initial_state[i].sort == "p":
                self.color[i] = COLOR_PAPER
            elif self.initial_state[i].sort == "s":
                self.color[i] = COLOR_SCISSOR

        self.ax.set_xlim([0,SIZE_BOX])
        self.ax.set_ylim([0,SIZE_BOX])                
        self.ax.scatter(self.X,self.Y,s=self.area,c=self.color,alpha=0.9)

        
    def update_plot(self,master):
        #Try to check if there is data in the queue
        try:      
            indx,part=self.queue.get_nowait()
            now = time.time()
            if TIMEOUT > now-self.init_time:
                self.X[indx] = part._x
                self.Y[indx] = part._y
            
                if part.sort == "r":
                    self.color[indx] = COLOR_ROCK
                elif part.sort == "p":
                    self.color[indx] = COLOR_PAPER
                else:
                    self.color[indx] = COLOR_SCISSOR
                
                self.canvas.draw()
                self.ax.clear()
                self.ax.set_title("rock=red, paper=green, scissor=blue")
                self.ax.set_xlim([0,SIZE_BOX])
                self.ax.set_ylim([0,SIZE_BOX])
                self.ax.scatter(self.X,self.Y,s=self.area,c=self.color,alpha=0.7)
                
                master.after(1,lambda arg=master: self.update_plot(arg))
            
            else:
                print(TIMEOUT,now-self.init_time)
                print ('Time elapsed. Killing GUI now')
                master.after(1,lambda:master.quit())
                master.after(1,lambda:master.destroy())

        except:
            master.after(10,lambda arg=master: self.update_plot(arg))

    def on_closing(self,master):
        print("closing GUI")
        master.after(10,lambda:master.quit())
        master.after(10,lambda:master.destroy())
        