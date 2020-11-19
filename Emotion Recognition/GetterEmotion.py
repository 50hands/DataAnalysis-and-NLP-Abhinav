import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
import warnings
from PIL import Image
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
warnings.filterwarnings('ignore')
def GetterTextual(l):
    emovalues,emolist=textmodel(l)
    tempsum=sum(emovalues)
    emovalues=np.divide(np.asarray(emovalues,dtype=float),[tempsum for i in range(len(emolist))]).tolist()
    return [round(float(i*100),4) for i in emovalues],list(emolist)
def textmodel(message):
    emotions=('happy','fear','angry','sad','neutral')
    mat=textemotionscore(message)
    l=np.array([0,0,0,0,0],dtype='float')
    for i in mat:
        l=l+np.array([round(j,2) for j in i])
    emotionlist=[round(i*100/9,4) for i in l.tolist()]
    return emotionlist,emotions
def textemotionscore(message):
    num_classes=5
    embed_num_dims=300
    max_seq_len=500
    tokenizer=Tokenizer()
    tokenizer.fit_on_texts(pd.read_excel('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/TextModelFiles/Texts.xlsx',sheet_name='Sheet1')['Text'].tolist())
    embedd_matrix=np.load('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/TextModelFiles/Embeddmatrix.npy')
    textmodel=tf.keras.models.load_model('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/textmodel',custom_objects=None,compile=True,options=None)
    seq=tokenizer.texts_to_sequences(message)
    padded=pad_sequences(seq,maxlen=max_seq_len)
    pred=textmodel.predict(padded)
    pred=pred.tolist()
    return pred
def GetterFacialPhoto(filename):
    faceCascade=cv2.CascadeClassifier('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/haarcascade_frontalface_default.xml')
    model=tf.keras.models.load_model('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/model',custom_objects=None,compile=True,options=None)
    objects,y_pos,emotion,emotions=uploadimage(model,faceCascade,filename)
    tempsum=sum(emotions.tolist())
    emotions=np.divide(emotions,[tempsum for i in range(len(objects))]).tolist()
    return [round(float(i*100),4) for i in emotions],list(objects)
def uploadimage(model,faceCascade,filename):
    image=cv2.imread(filename)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3,minSize=(30,30))
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        roi_color=image[y:y+h,x:x+w]
        stri='C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/images/targetface.jpg'
        cv2.imwrite(stri,roi_color)
    img=tf.keras.preprocessing.image.load_img(stri,color_mode='grayscale',target_size=(48,48))
    x=tf.keras.preprocessing.image.img_to_array(img)
    x=np.expand_dims(x,axis=0)
    x/=255
    custom=model.predict(x)
    objects,y_pos,emotion=emotion_analysis(custom[0])
    if os.path.exists(stri):
        os.remove(stri)
    return objects,y_pos,emotion,custom[0]
def emotion_analysis(emotions):
    objects=('angry','disgust','fear','happy','sad','surprise','neutral')
    y_pos=np.arange(len(objects))
    emotion=objects[(emotions.tolist()).index(max(emotions))]
    return objects,y_pos,emotion
def GetterFacialCamera():
    faceCascade=cv2.CascadeClassifier('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/haarcascade_frontalface_default.xml')
    model=tf.keras.models.load_model('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/model',custom_objects=None,compile=True,options=None)
    emotionlist,emotions=opencamera(model,faceCascade)
    emotionlist2=[]
    for i in emotionlist:
        emotionlist2.append(round(float(i*100/sum(emotionlist)),4))
    return emotionlist2,list(emotions)
def opencamera(model,faceCascade):
    emotions=('angry','disgust','fear','happy','sad','surprise','neutral')
    cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    frame=0
    dict={'angry':[],'disgust':[],'fear':[],'happy':[],'sad':[],'surprise':[],'neutral':[]}
    while(True):
        ret,img=cap.read()
        img=cv2.resize(img,(640,360))
        img=img[0:308,:]
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            if w>130:
                cv2.rectangle(img,(x,y),(x+w,y+h),(64,64,64),2)
                detectedface=img[int(y):int(y+h),int(x):int(x+w)]
                detectedface=cv2.cvtColor(detectedface,cv2.COLOR_BGR2GRAY)
                detectedface=cv2.resize(detectedface,(48,48))
                img_pixels=tf.keras.preprocessing.image.img_to_array(detectedface)
                img_pixels=np.expand_dims(img_pixels,axis=0)
                img_pixels/=255
                predictions=model.predict(img_pixels)
                max_index=np.argmax(predictions[0])
                overlay=img.copy()
                opacity=0.4
                cv2.rectangle(img,(x+w+10,y-25),(x+w+150,y+115),(64,64,64),cv2.FILLED)
                cv2.addWeighted(overlay,opacity,img,1-opacity,0,img)
                cv2.line(img,(int((x+x+w)/2),y+15),(x+w,y-20),(255,255,255),1)
                cv2.line(img,(x+w,y-20),(x+w+10,y-20),(255,255,255),1)
                emotion=''
                for i in range(len(predictions[0])):
                    emotion='%s %s%s'%(emotions[i],round(predictions[0][i]*100,2),'%')
                    dict[emotions[i]].append(round(predictions[0][i]*100,2))
                    color=(255,255,255)
                    cv2.putText(img,emotion,(int(x+w+15),int(y-12+i*20)),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,1)
        cv2.imshow('img',img)
        frame=frame+1
        if frame>50:
            break
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    emotionlist=[]
    for i in dict.items():
        emotionlist.append(np.mean(dict[i[0]]))
    return emotionlist,emotions
