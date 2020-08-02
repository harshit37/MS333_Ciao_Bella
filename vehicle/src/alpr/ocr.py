import numpy as np
import argparse
import time
from cv2 import cv2
import os



def read_plate(frame):
  path="src/alpr/alpr_data/ocr/ocr-net.names"
  labelsPath = path
  LABELS = open(labelsPath).read().strip().split("\n")

  np.random.seed(42)
  COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
    dtype="uint8")

  weightsPath="src/alpr/alpr_data/ocr/ocr-net.data"
  configPath ="src/alpr/alpr_data/ocr/ocr-net.cfg"
  print("Running ocr.py")
  net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)



#This is not the path of the image
#it is after cv2 has read the image


  image=frame																
  (H, W) = image.shape[:2]


  ln = net.getLayerNames()
  ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


  blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (128, 128),swapRB=True, crop=False)
  net.setInput(blob)
  layerOutputs = net.forward(ln)


  boxes = []
  confidences = []
  classIDs = []
  keylist= LABELS
  dict_boundingbox = {key:[] for key in keylist}
  dict_confidence={key:[] for key in keylist}

  for output in layerOutputs:
    for detection in output:
      scores = detection[5:]
      classID = np.argmax(scores)
      confidence = scores[classID]
      if confidence > 0.4:
        box = detection[0:4] * np.array([W, H, W, H])
        (centerX, centerY, width, height) = box.astype("int")
        x = int(centerX - (width / 2))
        y = int(centerY - (height / 2))
        if LABELS[classID] in keylist:
          dict_boundingbox[LABELS[classID]].append([x, y, int(width), int(height)])
          dict_confidence[LABELS[classID]].append(float(confidence))
        confidences.append(float(confidence))
        boxes.append([x, y, int(width), int(height)])
        classIDs.append(classID)
  idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,0.3)

  if len(idxs) > 0:
    for i in idxs.flatten():
      (x, y) = (boxes[i][0], boxes[i][1])
      (w, h) = (boxes[i][2], boxes[i][3])
      color = [int(c) for c in COLORS[classIDs[i]]]
      cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
      text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
      cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, color, 2)

  print(dict_boundingbox)
  print(dict_confidence)
  cropped_images = []
  for key in keylist:
    for bbox in dict_boundingbox[key]:
      x=bbox[0]
      y=bbox[1]
      w=bbox[2]
      h=bbox[3]
      cropped_image=image[y:y+h,x:x+w]
      cropped_images.append(cropped_image)

  return cropped_images


if __name__ == "__main__":
    path = "image.png"
    frame = cv2.imread(path)
    cropped_images = read_plate(frame)
    counter = 1
    for x in cropped_images:
        cv2.imwrite("cropped" + str(counter) + ".jpg", frame)
        counter+=1


    