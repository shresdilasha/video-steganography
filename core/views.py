from django.shortcuts import render
from . models import Encoding
from . forms import DecodeForm, EncodeForm
from PIL import Image
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def home(request):
    return render(request, 'core/home.html')


# def genData(data):

# 		# list of binary codes
# 		# of given data
# 		newd = []

# 		for i in data:
# 			newd.append(format(ord(i), '08b'))
# 		return newd

# # Pixels are modified according to the
# # 8-bit binary data and finally returned
# def modPix(pix, data):

# 	datalist = genData(data)
# 	lendata = len(datalist)
# 	imdata = iter(pix)

# 	for i in range(lendata):

# 		# Extracting 3 pixels at a time
# 		pix = [value for value in imdata.__next__()[:3] +
# 								imdata.__next__()[:3] +
# 								imdata.__next__()[:3]]

# 		# Pixel value should be made
# 		# odd for 1 and even for 0
# 		for j in range(0, 8):
# 			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
# 				pix[j] -= 1

# 			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
# 				if(pix[j] != 0):
# 					pix[j] -= 1
# 				else:
# 					pix[j] += 1
# 				# pix[j] -= 1

# 		# Eighth pixel of every set tells
# 		# whether to stop ot read further.
# 		# 0 means keep reading; 1 means thec
# 		# message is over.
# 		if (i == lendata - 1):
# 			if (pix[-1] % 2 == 0):
# 				if(pix[-1] != 0):
# 					pix[-1] -= 1
# 				else:
# 					pix[-1] += 1

# 		else:
# 			if (pix[-1] % 2 != 0):
# 				pix[-1] -= 1

# 		pix = tuple(pix)
# 		yield pix[0:3]
# 		yield pix[3:6]
# 		yield pix[6:9]

# def encode_enc(newimg, data):
# 	w = newimg.size[0]
# 	(x, y) = (0, 0)

# 	for pixel in modPix(newimg.getdata(), data):

# 		# Putting modified pixels in the new image
# 		newimg.putpixel((x, y), pixel)
# 		if (x == w - 1):
# 			x = 0
# 			y += 1
# 		else:
# 			x += 1

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2


# In[2]:


def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result



def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S


# In[15]:


def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key


# In[16]:


def preparing_key_array(s):
    return [ord(c) for c in s]


# In[17]:


def encryption(plaintext, key):
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext


# In[18]:


def decryption(ciphertext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext


# In[19]:


def embed(frame, msg, key): #  here msg is the parameter that is sent to this function for accepting the messages 
    data=encryption(msg, key)    # here the msg is encrypted
    print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='*^*^*'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame


# In[20]:


def extract(frame):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    for i in range(0,len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                    return 


# In[21]:


def encode_vid_data(file, frame_no, msg, key):
    cap=cv2.VideoCapture(file)
    vidcap = cv2.VideoCapture(file)    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))
    size = (frame_width, frame_height)
    print('fourcc' , fourcc)
    print('size' , size)
    out = cv2.VideoWriter('media/encoded/steg.mp4',fourcc, 25.0, size)
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    if (frame_no > max_frame or frame_no < max_frame):
        print("error")
    # print("Enter the frame number where you want to embed data : ")
    n=frame_no
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame, msg, key)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)
    print("\nEncoded the data successfully in the video file.")


# In[22]:


def decode_vid_data(frame):
    cap = cv2.VideoCapture('stego_video.mp4')
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    print("Total number of Frame in selected Video :",max_frame)
    n=int(input())
    vidcap = cv2.VideoCapture('stego_video.mp4')
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            extract(frame_)
            return


# In[23]:

# In[ ]:

#allowing user to first upload a video that could provide a result of total number of video frames

def video_upload(request):

    return 



def encode(request):
    video = Encoding.objects.last()
    videofile = None
    if video == None:
        print("File not found")
    else:
        videofile = video.file.path
    form = EncodeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        file = form.cleaned_data['file']
        secret_key = form.cleaned_data['secret_key']
        message = form.cleaned_data['message']
        frame_number = form.cleaned_data['frame_number']
        encode_vid_data(videofile, frame_number, message, secret_key)
        messages.error(request, f'Encoded')
    context ={'video' : video, 'form' : form}
    return render(request, 'core/encode.html',context)


def decode(request):
    video = Encoding.objects.last()
    videofile = None
    if video == None:
        print("File not found")
    else:
        videofile = video.file.path
    form = DecodeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        file = form.cleaned_data['file']
        secret_key = form.cleaned_data['secret_key']
        frame_number = form.cleaned_data['frame_number']
        decode_vid_data(videofile, frame_number)
        messages.error(request, f'Encoded')
    context ={'video' : video, 'form' : form}

    return render(request, 'core/decode.html',  context)
# %%
 

def about_us(request):
    return render(request, 'core/about.html')