from fastai.vision import *
from fastai.metrics import accuracy
path =  "/content/drive/My Drive/SIH/cropped/classify/Sedan_data/"
img = open_image(get_image_files(path)[11])
img.show()

learner=load_learner("/content/pura_model","/content/sedan_suv.pkl")

pred_class,pred_idx,outputs = learner.predict(img)
print(pred_class)    # answer

