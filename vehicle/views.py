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
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from vehicle.yolov5.detect import *




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
    return render(request, "vehicle/homeLogin.html")


def queryfromimage(request):

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

    return render(request, "vehicle/submitted.html", context)

def querybyform(request):

    print("HI")
    print(request.POST)

    context = {}
    images_path = []
    print(request.POST)
    if(request.method == "POST"):
        if(request.POST['car_plate'] is ""):
            q = CarSurveillance.objects.all()
            for i in q:
                image_path = i.Imagename
                images_path.append('frames/' + str(image_path))
        else:
            q = CarSurveillance.objects.filter(PlateNumber = request.POST['car_plate'])
            for i in q:
                image_path = i.Imagename
                images_path.append('frames/' + str(image_path))

    context['images_path'] = images_path
    print(images_path)
    return render(request, "vehicle/submitted.html", context)


def video_player(request):
    return(request, "vehicle/video_player.html")    

# if __name__ == "__main__":
#     img_path = "src/test_images/Indian_vehicles/0.png"
#     frame = cv2.imread(img_path)
#     extract_attributes(frame)