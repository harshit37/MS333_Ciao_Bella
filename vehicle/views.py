from django.shortcuts import render, HttpResponse
import argparse
# Create your views here.
from .models import CarSurveillance, CarRTO, Camera, Person
from .main_from_videos import process_video
from cv2 import cv2
from datetime import datetime
import os
from vehicle.src.alpr.vehicle_detection import extract_car
from vehicle.src.alpr.license_plate_detection import extract_lp
from vehicle.src.alpr.ocr2 import read_plate
from vehicle.src.color_identifier import color_segmenter
from vehicle.src.alpr.correct import accomodate
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from vehicle.yolov5.detect import *
from vehicle.src.alpr import *
import logging
logger = logging.getLogger(__name__)

# Put the logging info within your django view



import sys 
sys.path.insert(0, "C:/Users/lenovo/Desktop/smart_india_hackathon/MS333_CIAO_BELLA/vehicle/yolov5")



class optimi:
    weights = ['vehicle/yolov5/weights/brand_weights/best_wm.pt']
    source = 'vehicle/yolov5/inference/images'
    output = 'vehicle/yolov5/inference/output'
    img_size = 640
    conf_thres = 0.4
    iou_thres = 0.5
    device = ''
    view_img = False
    save_txt = False
    classes = None
    agnostic_nms = False
    augment= False
    update = False


def save_to_database(request):
    # path = "src/test_videos/new_videos/9.mp4"
    # ans = process_video(path)

    
    
    # for x in ans:
    #     c = CarSurveillance(CameraID = "2820010001", Brand = "Tata", PlateNumber = x[0], CarModel = "Nano", Color = x[1], FirstSeen = datetime.now(), LastSeen = datetime.now())
    #     c.save()
    # path = "src/test_output/scene00051.png"
    # frame = cv2.imread(path)

    # vehicles, img = extract_car(frame)
    # cv2.imwrite("temp3.jpg", vehicles[0])
    # for i in vehicles:
    #     cv2.imwrite("temp2.jpg", img)
    #     cv2.imwrite("temp1.jpg", i)
    #     maj_color=color_segmenter(i)
    #     print(maj_color)
    #     lp = extract_lp(i)
    #     x =  (read_plate(lp))
    #     print(x)

    
    # opt = optimi()
    # with torch.no_grad():
    #     if opt.update:  # update all models (to fix SourceChangeWarning)
    #         for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
    #             detect(opt, save_img=True)
    #             strip_optimizer(opt.weights)
    #     else:
    #         detect(opt, save_img=True)
    print("SFD")
    logger.info("HI HI HI ")
    return render(request, "vehicle/homeLogin.html")


def testingpage(request):
    print("HI ")
    return render(request, "vehicle/testingpage.html")

def savetodatabase(request):

    print("Mohit Singhal")
    print(request)
    if request.method == 'POST' and request.FILES['filename']:
        print("HO HO HO")
        myfile = request.FILES['filename']
        print(myfile.name)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        path = "media/" + myfile.name
        frame = cv2.imread(path)

        vehicles, img = extract_car(frame)
        for i in vehicles:
            maj_color=color_segmenter(i)
            print(maj_color)
            lp = extract_lp(i)
            x =  (read_plate(lp))
            print(x)
            context = {"major_color": maj_color, "number_plate": x}
        try:
            frame = cv2.imread(path)
            vehicles, img = extract_car(frame)
            for i in vehicles:
                try:
                    maj_color=color_segmenter(i)
                    print(maj_color)
                    lp = extract_lp(i)
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
                        x = accomodate(list(x))
                        y = ""
                        for item in x:
                            y = y + str(item)
                        print(y)
                except Exception as e:
                    print(e)
        except Exception as e:
                print(e)

    return render(request, "vehicle/submitted.html", context)


def querybyimage(request):

    print("Mohit Singhal")
    print(request)
    major_colors = []
    plate_numbers = []
    logos = []
    if request.method == 'POST' and request.FILES['filename']:
        print("HO HO HO")
        myfile = request.FILES['filename']
        print(myfile.name)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        path = "media/" + myfile.name
        try:
            frame = cv2.imread(path)
            vehicles, img = extract_car(frame)
            for i in vehicles:
                try:
                    maj_color=color_segmenter(i)
                    print(maj_color)
                    lp = extract_lp(i)
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
                        x = accomodate(list(x))
                        y = ""
                        for item in x:
                            y = y + str(item)
                        print(y)
                        plate_numbers.append(y)
                        major_colors.append(maj_color)
                        opt = optimi()
                        opt.source = path
                        with torch.no_grad():
                            if opt.update:  # update all models (to fix SourceChangeWarning)
                                for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                                    brand_logo = detect(opt, save_img=False)
                                    strip_optimizer(opt.weights)
                            else:
                                brand_logo = detect(opt, save_img=False)
                        logos.append(brand_logo)    
                except Exception as e:
                    print(e)
        except Exception as e:
                print(e)
    context = {"major_colors": major_colors, "number_plates": plate_numbers, "logos" : logos}
    return render(request, "vehicle/tempo.html", context)




def querybyform(request):

    print("HI")
    print(request.POST)

    context = {}
    images_path = []
    images_timestamp = []
    print(request.POST)
    if(request.method == "POST"):
        if(request.POST['car_plate'] == ""):
            q = CarSurveillance.objects.all()
            for i in q:
                image_path = i.Imagename
                images_path.append('frames/' + str(image_path))
                images_timestamp.append(i.VideoTimeStamp)
        else:
            q = CarSurveillance.objects.filter(PlateNumber = request.POST['car_plate'])
            for i in q:
                image_path = i.Imagename
                images_path.append('frames/' + str(image_path))
                images_timestamp.append(i.VideoTimeStamp)

    context['images_path'] = images_path
    context['images_timestamp'] = images_timestamp
    print(images_path)
    return render(request, "vehicle/submitted.html", context)


def video_player(request):
    return render(request, "vehicle/video_player.html")    

# if __name__ == "__main__":
#     img_path = "src/test_images/Indian_vehicles/0.png"
#     frame = cv2.imread(img_path)
#     extract_attributes(frame)