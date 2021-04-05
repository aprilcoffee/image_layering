import cv2
import glob, os
import numpy
from blend_modes import normal
from blend_modes import lighten_only

from tkinter import *
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from PIL import Image, ImageTk
import threading

exit_event = threading.Event()

fileName = 'Null'
done = False

#init random image
output = numpy.random.randint(0,256,(480,640,3), dtype=numpy.uint8)

#offset = 100
#transparency = 0.1
quality_option = ""

def browseCam():
    global fileName

def savePhoto():
    global output
def startProgram():
	x = threading.Thread(target=processImage, args=())
	x.daemon=True
	x.start()

def restartProgram():
	exit_event.set()

def processImage():
	global fileName
	global exit_event
	global done
	print('start processing')
	new = False
	vidcap = cv2.VideoCapture(0)
	while (vidcap.isOpened()):
		ret, frame=vidcap.read()
		if (new == False):
			img_base = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
			img_base[:, :, 3] = 255.
			img_base_float = img_base.astype(numpy.float32)
			img_base = numpy.uint8(img_base_float)
			img_base_raw = Image.fromarray(img_base)
			new = True
		cv2.waitKey(100)&0xFF
		img_layer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		img_layer[:, :, 3] = 255
		img_layer_float = img_layer.astype(numpy.float32)
		img_blend_float = lighten_only(img_base_float,img_layer_float,0.5)
		img_blend = numpy.uint8(img_blend_float)
		img_blend_raw=Image.fromarray(img_blend)
		output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
		output.paste(img_blend_raw)
		img_base_float = img_blend_float
		img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
		canvas.create_image(200,100,image=output,anchor=NW)
		if (exit_event.is_set()):
			vidcap.release()
			exit_event.clear()
			break
	done = True

root = Tk()
root.title('image layering')

canvas = Canvas(root,width=1000,height=700)
canvas.pack()

button_explore = Button(root,width=10,text="select File",command=browseCam)
button_explore.place(x=8,y=15)

camName_label = Label(root,text="")
camName_label.place(x=8,y=40)

#input_offset = tk.StringVar(root)
#input_transparent = tk.StringVar(root)
#input_quality = tk.StringVar()

#offset_label = Label(root,text="疊加層數")
#offset_label.place(x=8,y=80)
#offset_input = Entry(root,width=10, textvariable=input_offset)
#offset_input.insert(10,60)
#offset_input.place(x=10,y=100)

#transparent_label = Label(root,text="漸層程度 (0.00 ~ 1.00)")
#transparent_label.place(x=8,y=140)
#transparent_input = Entry(root,width=10,textvariable=input_transparent)
#transparent_input.insert(10,0.1)
#transparent_input.place(x=8,y=160)

#quality_label = Label(root,text="輸出品質")
#quality_label_selection = Label(root,text="F:快速 D:一般 H:高解析 O:原檔")
#quality_label.place(x=8,y=200)
#quality_label_selection.place(x=8,y=220)

#quality_input = ttk.Combobox(root, width = 10, textvariable = input_quality)
#quality_input['values'] = ('Fast',
#                          'Default',
#                          'High',
#                          'Original',
#                          )
#quality_input.place(x=8,y=240)
#quality_input.current(0)

button_start = Button(root,width=10,text="Start",command=startProgram)
button_start.place(x=8,y=300)

#count_label = Label(root,text="")
#count_label.place(x=8,y=330)


#button_save = Button(root,width=10,text="Save",command=savePhoto)
#button_save.place(x=8,y=330)

button_stop = Button(root,width=10,text="Restart",command=restartProgram)
button_stop.place(x=8,y=370)

#base_img_float = base_img.astype(float)
root = mainloop()

if done == True:
    sys.exit()
