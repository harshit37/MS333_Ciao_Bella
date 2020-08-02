from alpr.vehicle_detection import extract_car
from alpr.license_plate_detection import extract_lp
from alpr.ocr2 import read_plate
from color_identifier import color_segmenter
from cv2 import cv2
import os 
from alpr.correct import jugaad


print("HI")
path = "testing_images/"
path_lp = "lp/"
path_color_masks = "color_masks/"
f = open("results.txt", "a")

for image in os.listdir(path):
    try:
        print(path + "/" + image)
        frame = cv2.imread(path + "/" + image)
        vehicles, img = extract_car(frame)
        for i in vehicles:
            try:
                maj_color=color_segmenter(i, image)
                print(maj_color)
                lp = extract_lp(i)
                cv2.imwrite("lp/" + image, lp)
                x =  (read_plate(lp))
                if( x is not None):
                    x = x.replace(".", "")
                    x = x.replace("-", "")
                    x = x.replace("_", "")
                    x = x.replace("{", "")
                    x = x.replace("(", "")
                    x = x.replace(")", "")
                    x = x.replace("|", "")
                    x = x.replace('"', "")
                    x = x.replace("}", "")
                    x = jugaad(list(x))
                    y = ""
                    for item in x:
                        y = y + str(item)
                    f.write(maj_color + "\n")
                    f.write(y + "\n")
                    print(y)
            except Exception as e:
                print(e)
    except Exception as e:
            print(e)
        
f.close()