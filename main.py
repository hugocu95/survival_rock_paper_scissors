"""Simulator of rock, paper and scizors
"""

import sys
import multiprocessing as mp
import numpy as np
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from lib.RPS import RPS
from lib.mover import Dynamics
from lib.GUI import Application
from settings import NR_ELEMENTS, NR_THREADS

def main():
    window = tk.Tk()
    queue = mp.Queue()
    stop_event = threading.Event()

    list_elements = NR_ELEMENTS*[None]  
    for i in range(NR_ELEMENTS):
        list_elements[i] = RPS()

    
    app = Application(window,list_elements,queue)

    Mover = NR_THREADS*[None]
    for i in range(NR_THREADS):
        Mover[i] = Dynamics(list_elements,queue,stop_event)
        Mover[i].start()
    

    app.mainloop()
    stop_event.set()
    for i in range(NR_THREADS):
        Mover[i].join()
        
    print(queue.qsize())
    
    print("end of main")
    
if __name__ == "__main__":
    main()
    