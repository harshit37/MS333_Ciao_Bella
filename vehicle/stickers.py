import os
import cv2
path="C:/Users/Dell/Desktop/sih/stickers/"
dest_path="C:/Users/Dell/Desktop/sih/final_stickers/"
counter=1
for web_img in os.listdir(path):
    img=cv2.imread(path+web_img)
    cv2.imwrite(dest_path+"sticker"+str(counter)+".jpg",img)
    counter+=1

