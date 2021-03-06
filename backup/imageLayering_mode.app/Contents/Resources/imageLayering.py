import cv2
import glob, os
import numpy
from blend_modes import normal
from blend_modes import lighten_only
from blend_modes import soft_light
from blend_modes import dodge
from blend_modes import addition
from blend_modes import darken_only
from blend_modes import multiply
from blend_modes import hard_light
from blend_modes import difference
from blend_modes import subtract
from blend_modes import grain_extract
from blend_modes import grain_merge
from blend_modes import divide
from blend_modes import overlay
from blend_modes import screen
from blend_modes import normal

from tkinter import *
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from PIL import Image, ImageTk
import threading

import gc

exit_event = threading.Event()

fileName = 'Null'
done = False

offset = 100
transparency = 0.1
quality_option = ""
blendmode = ""

def browseFiles():
    global fileName
    #fileName = filedialog.askopenfilename(initialdir="/",title="select movie file",filetypes=[("ALL FILES","*.*"),("video file","*.py"),])
    fileName = filedialog.askopenfilename(title="select movie file")
    fileName_label.configure(text=fileName)

def browseDirectory():
    global dirName
    dirName = filedialog.askdirectory(title="select Directory")
    dirName_label.configure(text=dirName)

def startProgram():
    global offset
    global transparency
    global blendmode
    global outputName
    global quality_option
    #offset = int(input_offset.get())
    transparency = float(input_transparent.get())
    quality_option = str(input_quality.get())
    blendmode = str(input_mode.get())
    outputName = str(input_outputName.get())


    if(fileName!='Null'):
        #button_explore.place_forget()
        x = threading.Thread(target=processImage, args=())
        x.daemon=True
        x.start()
        #x.join()
    else:
        print('false')

def stopProgram():
    exit_event.set()

def savingPhoto():
    print('saved')

def exporting(output,quality_option,dirName,outputName,index):
    if(quality_option=='Fast'):
        #print('Fast')
        output.save(dirName+'/'+outputName+'/'+'frame'+str(index)+'.jpg',quality='low',subsampling=2)
    elif(quality_option=='Default_JPG'):
        #print('Default')
        output.save(dirName+'/'+outputName+'/'+'frame'+str(index)+'.jpg',dpi=[72,72],quality='web_maximum',subsampling=0)
    elif(quality_option=='Default_PNG'):
        #print('Default')
        output.save(dirName+'/'+outputName+'/'+'frame'+str(index)+'.png',dpi=[72,72])
    elif(quality_option=='Original_JPG'):
        #print('High')
        output.save(dirName+'/'+outputName+'/'+'frame'+str(index)+'.jpg',dpi=[150,150],quality='web_maximum',subsampling=0)
    elif(quality_option=='Original_PNG'):
        #print('Original')
        output.save(dirName+'/'+outputName+'/'+'frame'+str(index)+'.png',dpi=[150,150])
    else:
        output.save(dirName+'/'+outputName+'/'+'frame'+str(index)+'.jpg',dpi=[72,72])


def processImage():
    global fileName
    global exit_event
    global done
    global img_size_opacity
    global dirName
    global outputName
    global startNum
    global quality_option
    global blendmode
    global transparency
    #img_queue = []

    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    if(dirName == 'Null'):
        dirName = uppath(fileName,1)
    if not os.path.exists(dirName+'/'+outputName):
        os.makedirs(dirName+'/'+outputName)

    index = 0
    vidcap = cv2.VideoCapture(fileName)
    #success, image = vidcap.read()
    ret, frame = vidcap.read()

    img_base = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img_base[:, :, 3] = 255.
    img_base_float = img_base.astype(numpy.float32)
    img_base = numpy.uint8(img_base_float)
    img_base_raw = Image.fromarray(img_base)
    output = Image.new("RGB",img_base_raw.size,(255,255,255,255))
    output.paste(img_base_raw)
    count_label.configure(text="Image: "+str(index))

    #img_queue.append(img_base_float)
    #show image
    #img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
    #canvas.create_image(200,100,image=img,anchor=NW)
    exporting(output,quality_option,dirName,outputName,index)

    img_trans = Image.fromarray(img_base)
    img_trans_float = img_base_float

    while True:
        print("processing image:"+str(index))
        index +=1
        ret, frame=vidcap.read()

        #Ending last photo without blending
        #Ending photos, poping queue


        #normal execution
        if ret:
            img_layer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img_layer[:, :, 3] = 255.
            img_layer_float = img_layer.astype(numpy.float32)
            #add to array
            #img_queue.append(img_layer_float)

            #change modes
            if(blendmode=='soft_light'):
                img_blend_float = soft_light(img_base_float,img_layer_float,transparency)
            elif(blendmode=='lighten_only'):
                img_blend_float = lighten_only(img_base_float,img_layer_float,transparency)
            elif(blendmode=='dodge'):
                img_blend_float = dodge(img_base_float,img_layer_float,transparency)
            elif(blendmode=='addition'):
                img_blend_float = addition(img_base_float,img_layer_float,transparency)
            elif(blendmode=='darken_only'):
                img_blend_float = darken_only(img_base_float,img_layer_float,transparency)
            elif(blendmode=='multiply'):
                img_blend_float = multiply(img_base_float,img_layer_float,transparency)
            elif(blendmode=='hard_light'):
                img_blend_float = hard_light(img_base_float,img_layer_float,transparency)
            elif(blendmode=='difference'):
                img_blend_float = difference(img_base_float,img_layer_float,transparency)
            elif(blendmode=='subtract'):
                img_blend_float = subtract(img_base_float,img_layer_float,transparency)
            elif(blendmode=='grain_extract'):
                img_blend_float = grain_extract(img_base_float,img_layer_float,transparency)
            elif(blendmode=='grain_merge'):
                img_blend_float = grain_merge(img_base_float,img_layer_float,transparency)
            elif(blendmode=='divide'):
                img_blend_float = divide(img_base_float,img_layer_float,transparency)
            elif(blendmode=='overlay'):
                img_blend_float = overlay(img_base_float,img_layer_float,transparency)
            elif(blendmode=='screen'):
                img_blend_float = screen(img_base_float,img_layer_float,transparency)
            elif(blendmode=='normal'):
                img_blend_float = normal(img_base_float,img_layer_float,transparency)
            else:
                img_blend_float = normal(img_base_float,img_layer_float,transparency)

            #img_blend_float = lighten_only(img_base_float,img_layer_float,0.5)
            img_blend = numpy.uint8(img_blend_float)
            img_blend_raw=Image.fromarray(img_blend)

            #counter
            count_label.configure(text="Image: "+str(index))

            output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
            output.paste(img_blend_raw)
            exporting(output,quality_option,dirName,outputName,index)

            #reset base
            img_base_float = img_blend_float
            if(index%30==0):
                gc.collect()

            #show Image
            #img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
            #canvas.create_image(200,100,image=output,anchor=NW)
        else:
            count_label.configure(text="End")

        if exit_event.is_set():
            index = 0
            #output = Image.new("RGB",img_trans.size,(255,255,255,255))
            #output.paste(img_trans)
            #img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
            #canvas.create_image(200,100,image=img,anchor=NW)
            count_label.configure(text="Image: "+str(index))
            exit_event.clear()
            break
    done = True


