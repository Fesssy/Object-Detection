import cv2
import numpy as np
import captureimage as cap
import askFile as ask

#defining values
whT = 320
confThreshold =0.5
nmsThreshold= 0.2

# Load YOLOv3 model and configuration
modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load COCO class labels
classesFile = "coco.names"
classNames = []
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')


# Perform object detection
def findObjects(outputs,img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    
    # Loop through the detections
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(det[2]*wT) , int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    # draw bounding boxes
    for i in indices:
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # print(x,y,w,h)
        cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
        cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                  (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        
# Asking for user's choice
choice = input("Image or video? ")

#
# Image
#

if 'image' in choice:

    # Load an image for object detection
    choice = input("Capture image? ")
    if 'yes' in choice:
        cap.run_camera_app()
        path = cap.path
    elif 'no' in choice:
        ask.main(0)
        path = ask.path

    image = cv2.imread(path)

    # Preprocess input image for YOLO
    blob = cv2.dnn.blobFromImage(image, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)

    # Set input for the network
    net.setInput(blob)

    # Get the output layers to be further process
    layersNames = net.getLayerNames()
    outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    
    #object detection
    findObjects(outputs,image)
    
    # Display the result
    cv2.imshow("Object Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#
# Video
#

elif 'video' in choice:

    choice = input("Webcam? ")

    if 'no' in choice:
        ask.main(1)
        path = ask.path
        cap = cv2.VideoCapture(path)
    elif 'yes' in choice:
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError('Cannot open the video')

    while True:
        ret, image = cap.read()

        # Preprocess input image for YOLO
        blob = cv2.dnn.blobFromImage(image, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)

        # Set input for the network
        net.setInput(blob)

        # Get the output layers to be further process
        layersNames = net.getLayerNames()
        outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)
        
        #object detection
        findObjects(outputs,image)

        # Display the result
        cv2.imshow("Object Detection", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
