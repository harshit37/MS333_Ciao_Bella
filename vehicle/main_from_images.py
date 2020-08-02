# import object_detection
# import alpr
# import color_identifier

# from cv2 import cv2
# import os
# import shutil
from .models import Camera
from vehicle.src.alpr.vehicle_detection import extract_car
from vehicle.src.alpr.license_plate_detection import extract_lp
from vehicle.src.alpr.ocr2 import read_plate
from cv2 import cv2
from vehicle.src.color_identifier import color_segmenter
import os
def extract_attributes(frame):
    try:
        vehicles, bb_img = extract_car(frame)
        for i in vehicles:
            lp = extract_lp(i)
            maj_color=color_segmenter(i)
            x =  (read_plate(lp))
            print(x)
            print(maj_color)
        return x, maj_color
    except Exception as e:
        print(e)
        return None, None





# def image_attr(frame, counter,writer):
#     outputPath="src/testing_videos/output"
#     cropped_cars = object_detection.extract_car(frame,writer)
#     print(len(cropped_cars))
    
#     for img in cropped_cars:
#         try:
#             print("frame number:- ",counter)
#             maj_color=color_identifier.color_segmenter(img)
#             cv2.imwrite( outputPath+ "/car number " + str(counter) + ".jpg", img)
#             print("color:- ",maj_color)
#             license_plate=alpr.license_plate_detection.extract_lp(img)
#             #ocr lagao
#             cv2.imwrite( outputPath+ "/lp number " + str(counter) + ".jpg", license_plate)


#             counter+=1
#         except Exception as e:
#             print(e)

  

# if __name__ == "__main__":
#     path = "alpr-unconstrained/samples/test/har4.jpeg"
#     frame = cv2.imread(path)
#     image_attr(frame, 4)