import cv2
import glob, os
import numpy as np
#from blend_modes import normal
#from blend_modes import lighten_only

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
img_size_opacity = []

def _compose_alpha(img_in, img_layer, opacity):
    """Calculate alpha composition ratio between two images.
    """
    #print(img_layer[:, :, 3])
    comp_alpha = np.minimum(img_in[:, :, 3], img_layer[:, :, 3]) * opacity
    new_alpha = img_in[:, :, 3] + (1.0 - img_in[:, :, 3]) * comp_alpha
    np.seterr(divide='ignore', invalid='ignore')
    ratio = comp_alpha / new_alpha
    ratio[ratio == np.NAN] = 0.0
    return ratio

def lighten_only(img_in, img_layer, opacity, disable_type_checks: bool = False):
    """Apply lighten only blending mode of a layer on an image.
    Example:
        .. image:: ../tests/lighten_only.png
            :width: 30%
        ::
            import cv2, numpy
            from blend_modes import lighten_only
            img_in = cv2.imread('./orig.png', -1).astype(float)
            img_layer = cv2.imread('./layer.png', -1).astype(float)
            img_out = lighten_only(img_in,img_layer,0.5)
            cv2.imshow('window', img_out.astype(numpy.uint8))
            cv2.waitKey()
    See Also:
        Find more information on
        `Wikipedia <https://en.wikipedia.org/w/index.php?title=Blend_modes&oldid=747749280#Lighten_Only>`__.
    Args:
      img_in(3-dimensional numpy array of floats (r/g/b/a) in range 0-255.0): Image to be blended upon
      img_layer(3-dimensional numpy array of floats (r/g/b/a) in range 0.0-255.0): Layer to be blended with image
      opacity(float): Desired opacity of layer for blending
      disable_type_checks(bool): Whether type checks within the function should be disabled. Disabling the checks may
        yield a slight performance improvement, but comes at the cost of user experience. If you are certain that
        you are passing in the right arguments, you may set this argument to 'True'. Defaults to 'False'.
    Returns:
      3-dimensional numpy array of floats (r/g/b/a) in range 0.0-255.0: Blended image


    if not disable_type_checks:
        _fcn_name = 'lighten_only'
        assert_image_format(img_in, _fcn_name, 'img_in')
        assert_image_format(img_layer, _fcn_name, 'img_layer')
        assert_opacity(opacity, _fcn_name)
    """
    global img_size_opacity
    img_in_norm = img_in / 255.0
    img_layer_norm = img_layer / 255.0
    #ratio = _compose_alpha(img_in_norm, img_layer_norm, opacity)
    #print("ratio")
    #print(ratio)

    #print("false")
    #print(img_size_opacity)
    ratio = img_size_opacity

    comp = np.maximum(img_in_norm[:, :, :3], img_layer_norm[:, :, :3])
    #comp = np.maximum(img_in_norm, img_layer_norm)

    ratio_rs = np.reshape(np.repeat(ratio, 3), [comp.shape[0], comp.shape[1], comp.shape[2]])
    img_out = comp * ratio_rs + img_in_norm[:, :, :3] * (1.0 - ratio_rs)
    img_out = np.nan_to_num(np.dstack((img_out, img_in_norm[:, :, 3])))  # add alpha channel and replace nans
    return img_out * 255.0


def browseFiles():
    global fileName
    #fileName = filedialog.askopenfilename(initialdir="/",title="select movie file",filetypes=[("ALL FILES","*.*"),("video file","*.py"),])
    fileName = filedialog.askopenfilename(title="select movie file")
    fileName_label.configure(text="File Opened: "+fileName)

def startProgram():
    global offset
    #global transparency

    offset = int(input_offset.get())
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

