import cv2
import glob, os
import gc
import numpy as np
#from blend_modes import normal
#from blend_modes import lighten_only

from tkinter import *
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from PIL import Image, ImageTk
import threading

import time

exit_event = threading.Event()

fileName = 'Null'
dirName = 'Null'
outputName = 'processedImage'
done = False

offset = 100
transparency = 0.1
quality_option = ""
mode_option = ""
img_size_opacity = []
startNum = 0

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
    global outputName
    global startNum
    global quality_option
    global mode_option

    #global transparency

    startNum = 0
    offset = int(input_offset.get())
    mode_option = str(input_mode.get())
    outputName = str(input_outputName.get())
    #transparency = float(input_transparent.get())
    quality_option = str(input_quality.get())

    if(fileName!='Null'):
        #button_explore.place_forget()
        x = threading.Thread(target=processImage, args=())
        x.daemon=True
        x.start()
        #x.join()
    else:
        print('false')


def restartProgram():
    global offset
    global outputName
    global startNum
    global quality_option
    global mode_option

    #global transparency
    mode_option = str(input_mode.get())
    startNum = int(input_restart.get())
    offset = int(input_offset.get())
    outputName = str(input_outputName.get())
    #transparency = float(input_transparent.get())
    quality_option = str(input_quality.get())

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
    img_queue = []
    restarting = True;

    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    if(dirName == 'Null'):
        dirName = uppath(fileName,1)
    if not os.path.exists(dirName+'/'+outputName):
        os.makedirs(dirName+'/'+outputName)

    index = 0
    vidcap = cv2.VideoCapture(fileName)
    #success, image = vidcap.read()

    if(startNum!=0 and startNum>=offset and offset!=-1):
        if(offset!=-1):
            restarting = True
            index = startNum-1
            for i in range(startNum-offset):
                ret, frame = vidcap.read()
                #print('hi')
            for i in range(offset):
                ret, frame = vidcap.read()
                #print('hi')
                if(not ret):
                    break
                img_layer_restart = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_base = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #img_layer_restart[:, :, 3] = 255.
                #img_layer_restart_float = img_layer_restart.astype(np.float32)
                #add to array
                if(offset!=-1):
                    img_queue.append(img_layer_restart)

    elif(startNum==0 or offset==-1):
        ret, frame = vidcap.read()
        img_base = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #img_base[:, :, 3] = 255.
        #img_base_float = np.float32(img_base)
        #img_base = np.uint8(img_base_float)
        img_base_raw = Image.fromarray(img_base)
        output = Image.new("RGB",img_base_raw.size)
        output.paste(img_base_raw)
        count_label.configure(text="Image: "+str(index))
        img_queue.append(img_base)
        #show image
        #img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
        #canvas.create_image(200,100,image=img,anchor=NW)

    while True:
        print("processing image:"+str(index))
        index +=1
        ret, frame=vidcap.read()
        if(index%2==0):
            gc.collect()
        #Ending last photo without blending
        if not ret and (len(img_queue) <= 2):
            #last Image
            if(len(img_queue)>1):
                img_queue.pop(0)
            img_blend = img_queue[0]
            #img_blend = np.uint8(img_blend_float)
            img_blend_raw=Image.fromarray(img_blend)
            output = Image.new("RGB",img_blend_raw.size,(255,255,255))
            output.paste(img_blend_raw)
            exporting(output,quality_option,dirName,outputName,index)
            count_label.configure(text="???????????? ?????????: "+str(index))
            break

        #Ending photos, poping queue
        elif not ret:
            img_queue.pop(0)
            #img_temp_base_float = img_queue[0]
            #for i in range(1,len(img_queue)):
            #    img_temp_blend_float = lighten_only(img_temp_base_float,img_queue[i],1)
            #    img_temp_base_float = img_temp_blend_float
            #img_blend_float = img_temp_base_float

            if(mode_option=='lighten_only'):
                img_blend = np.maximum.reduce(img_queue)
            else:
                img_blend = np.minimum.reduce(img_queue)
            #img_blend = np.uint8(img_blend_float)
            img_blend_raw = Image.fromarray(img_blend)
            #counter
            count_label.configure(text="Ending Image: "+str(index))
            output = Image.new("RGB",img_blend_raw.size,(255,255,255))
            output.paste(img_blend_raw)
            exporting(output,quality_option,dirName,outputName,index)
        #normal execution
        else:
            img_layer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #img_layer[:, :, 3] = 255.
            #img_layer_float = np.float32(img_layer)
            if(offset!=-1):
                img_queue.append(img_layer)

            if(index < offset or offset==-1):
                #np.maximum
                if(mode_option=='lighten_only'):
                    img_blend = np.maximum(img_base,img_layer)
                else:
                    img_blend = np.minimum(img_base,img_layer)
                #img_blend_float = lighten_only(img_base_float,img_layer_float,0.5)
            else:
                #start = time.process_time()
                img_queue.pop(0)
                #img_temp_base = []
                #for i in range(0,len(img_queue)):
                #    img_temp_base.append(img_queue[i])
                if(mode_option=='lighten_only'):
                    img_blend = np.maximum.reduce(img_queue)
                else:
                    img_blend = np.minimum.reduce(img_queue)
                #img_temp_base_float = img_queue[0]
                #for i in range(1,len(img_queue)):
                #    img_temp_blend_float = lighten_only(img_temp_base_float,img_queue[i],0.5)
                #    img_temp_base_float = img_temp_blend_float
                #img_blend_float = img_temp_base_float
                #end = time.process_time()
                #print('obo\t'+str(end-start))

            #counter
            count_label.configure(text="Image: "+str(index))

            #cv2.imwrite(dirName+'/'+outputName+'_png/'+'frame'+str(index)+'.png', img_blend, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            #cv2.imwrite(dirName+'/'+outputName+'_jpg/'+'frame'+str(index)+'.jpg', img_blend, [cv2.IMWRITE_JPEG_QUALITY, 100])
            if(index>=startNum):
                img_blend_raw=Image.fromarray(img_blend)
                output = Image.new("RGB",img_blend_raw.size,(255,255,255))
                output.paste(img_blend_raw)
                exporting(output,quality_option,dirName,outputName,index)
            #reset base
            img_base = img_blend
            #show Image
            #img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
            #canvas.create_image(200,100,image=output,anchor=NW)


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

