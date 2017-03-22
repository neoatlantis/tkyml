#!/usr/bin/env python3


import os
import sys

from tkyml import TKYML
from tkinter import *


if(len(sys.argv) < 2):
    print("Usage: python3 demo.py <foobar.yaml>")
    exit()

filename = sys.argv[1]
data = open(filename, 'r').read()


root = Tk()

frame = TKYML(root, data)
frame.pack()

frame.cmdConfirm_click = lambda e: exit()

root.mainloop()
