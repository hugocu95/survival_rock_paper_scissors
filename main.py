"""Simulator of rock, paper and scizors
"""

import numpy as np
import tkinter as tk
from lib.RPS import RPS

NR_ELEMENTS = 20

def main():
    
    list_elements = NR_ELEMENTS*[None]
    
    breakpoint()
    
    for i in range(NR_ELEMENTS):
        list_elements[i] = RPS()
    
    breakpoint()
    
    print("end of main")
if __name__ == "__main__":
    main()
    