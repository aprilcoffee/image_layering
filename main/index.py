import gc
import time
import glob, os
import threading

from tkinter import *
import tkinter as tk
from tkinter import ttk
import threading



root = Tk()
root.title('圖片疊加軟體')

window_height = 200
window_width = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
canvas = Canvas(root,width=200,height=200)

cwd = os.getcwd()
print(os.getcwd)

def execModes():
    #exec(open('version_modes/imageLayering.py').read())
    os.system('open imageLayering_mode.app')

def execCv2():
    #exec(open('version_cv2/imageLayering.py').read())
    os.system('open imageLayering_cv2.app')

def execRealtime():
    #exec(open('version_realtime/imageLayering.py').read())
    os.system('open imageLayering_realtime.app')

root.configure(bg="black")

#test = Button(root,width=50, text =cwd, command = execModes)

B_mode = Button(root,width=12, text ="濾鏡多模式疊圖", command = execModes)
B_cv2 = Button(root,width=12, text ="圖片亮度疊加", command = execCv2)
B_realtime = Button(root,width=12, text ="疊圖即時監控", command = execRealtime)
B_mode.place(x=45,y=40)
B_cv2.place(x=45,y=90)
B_realtime.place(x=45,y=140)
#test.place(x=45,y=10)

root = mainloop()
