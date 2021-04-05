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
cap = cv2.VideoCapture(1)
#cap.set(cv2.CV_CAP_PROP_FPS,30)
#while True:
#ret = cap.set(0,720)
while(cap.isOpened()):
	ret,frame = cap.read()
	if (new == False):
		img_base = (Image.fromarray(frame)).resize((1280,720),Image.ANTIALIAS)
		img_base = numpy.uint8(img_base)
		img_base = cv2.cvtColor(img_base, cv2.COLOR_RGB2RGBA)
		img_base[:, :, 3] = 255
		img_base_float = img_base.astype(numpy.float32)
		#img_base = numpy.uint8(img_base_float)
		#img_base_raw = Image.fromarray(img_base)
		new = True
		continue	

	img_layer = (Image.fromarray(frame)).resize((1280,720),Image.ANTIALIAS)
	img_layer = numpy.uint8(img_layer)
	img_layer = cv2.cvtColor(img_layer, cv2.COLOR_RGB2RGBA)
	img_layer[:, :, 3] = 255
	img_layer_float = img_layer.astype(numpy.float32)

	img_blend_float = lighten_only(img_base_float,img_layer_float,0.5)
	img_blend = numpy.uint8(img_blend_float)
	img_blend_raw=Image.fromarray(img_blend)
	#output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
	#output.paste(img_blend_raw)	
	img_base_float = img_blend_float
	cv2.imshow('frame',img_blend)
	key = cv2.waitKey(1) & 0xFF
	if key==32:
		new = False
	if key==27 or key==ord('q'):
		break
	done = True

cap.release()
cv2.destroyAllWindows()
