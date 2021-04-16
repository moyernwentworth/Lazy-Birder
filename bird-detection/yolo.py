import numpy as np
import argparse
import time
import cv2
import os
import gcsfs
from tempfile import NamedTemporaryFile

MODEL_PATH = 'gs://path/yolo-coco'
PROJECT_NAME = 'name'
CREDENTIALS = 'keys.json'

def main_start(path):
    yolo(path, MODEL_PATH)



def yolo_act(path, yolococo):
    # construct the argument parse and parse the arguments
    FS = gcsfs.GCSFileSystem(project=PROJECT_NAME,token=CREDENTIALS)
    # going to use authenticated open path in storage to access h5 file
    # very complicated, have to access specific way; if you dont get it dont touch it
    with FS.open(MODEL_PATH, mode='rb') as yolococo:
        # load the COCO class labels our YOLO model was trained on
        labelsPath = "gs://path/coco.names" #os.path.sep.join([yolococo, "coco.names"])
        with FS.open(labelsPath, mode='rt') as LABELS:
            LABELS = LABELS.read().strip().split("\n")
        print (LABELS)

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
            dtype="uint8")

        # derive the paths to the YOLO weights and model configuration

        weightsPathOrig = "gs://path/yolov3.weights"
        with FS.open(weightsPathOrig, mode='rb') as weightsPath:
            weightsPath=weightsPath.read()
        #print (weightsPath)
        configPathOrig ="gs://path/yolov3.cfg"
        with FS.open(configPathOrig, mode='rb') as configPath:
            configPath=configPath.read()
        #print (configPath)
        # load our YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        # load our input image and grab its spatial dimensions
        image = cv2.imread(path)
        (H, W) = image.shape[:2]
        white = [255,255,255]
        image = cv2.copyMakeBorder(image,20,20,20,20,cv2.BORDER_CONSTANT,value=white)

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        # show timing information on YOLO
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                confidence1 = 0
                if confidence > confidence1:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        threshold1 = 0
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold1)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            cropped = image
            i = 0
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)
                print("{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i]))

                if LABELS[classIDs[i]] == 'bird':
                    cropped = image[y:y+h, x:x+w]
                    # returns cropped image with bird in it in csv form to main
                    i = i + 1
                    return(cropped)


        # show the output image
        #cv2.imshow("Image", image)
        #cv2.waitKey(0)
    
     