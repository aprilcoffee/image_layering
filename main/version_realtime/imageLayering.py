import cv2
import glob, os
import numpy
from blend_modes import normal
from blend_modes import lighten_only
import numpy as py
import cv2
from PIL import Image, ImageTk


def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

print(returnCameraIndexes())

new = False
cap = cv2.VideoCapture(0)
#cap.set(cv2.CV_CAP_PROP_FPS,30)
#while True:
#ret = cap.set(0,720)

img_queue = []
index = 0

while(cap.isOpened()):
    ret,frame = cap.read()
    print(index)
    index+=1

    if(index%2==0):
        continue
    if (new == False):
        img_base = (Image.fromarray(frame)).resize((720,480),Image.ANTIALIAS)
        img_base = numpy.uint8(img_base)
        img_base = cv2.cvtColor(img_base, cv2.COLOR_RGB2RGBA)
        img_base[:, :, 3] = 255
        img_base_float = img_base.astype(numpy.float32)
        img_queue.append(img_base_float)
        #img_base = numpy.uint8(img_base_float)
        #img_base_raw = Image.fromarray(img_base)
        new = True
        continue
    img_layer = (Image.fromarray(frame)).resize((720,480),Image.ANTIALIAS)
    img_layer = numpy.uint8(img_layer)
    img_layer = cv2.cvtColor(img_layer, cv2.COLOR_RGB2RGBA)
    img_layer[:, :, 3] = 255
    img_layer_float = img_layer.astype(numpy.float32)
    img_queue.append(img_layer_float)

    if(len(img_queue)<10):
        img_blend_float = lighten_only(img_base_float,img_layer_float,0.5)
    else:
        img_queue.pop(0)
        img_temp_base_float = img_queue[0]
        for i in range(1,len(img_queue)):
            img_temp_blend_float = lighten_only(img_temp_base_float,img_queue[i],0.5)
            img_temp_base_float = img_temp_blend_float
            i+=3
        img_blend_float = img_temp_base_float

    img_blend = numpy.uint8(img_blend_float)
    img_blend_raw=Image.fromarray(img_blend).resize((1280,720),Image.ANTIALIAS)
    img_blend = numpy.uint8(img_blend_raw)
    #output = Image.new("RGB",img_blend_raw.size,(255,255,255,255)
    #output.paste(img_blend_raw)
    img_base_float = img_blend_float
    cv2.imshow('frame',img_blend)
    key = cv2.waitKey(1) & 0xF
    if key==32:
        new = False
    if key==27 or key==ord('q'):
        break
    done = True

cap.release()
cv2.destroyAllWindows()
