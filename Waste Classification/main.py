import os
import cvzone
from cvzone.ClassificationModule import Classifier
import cv2

# Open the webcam 
cap = cv2.VideoCapture(0)

# Load the pre-trained model 
classifier = Classifier('Resources/Model/keras_model.h5', 'Resources/Model/labels.txt')

# Load the arrow image used to indicate the detected bin
imgArrow = cv2.imread('Resources/arrow.png', cv2.IMREAD_UNCHANGED)

# Initialize the bin class ID
classIDBin = 0

# Import all waste images
imgWasteList = []
pathFolderWaste = "Resources/Waste"
pathList = os.listdir(pathFolderWaste)
for path in pathList:
    imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste, path), cv2.IMREAD_UNCHANGED))

# Import all different bins images 
imgBinsList = []
pathFolderBins = "Resources/Bins"
pathList = os.listdir(pathFolderBins)
# Load each bin image into the list
for path in pathList:
    imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_UNCHANGED))

classDic = {
    0: None,    # No class detected (default)
    1: 0,       # Recyclable waste
    2: 0,       # Recyclable waste
    3: 3,       # Residual waste
    4: 3,       # Residual waste
    5: 1,       # Hazardous waste
    6: 1,       # Hazardous waste
    7: 2,       # Food waste
    8: 2        # Food waste
}

while True:
    # Read a frame from the webcam
    _, img = cap.read()
    
    # Resize the webcam image to fit the display
    imgResize = cv2.resize(img, (454, 340))

    # Load the background image 
    imgBackground = cv2.imread('Resources/bgimg.png')

    # Get the prediction 
    predection = classifier.getPrediction(img)

    classID = predection[1]
    print(classID)
    if classID != 0:
        # Overlay the corresponding waste image onto the background
        imgBackground = cvzone.overlayPNG(imgBackground, imgWasteList[classID - 1], (909, 127))
        
        # Overlay the arrow image to indicate which bin to use
        imgBackground = cvzone.overlayPNG(imgBackground, imgArrow, (978, 320))

        classIDBin = classDic[classID]

    imgBackground = cvzone.overlayPNG(imgBackground, imgBinsList[classIDBin], (895, 374))

    # Place the resized webcam image into the background image
    imgBackground[148:148 + 340, 159:159 + 454] = imgResize

    cv2.imshow("Output", imgBackground)
    cv2.waitKey(1)
