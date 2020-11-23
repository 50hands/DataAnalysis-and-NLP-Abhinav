import requests
import numpy as np
import GetterEmotion
import sys
def Choice():
    if sys.argv[1]==str(1):
        emovalues,emolist=GetterEmotion.GetterTextual(sys.argv[2:])
        return list(emolist)[np.argmax(emovalues)]
    elif sys.argv[1]==str(2):
        emovalues,emolist=GetterEmotion.GetterFacialPhoto(sys.argv[2])
        return list(emolist)[np.argmax(emovalues)]
    elif sys.argv[1]==str(3):
        emovalues,emolist=GetterEmotion.GetterFacialCamera()
        return list(emolist)[np.argmax(emovalues)]
if __name__=='__main__':
    base='http://127.0.0.1:5000/'
    s=Choice()
    response=requests.get(base+'emotion/'+s)
    d=response.json()
    sys.exit(d)
