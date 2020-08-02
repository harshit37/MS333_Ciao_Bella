import sys, os
import keras
from cv2 import cv2
import traceback
from .src.keras_utils import load_model
from glob import glob
from .src.utils import im2single
from .src.keras_utils import load_model, detect_lp



path="C:/Users/Dell/Desktop/sih/alpr_data/lp-detector/wpod-net_update1"
def adjust_pts(pts,lroi):
	return pts*lroi.wh().reshape((2,1)) + lroi.tl().reshape((2,1))


def extract_lp(frame):
	
	print(os.getcwd())
	try:
		wpod_net_path = "vehicle/src/alpr/alpr_data/lp-detector/wpod-net_update1"
		
		wpod_net = load_model(wpod_net_path)
		lp_threshold = .5

		print ('Searching for license plates using WPOD-NET')
		Ivehicle = frame

		ratio = float(max(Ivehicle.shape[:2]))/min(Ivehicle.shape[:2])
		side  = int(ratio*288.)
		bound_dim = min(side + (side%(2**4)),608)
		_,LlpImgs,_ = detect_lp(wpod_net,im2single(Ivehicle),bound_dim,2**4,(240,80),lp_threshold)

		if len(LlpImgs):
			Ilp = LlpImgs[0]
			Ilp = Ilp*255.0
			# cv2.imwrite("vehicle/src/test_output/image.png", Ilp)

			return Ilp
		else:
			return None

	except:
		traceback.print_exc()
		return None





