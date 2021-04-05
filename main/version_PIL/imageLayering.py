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

offset = 100
transparency = 0.1
quality_option = ""

def browseFiles():
    global fileName
    #fileName = filedialog.askopenfilename(initialdir="/",title="select movie file",filetypes=[("ALL FILES","*.*"),("video file","*.py"),])
    fileName = filedialog.askopenfilename(title="select movie file")
    fileName_label.configure(text="File Opened: "+fileName)

def startProgram():
    global offset
    global transparency

    offset = int(input_offset.get())
    transparency = float(input_transparent.get())
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

def processImage():
    global fileName
    global exit_event


    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    outputDir = uppath(fileName,1)
    if not os.path.exists(outputDir+'/processedImage'):
        os.makedirs(outputDir+'/processedImage')


    global done
    index = 0
    vidcap = cv2.VideoCapture(fileName)
    #success, image = vidcap.read()
    ret, frame = vidcap.read()

    base_img_raw = Image.fromarray(frame)
    base_img_raw.putalpha(255)
    base_img = numpy.array(base_img_raw)
    base_img_float = base_img.astype(float)

    transparent_img_raw = base_img_raw
    transparent_img = base_img
    transparent_img_float = base_img_float


    base_img = numpy.uint8(base_img_float)
    base_img = cv2.cvtColor(base_img, cv2.COLOR_BGR2RGB)
    base_img_raw=Image.fromarray(base_img)
    output = Image.new("RGB",base_img_raw.size,(255,255,255,255))
    output.paste(base_img_raw)
    img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
    canvas.create_image(200,100,image=img,anchor=NW)
    count_label.configure(text="Image: "+str(index))

    if(quality_option=='Fast'):
        output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg',quality='low',subsampling=2)
    elif(quality_option=='Default'):
        output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg')
    elif(quality_option=='High'):
        output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg',quality='maximum',subsampling=0)
    elif(quality_option=='Original'):
        output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg',quality='web_maximum',subsampling=0)
    else:
        output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg')


    while True:
        index +=1

        print("processing image:"+str(index))
        ret, frame=vidcap.read()
        if not ret:
            break

        layer_img_raw = Image.fromarray(frame)
        layer_img_raw.putalpha(255)
        layer_img = numpy.array(layer_img_raw)
        layer_img_float = layer_img.astype(float)

        blend_img_float = lighten_only(base_img_float,layer_img_float,0.5)
        if(index >= offset):
            blend_img_float = normal(blend_img_float,transparent_img_float,transparency)

        blend_img = numpy.uint8(blend_img_float)
        blend_img = cv2.cvtColor(blend_img, cv2.COLOR_BGR2RGB)
        blend_img_raw=Image.fromarray(blend_img)


        output = Image.new("RGB",blend_img_raw.size,(255,255,255,255))
        output.paste(blend_img_raw)
        if(quality_option=='Fast'):
            output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg',quality='low',subsampling=2)
        elif(quality_option=='Default'):
            output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg')
        elif(quality_option=='High'):
            output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg',quality='maximum',subsampling=0)
        elif(quality_option=='Original'):
            output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg',quality='web_maximum',subsampling=0)
        else:
            output.save(outputDir+'/processedImage/frame'+str(index)+'.jpg')

        base_img_float = blend_img_float
        img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
        canvas.create_image(200,100,image=img,anchor=NW)
        count_label.configure(text="Image: "+str(index))


        if exit_event.is_set():
            index = 0
            output = Image.new("RGB",base_img_raw.size,(255,255,255,255))
            output.paste(base_img_raw)
            img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
            canvas.create_image(200,100,image=img,anchor=NW)
            count_label.configure(text="Image: "+str(index))
            exit_event.clear()
            break
    done = True


root = Tk()
root.title('image layering')

canvas = Canvas(root,width=1000,height=700)
canvas.pack()

button_explore = Button(root,width=10,text="select File",command=browseFiles)
button_explore.place(x=8,y=15)

fileName_label = Label(root,text="")
fileName_label.place(x=8,y=40)

input_offset = tk.StringVar(root)
input_transparent = tk.StringVar(root)
input_quality = tk.StringVar()

offset_label = Label(root,text="幾張圖片後開始疊加 (整數)")
offset_label.place(x=8,y=80)
offset_input = Entry(root,width=10, textvariable=input_offset)
offset_input.insert(10,100)
offset_input.place(x=10,y=100)

transparent_label = Label(root,text="漸層程度 (0.00 ~ 1.00)")
transparent_label.place(x=8,y=140)
transparent_input = Entry(root,width=10,textvariable=input_transparent)
transparent_input.insert(10,0.1)
transparent_input.place(x=8,y=160)

quality_label = Label(root,text="輸出品質")
quality_label_selection = Label(root,text="F:快速 D:一般 H:高解析 O:原檔")
quality_label.place(x=8,y=200)
quality_label_selection.place(x=8,y=220)

quality_input = ttk.Combobox(root, width = 10, textvariable = input_quality)
quality_input['values'] = ('Fast',
                          'Default',
                          'High',
                          'Original',
                          )
quality_input.place(x=8,y=240)
quality_input.current(1)

button_start = Button(root,width=10,text="start",command=startProgram)
button_start.place(x=8,y=300)

count_label = Label(root,text="")
count_label.place(x=8,y=330)

button_stop = Button(root,width=10,text="Restart",command=stopProgram)
button_stop.place(x=8,y=370)

#base_img_float = base_img.astype(float)
root = mainloop()

if done == True:
    sys.exit()
