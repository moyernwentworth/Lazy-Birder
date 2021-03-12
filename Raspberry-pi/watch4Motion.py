from gpiozero import MotionSensor
from picamera import PiCamera
import time
from time import sleep
import uploadBucket
#comment 
pir = MotionSensor(4)
camera = PiCamera()
camera.rotation = 180
 
while True:
 pir.wait_for_motion()
 print("Motion detected!")
 camera.start_preview(fullscreen=False, window = (1250,10,640,480))
 filename = "/home/pi/scripts/pics/" + (time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"
 sendFilename =(time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"
 camera.capture(filename)
 pir.wait_for_no_motion()
 camera.stop_preview()
 uploadBucket.uploadPic(sendFilename,filename)
 #add check like in processing gcloud script
 print ("uploaded")
