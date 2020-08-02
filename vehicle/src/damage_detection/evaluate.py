import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt
import time
import cv2

from PIL import Image

from Model import Model

class Evaluate () :
    def __init__ (self) :
        model = Model ()
        self.generator = model.build_generator ()

        checkpoint_dir = './training_checkpoints/'
        checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
        checkpoint = tf.train.Checkpoint(generator=self.generator)

        checkpoint.restore ('training_checkpoints/ckpt-1')

    def from_numpy (self, image) :
        if not max (np.unique(image)) <= 1.0 :
            image = image / 255.0

        pred = self.generator (image[np.newaxis, ...], training=False)
        pred = np.where (pred>0.5, 1, 0).astype ('uint8')

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        pred = cv2.morphologyEx(pred[0, :, :, 0],cv2.MORPH_OPEN,kernel)

        return pred

    def from_path (self, image_file) :
        image = np.array (Image.open (image_file).resize ((128, 128))).astype ('float32') / 255.0
        pred = self.generator (image[np.newaxis, ...], training=False)
        pred = tf.nn.sigmoid (pred)
        pred = np.where (pred>0.5, 1, 0).astype ('uint8')

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        pred = cv2.morphologyEx(pred[0, :, :, 0],cv2.MORPH_OPEN,kernel)

        return pred


if __name__ == "__main__":
    obj = Evaluate()
    image_list=[]
    load_img=cv2.imread("1.jpg")
    
    cntr=0
    f_h=int(load_img.shape[0]/128)
    f_w=int(load_img.shape[1]/128)
    for i in obj.from_path("1.jpg"):
        row=[]
        cntc=0
        for j in i:
            if j==1:
                row.append(255)
                load_img[int(cntr*f_h),int(cntc*f_w)] = [0,255,0]

            else:
                row.append(j)

            cntc+=1

        image_list.append(row)
        cntr+=1
                
    img=np.array(image_list,dtype=object)

   
    print(img)
    img2=np.uint8(img)

    #img2= tf.image.resize(img2,[desired_h,desired_w])
    print(img2.shape)
    print(load_img.shape)
    cv2.imshow("dent_image",img2) 
    cv2.imshow("actual_image",load_img)
    cv2.waitKey()        