root = Tk()
root.title('image layering')

canvas = Canvas(root,width=400,height=800)
canvas.pack()


input_offset = tk.StringVar(root)
input_transparent = tk.StringVar(root)
input_quality = tk.StringVar(root)
input_outputName = tk.StringVar(root)
input_restart = tk.StringVar(root)

input_mode = tk.StringVar(root)


button_explore_label = Label(root,text="???????????????")
button_explore_label.place(x=8,y=20)
button_explore = Button(root,width=10,text="select File",command=browseFiles)
button_explore.place(x=6,y=45)

fileName_label = Label(root,text="")
fileName_label.place(x=8,y=70)

button_dir_explore_label = Label(root,text="?????????????????????")
button_dir_explore_label.place(x=8,y=120)
button_dir_explore = Button(root,width=10,text="select Dir",command=browseDirectory)
button_dir_explore.place(x=6,y=145)
dirName_label = Label(root,text="")
dirName_label.place(x=8,y=170)


outputName_label = Label(root,text="?????????????????????")
outputName_label.place(x=8,y=220)
outputName_input = Entry(root,width=20, textvariable=input_outputName)
outputName_input.insert(20,'images')
outputName_input.place(x=8,y=240)





#offset_label = Label(root,text="????????????")
#offset_label.place(x=8,y=80)
#offset_input = Entry(root,width=10, textvariable=input_offset)
#offset_input.insert(10,60)
#offset_input.place(x=10,y=100)

transparent_label = Label(root,text="???????????? (0.00 ~ 1.00)")
transparent_label.place(x=8,y=300)
transparent_input = Entry(root,width=10,textvariable=input_transparent)
transparent_input.insert(10,0.5)
transparent_input.place(x=8,y=320)

mode_label = Label(root,text="????????????")
mode_label.place(x=8,y=360)
mode_input = ttk.Combobox(root, width = 10, textvariable = input_mode)
mode_input['values'] = ('soft_light',
                          'lighten_only',
                          'dodge',
                          'addition',
                          'darken_only',
                          'multiply',
                          'hard_light',
                          'difference',
                          'subtract',
                          'grain_extract',
                          'grain_merge',
                          'divide',
                          'overlay',
                          'screen',
                          'normal',
                          )
mode_input.place(x=8,y=380)
mode_input.current(0)

quality_label = Label(root,text="????????????")
quality_label.place(x=8,y=420)
quality_label_selection = Label(root,text="Fast:????????????  Default:?????????72dpi  Original:?????????150dpi")
quality_label_selection.place(x=8,y=440)

quality_input = ttk.Combobox(root, width = 10, textvariable = input_quality)
quality_input['values'] = ('Fast',
                          'Default_JPG',
                          'Default_PNG',
                          'Original_JPG',
                          'Original_PNG',
                          )
quality_input.place(x=8,y=470)
quality_input.current(0)

button_start = Button(root,width=10,text="Start",command=startProgram)
button_start.place(x=8,y=520)

count_label = Label(root,text="")
count_label.place(x=8,y=550)

button_stop = Button(root,width=10,text="Stop",command=stopProgram)
button_stop.place(x=8,y=580)

#base_img_float = base_img.astype(float)
root = mainloop()

if done == True:
    sys.exit()
