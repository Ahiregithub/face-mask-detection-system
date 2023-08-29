from tensorflow.keras.preprocessing.image import ImagebataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflOw.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img to_array
from tensorflOw.keras.preprocessing.image import load_img
from tensorflOw.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import os

INIT_LR = 1e-4 
EPOCHS = 20
BS = 32
DIRECTORY =r"C:\Users\Hp\Desktop\zip1\Face-Mask-Detection-master (1)\Face-Mask-Detection-master"
CATEGORIES = ["with_mask", "without_mask"]
# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images
print("[INFO] loading images...")
data []
labels = []
	for category in CATEGORIES:
path
	for img in os.listdir(path):
os. path.join(DIRECTORY, category)
 	for img in os.listdir(path):
img_path =os.path.join(path, img)
image = load_img(img_path, target_size-(224, 224))
image =img_to_array(image)
image =preprocess_input(image)

data.append (image)
labels.append (category)
# perform one-hot encoding on the labels
lb = LabelBinarizer()
labels = 1b.fit_transform(labels)
labels = to_categorical(labels)

 
lb LabelBinarizer()
labels = 1b.fit transform(labels)
labels = to_categorical(labels)
data =np.array(data, dtype="float32")
labels =np.array(labels)
(trainx, testX, trainY, testY) = train_test_split(data, labels,
test_size=0.20, stratify=labels, random state=42)
# construct the training image generator for data augmentation
aug =ImageDataGenerator(
rotation_range=20,
zoom_range=0.15,
width_shift_range=0.2,
height_shift_range=0.2,
shear_range=0.15,
horizontal_flip=True,
filmode="nearest")
# load the MobileNetV2 network, ensuring the head FC layer sets are
# left off
baseModel = MobileNetV2(weights="imagenet", include_top=False,
input_tensor=Input(shape=(224, 224, 3)))

headModel = baseModel.output
headModel
AveragePooling2D(pool_size=(7, 7))(headModel)
Flatten(name="flatten")(headModel)
Dense(128, activation="relu")(headModel)
headModel 00
headModel
headModel =Dropout (0.5) (headModel)
headModel
Dense(2, activation="softmax")(headModel)
# place the head FC model on top of the base model (this will become
# the actual model we will train)
model = Model1(inputs=baseModel.input, outputs-headModel)

for layer in baseModel.layers:
layer.trainable =False
# compile our model
print("[INFO] compiling model...")
opt Adam(Lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(Loss="binary_crossentropy", optimizer-opt,
metrics=["accuracy"])

 print("[INFO] training head...")
model.fit(
aug.flow(trainx, trainy, batch_size=BS),
steps_per_epoch=len(trainX) // BS,
validation_data=(testx, testY),
validation_steps=len(testX) // BS,
epochs=EPOCHS)

 # make predictions on the testing set
print("[INFO] evaluating network...")
predIdxs =model.predict(testx, batch_size-BS)
# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs =np.argmax(predIdxs, axis=1)
# show a nicely formatted classification report
print(classification_report(testY.argmax(axis=1), predIdxs,
target_names=1b.classes_))

 # serialize the model to disk
print("[INFO] saving mask detector model...")
model.save("mask_detector.model", save_format="h5")
# plot the training loss and accuracy
N= EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], Label="train_loss")
plt.plot(np.arange(e, N), H.history["val_loss"], Label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy" ], Label-"train_acc")
plt.plot(np.arange(e, N), H.history["val_accuracy"], Label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(Loc="lower left")
plt.savefig("plot.png")












