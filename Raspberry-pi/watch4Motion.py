from gpiozero import MotionSensor
from picamera import PiCamera
import time
from time import sleep
import uploadBucket
import time
import pause
from datetime import datetime

pir = MotionSensor(4)
camera = PiCamera()
camera.rotation = 180
#print ("Starting Script"+" - " + time.strftime("%y%b%d_%H:%M:%S"))

while (True):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)

    pir.wait_for_motion()
    #print ("Motion detected! " + "- " + time.strftime("%y%b%d_%H:%M:%S"))
    try:
        camera.start_preview(fullscreen=False, window = (1250,10,640,480))
        filename = "/home/pi/scripts/pics/" + "name_here" + (time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"
        camera.capture(filename)
        camera.stop_preview()
        sendFilename = "nick_" + (time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"
        pir.wait_for_no_motion()
        #sleep(5)
    except Exception as e:
        print (e)
        pass
    #print(now)
    #print(today8pm)
    #camera.close()
    if now >= today8pm:
        camera.close()
        break
    else:
        try:
            uploadBucket.uploadPic(sendFilename,filename)
            print ("uploaded")
        except Exception:
            print ("opps - didn't upload")
            pass