def processImage():
    global fileName
    global exit_event
    global done
    global img_size_opacity

    img_queue = []

    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    outputDir = uppath(fileName,1)
    if not os.path.exists(outputDir+'/processedImage'):
        os.makedirs(outputDir+'/processedImage')


    index = 0
    vidcap = cv2.VideoCapture(fileName)
    #success, image = vidcap.read()
    ret, frame = vidcap.read()

    img_base = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img_base[:, :, 3] = 255.
    img_base_float = img_base.astype(np.float32)
    img_base = np.uint8(img_base_float)
    img_base_raw = Image.fromarray(img_base)
    img_size_opacity = np.full(img_base_raw.size, 0.5)


    print (img_size_opacity)
    output = Image.new("RGB",img_base_raw.size,(255,255,255,255))
    output.paste(img_base_raw)
    count_label.configure(text="Image: "+str(index))

    img_queue.append(img_base_float)
    #show image
    #img = ImageTk.PhotoImage(output.resize((800,600),Image.ANTIALIAS))
    #canvas.create_image(200,100,image=img,anchor=NW)

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

    img_trans = Image.fromarray(img_base)
    img_trans_float = img_base_float

    while True:
        print("processing image:"+str(index))
        index +=1
        ret, frame=vidcap.read()

        #Ending last photo without blending
        if not ret and (len(img_queue) == 2):
            #last blending
            img_blend_float = lighten_only(img_queue[0],img_queue[1],0.5,True)
            img_blend = np.uint8(img_blend_float)
            img_blend_raw=Image.fromarray(img_blend)
            output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
            output.paste(img_blend_raw)
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

            #last Image
            index += 1
            img_blend_float = img_queue[1]
            img_blend = np.uint8(img_blend_float)
            img_blend_raw=Image.fromarray(img_blend)
            output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
            output.paste(img_blend_raw)
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
            break

        #Ending photos, poping queue
        elif not ret:
            img_queue.pop(0)
            #img_temp_base_float = img_queue[0]
            #for i in range(1,len(img_queue)):
            #    img_temp_blend_float = lighten_only(img_temp_base_float,img_queue[i],1)
            #    img_temp_base_float = img_temp_blend_float
            #img_blend_float = img_temp_base_float
            img_blend_float = np.maximum.reduce(img_queue)
            img_blend = np.uint8(img_blend_float)
            img_blend_raw=Image.fromarray(img_blend)
            #counter
            count_label.configure(text="Ending Image: "+str(index))
            output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
            output.paste(img_blend_raw)
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


        #normal execution
        else:
            img_layer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img_layer[:, :, 3] = 255.
            img_layer_float = img_layer.astype(np.float32)

            #add to array
            img_queue.append(img_layer_float)

            if(index < offset):
                #np.maximum
                img_blend_float = np.maximum(img_base_float,img_layer_float)
                #img_blend_float = lighten_only(img_base_float,img_layer_float,0.5)
            else:
                img_queue.pop(0)
                #img_temp_base = []
                #for i in range(0,len(img_queue)):
                #    img_temp_base.append(img_queue[i])
                img_blend_float = np.maximum.reduce(img_queue)
                #img_temp_base_float = img_queue[0]
                #for i in range(1,len(img_queue)):
                #    img_temp_blend_float = lighten_only(img_temp_base_float,img_queue[i],0.5)
                #    img_temp_base_float = img_temp_blend_float
                #img_blend_float = img_temp_base_float

            img_blend = np.uint8(img_blend_float)
            img_blend_raw=Image.fromarray(img_blend)

            #counter
            count_label.configure(text="Image: "+str(index))
            output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
            output.paste(img_blend_raw)
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

            #reset base
            img_base_float = img_blend_float

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

    '''
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
    '''
    done = True


root = Tk()
root.title('image layering')

canvas = Canvas(root,width=400,height=700)
canvas.pack()

button_explore = Button(root,width=10,text="select File",command=browseFiles)
button_explore.place(x=8,y=15)

fileName_label = Label(root,text="")
fileName_label.place(x=8,y=40)

input_offset = tk.StringVar(root)
input_transparent = tk.StringVar(root)
input_quality = tk.StringVar()

offset_label = Label(root,text="疊加層數")
offset_label.place(x=8,y=80)
offset_input = Entry(root,width=10, textvariable=input_offset)
offset_input.insert(10,60)
offset_input.place(x=10,y=100)

#transparent_label = Label(root,text="漸層程度 (0.00 ~ 1.00)")
#transparent_label.place(x=8,y=140)
#transparent_input = Entry(root,width=10,textvariable=input_transparent)
#transparent_input.insert(10,0.1)
#transparent_input.place(x=8,y=160)

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
quality_input.current(0)

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