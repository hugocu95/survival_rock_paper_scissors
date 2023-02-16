"""Graphics User Interface for polotting the hand shapes (rock, paper, scissors)
"""
import sys
import time
import queue
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from settings import COLOR_PAPER, COLOR_ROCK, COLOR_SCISSOR, SIZE_BOX, TIMEOUT

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

class Application(tk.Frame):
    """Creates application for plotting hand shapes
    """
    def __init__(self, master: tk.Tk, initial_state:list, queue_data: queue.Queue):
        """Constructor of application

        Args:
            master (tk.Tk): window of tkinter 
            initial_state (list): list of objects of type HandShape
            queue_data (queue.Queue): (index (int), instance of HandShape)
        """
        master.protocol("WM_DELETE_WINDOW", lambda args=master:self.on_closing(args))
        self.queue = queue_data
        self.initial_state = initial_state
        self.indx = []
        self.part = []
        
        # Position, color and area of the hand shapes being plotted
        self.X = np.zeros(len(self.initial_state))
        self.Y = np.zeros(len(self.initial_state))
        self.color = len(self.initial_state)*["k"]
        self.area = 5*np.ones(len(self.initial_state))
        
        self.init_time = time.time()
        tk.Frame.__init__(self,master)
        self.create_widgets(master)
        
        
    def create_widgets(self,master: tk.Tk):
        """Creates canvas and calls update_plot to constantly refresh it

        Args:
            master (tk.Tk): window of tkinter 
        """
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.canvas=FigureCanvasTkAgg(self.fig,master=master)
        self.canvas.get_tk_widget().grid(row=0,column=1)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()
        
        self.first_plot()
        self.update_plot(master)
        
    def first_plot(self):
        """Stores and plots the position and sorts of instances of HandShape
        """
        for i,_ in enumerate(self.initial_state):
            self.X[i], self.Y[i] = self.initial_state[i].position
        
            if self.initial_state[i].sort == "r":
                self.color[i] = COLOR_ROCK
            elif self.initial_state[i].sort == "p":
                self.color[i] = COLOR_PAPER
            elif self.initial_state[i].sort == "s":
                self.color[i] = COLOR_SCISSOR

        self.ax.set_title("rock=red, paper=green, scissor=blue")
        self.ax.set_xlim([0,SIZE_BOX])
        self.ax.set_ylim([0,SIZE_BOX])                
        self.ax.scatter(self.X,self.Y,s=self.area,c=self.color,alpha=0.9)

        
    def update_plot(self,master:tk.Tk):
        """Constantly refreshes the plot of instances of HandShape

        Args:
            master (tk.Tk): window of tkinter
        """
        try:      
            while not self.queue.empty():  
                indx,part=self.queue.get_nowait()
                self.indx.append(indx)
                self.part.append(part)

            now = time.time()
            if TIMEOUT > now-self.init_time:
                for i,_ in enumerate(self.indx):
                    self.X[i], self.Y[i] = self.initial_state[i].position
                
                    if self.part[i].sort == "r":
                        self.color[self.indx[i]] = COLOR_ROCK
                    elif self.part[i].sort == "p":
                        self.color[self.indx[i]] = COLOR_PAPER
                    else:
                        self.color[self.indx[i]] = COLOR_SCISSOR
                        
                self.indx.clear()
                self.part.clear()
                                    
                self.canvas.draw()               
                self.ax.clear()
                
                self.ax.set_title("rock=red, paper=green, scissor=blue")
                self.ax.set_xlim([0,SIZE_BOX])
                self.ax.set_ylim([0,SIZE_BOX])
                
                self.ax.scatter(self.X,self.Y,s=self.area,c=self.color,alpha=0.7)

                master.after(1,lambda arg=master: self.update_plot(arg))
            
            else:
                print ('Time elapsed. Killing GUI now')
                master.after(1,lambda:master.quit())
                master.after(1,lambda:master.destroy())

        except queue.Empty:
            master.after(10,lambda arg=master: self.update_plot(arg))

    def on_closing(self,master: tk.Tk):
        """Ensures a smooth closing of the app if the "X" button for closing is clicked

        Args:
            master (tk.Tk): window of tkinter
        """
        print("closing GUI")
        master.after(10,lambda:master.quit())
        master.after(10,lambda:master.destroy())
        