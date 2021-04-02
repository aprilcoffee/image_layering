import cv2
import glob, os
import numpy
from blend_modes import normal
from blend_modes import lighten_only
import numpy as py
import cv2 
from PIL import Image, ImageTk




new = False
cap = cv2.VideoCapture(0)
#cap.set(cv2.CV_CAP_PROP_FPS,30)

#ret = cap.set(0,720)
while(cap.isOpened()):
	ret,frame = cap.read()
	if (new == False):
		img_base = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		img_base[:, :, 3] = 255
		img_base_raw = Image.fromarray(img_base)
		img_base_raw_re = img_base_raw.resize((1280,720),Image.ANTIALIAS)
		img_base_float = Image.fromarray(img_base_raw_re).astype(numpy.float32)
		#img_base = numpy.uint8(img_base_float)
		#img_base_raw = Image.fromarray(img_base)
		new = True
		continue	
	img_layer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	img_layer[:, :, 3] = 255
	img_layer_raw = Image.fromarray(img_layer)
	img_layer_raw_re = img_layer_raw.resize((1280,720),Image.ANTIALIAS)
	img_layer_float = Image.fromarray(img_layer_raw_re).astype(numpy.float32)


	img_blend_float = lighten_only(img_base_float,img_layer_float,0.5)
	img_blend = numpy.uint8(img_blend_float)
	img_blend_raw=Image.fromarray(img_blend)
	#output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
	#output.paste(img_blend_raw)	
	#img_base_float = img_blend_float
	cv2.imshow('frame',img_blend)
	if cv2.waitKey(100)&0xFF==ord('q'):
		break
	done = True

cap.release()
cv2.destroyAllWindows()
