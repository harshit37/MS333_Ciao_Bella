from PIL import Image
import pytesseract
import argparse
from cv2 import cv2
import os
import numpy as np


 
def read_plate(plate):
    print("Reading plate now...")
    pytesseract.pytesseract.tesseract_cmd =  'C:/Program Files/Tesseract-OCR/tesseract.exe'
    gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    # preproc = "thresh"
    # if preproc == "thresh":
    #     gray = cv2.threshold(gray, 0, 255,
    #         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # elif preproc == "blur":
    #     gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray)
    print(text)
    return text

if __name__ == "__main__":
    path = "image.png"
    frame = cv2.imread(path)
    read_plate(frame)