"""Simulator of rock, paper and scizors
"""

import sys
import threading
import queue 
from lib.RPS import HandShape
from lib.mover import Dynamics
from lib.GUI import Application
from settings import NR_ELEMENTS, NR_THREADS

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
    
def main():
    window = tk.Tk()
    queue_data = queue.Queue()
    # Event to join all threads
    stop_event = threading.Event()

    list_elements = NR_ELEMENTS*[None]
    for i in range(NR_ELEMENTS):
        list_elements[i] = HandShape()
    
    # GUI object
    app = Application(window,list_elements,queue_data)

    movers = NR_THREADS*[None]
    for i in range(NR_THREADS):
        movers[i] = Dynamics(list_elements,queue_data,stop_event)
        movers[i].start()
    

    app.mainloop()
    # Event to join all threads is set
    stop_event.set()
    
    for i in range(NR_THREADS):
        movers[i].join()
            
    print("end of main")
    
if __name__ == "__main__":
    main()
    