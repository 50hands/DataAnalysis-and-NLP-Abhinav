import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
def emotion_analysis(emotions):
    objects=('angry','disgust','fear','happy','sad','surprise','neutral')
    y_pos=np.arange(len(objects))
    emotion=objects[(emotions.tolist()).index(max(emotions))]
    plt.bar(y_pos,emotions,align='center',alpha=0.5)
    plt.xticks(y_pos,objects)
    plt.ylabel('percentage')
    plt.title('Emotion')
    plt.show()
    return emotion
if __name__=='__main__':
    image=cv2.imread('50 Hands/Emotion Recognition/images/nina.jpg')
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faceCascade=cv2.CascadeClassifier('50 Hands/Emotion Recognition/haarcascade_frontalface_default.xml')
    faces=faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3,minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        roi_color=image[y:y+h,x:x+w]
        print('Face found.')
        stri='50 Hands/Emotion Recognition/images/targetface.jpg'
        cv2.imwrite(stri,roi_color)
    model=tf.keras.models.load_model('50 Hands/Emotion Recognition/model',custom_objects=None,compile=True,options=None)
    img=tf.keras.preprocessing.image.load_img(stri,color_mode='grayscale',target_size=(48,48))
    x=tf.keras.preprocessing.image.img_to_array(img)
    x=np.expand_dims(x,axis=0)
    x/=255
    custom=model.predict(x)
    emotion=emotion_analysis(custom[0])
    print('The person is',emotion,'!!!')
