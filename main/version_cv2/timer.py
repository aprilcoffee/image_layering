import cv2
import numpy as np
from PIL import Image, ImageTk
import timeit
import time


index = 0
iteration = 600
offset = 300
fileName = 'trim1080.mov'
vidcap = cv2.VideoCapture(fileName)
new = False
img_queue = []

for i in range(300):
    ret, frame = vidcap.read()
    index+=1
    start = time.process_time()
    #print(index)
    if (new == False):
        img_base_float = cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
        new = True

    img_layer_float = cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
    img_queue.append(img_layer_float)
    if(index >= offset):
        img_queue.pop(0)
        img_blend_float = np.maximum.reduce(img_queue)
    else:
        img_blend_float = np.maximum(img_base_float,img_layer_float)

    img_blend = img_blend_float
    img_blend_raw=Image.fromarray(img_blend)

    #counter
    output = Image.new("RGB",img_blend_raw.size,(255,255,255,255))
    output.paste(img_blend_raw)
    output.save('hi/'+'frame'+str(index)+'.jpg',quality='web_maximum',subsampling=0)
    img_base_float = img_blend_float
    end = time.process_time()
    print(str(index)+'\ttime\t'+str(end-start))

    #return True

print(index)

def max(q):
    return np.maximum.reduce(q)

def cut(q):
    img_queue_c = np.array_split(q,10)
    q_b = []
    for i in range(len(img_queue_c)):
        q_b.append(np.maximum.reduce(img_queue_c[i]))
    return np.maximum.reduce(q_b)

def obo(q):
    bases = q[0]
    for i in range(1,len(q)):
        layer = img_queue[i]
        blend = np.maximum(bases,layer)
        bases = blend
    return bases

start = time.process_time()
max(img_queue)
end = time.process_time()
print('max\t'+str(end-start))

start = time.process_time()
cut(img_queue)
end = time.process_time()
print('cut\t'+str(end-start))

start = time.process_time()
obo(img_queue)
end = time.process_time()
print('obo\t'+str(end-start))

img_queue = np.int8(img_queue)

start = time.process_time()
max(img_queue)
end = time.process_time()
print('max\t'+str(end-start))

start = time.process_time()
cut(img_queue)
end = time.process_time()
print('cut\t'+str(end-start))

start = time.process_time()
obo(img_queue)
end = time.process_time()
print('obo\t'+str(end-start))