canvas = Canvas(root,width=500,height=800)
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

offset_label = Label(root,text="???????????? (??????-1 ??????fadeout)")
offset_label.place(x=8,y=340)
offset_input = Entry(root,width=10, textvariable=input_offset)
offset_input.insert(10,150)
offset_input.place(x=10,y=360)

#transparent_label = Label(root,text="???????????? (0.00 ~ 1.00)")
#transparent_label.place(x=8,y=140)
#transparent_input = Entry(root,width=10,textvariable=input_transparent)
#transparent_input.insert(10,0.1)
#transparent_input.place(x=8,y=160)

quality_label = Label(root,text="????????????")
quality_label.place(x=8,y=400)
quality_label_selection = Label(root,text="Fast:????????????  Default:?????????72dpi  Original:?????????150dpi")
quality_label_selection.place(x=8,y=420)

quality_input = ttk.Combobox(root, width = 10, textvariable = input_quality)
quality_input['values'] = ('Fast',
                          'Default_JPG',
                          'Default_PNG',
                          'Original_JPG',
                          'Original_PNG',
                          )
quality_input.place(x=8,y=440)
quality_input.current(0)

mode_label = Label(root,text="???????????? (lighten_only, darken_only)")
mode_label.place(x=8,y=470)

mode_input = ttk.Combobox(root, width = 10, textvariable = input_mode)
mode_input['values'] = ('lighten_only',
                        'darken_only',
                        )
mode_input.place(x=8,y=490)
mode_input.current(0)

button_start = Button(root,width=10,text="Start",command=startProgram)
button_start.place(x=8,y=550)

count_label = Label(root,text="")
count_label.place(x=8,y=580)

button_stop = Button(root,width=10,text="Stop",command=stopProgram)
button_stop.place(x=8,y=600)

restart_label = Label(root,text="---------------------------------")
restart_label.place(x=8,y=640)

restart_label = Label(root,text="????????????(?????????)")
restart_label.place(x=8,y=660)
restart_label2 = Label(root,text="????????????????????????: (???????????????????????????)")
restart_label2.place(x=8,y=680)

restart_num_input = Entry(root,width=10, textvariable=input_restart)
restart_num_input.insert(10,1000)
restart_num_input.place(x=8,y=700)
button_restart = Button(root,width=10,text="restart",command=restartProgram)
button_restart.place(x=8,y=760)


#base_img_float = base_img.astype(float)
root = mainloop()

if done == True:
    sys.exit()
