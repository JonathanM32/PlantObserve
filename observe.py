from __future__ import division
import pynma
import schedule
from Adafruit_IO import Client
from subprocess import PIPE, Popen
import psutil
import time
import picamera
from datetime import datetime
from os import system as shell
import base64

print ("Modules loaded")

print ("Create AIO Client...")

aio = Client("b5d28a49428e45158fbf3d9cef710827")
p = pynma.PyNMA("bb31cd6de55e2da00c40e94e1576747b9d513b1ea00c7395")
print ("Done")

print ("Upload test data to confirm link...")

aio.send('systemTime',time.strftime("%Y-%m-%d %H:%M:%S")) 

data = aio.receive('systemTime')
print('Received value: {0}'.format(data.value))

print("\n Create Camera Instance")
try:
	camera = picamera.PiCamera()
except:
	p.push('PLOTS',"Failed to initalize PiCamera")


def recordData():
	try:
		filename = "PlantObserveration_unprocessed_%s.jpg"  %datetime.now().strftime('%m-%d-%Y-%s')
		camera.capture(filename)
		shell("fswebcam -r 1280x720  wc_%s.jpg" %datetime.now().strftime('%m-%d-%Y-%s'))
		print("Image " + filename +" Captured")
		shell("./dropbox_uploader.sh upload wc_* /ScienceFair")
		shell('./dropbox_uploader.sh upload %s /ScienceFair' %filename)
	except:
		p.push('PlOSt_1','PROGRAM FAILURE!!') 
schedule.every().day.at('8:30').do(recordData)
schedule.every().day.at('12:30').do(recordData)
schedule.every().day.at('16:30').do(recordData)

def checkIn():
	aio.send('systemTime','Script running as of: \n' + time.strftime("%Y-%m-%d %H:%M:%S"))
schedule.every(30).minutes.do(checkIn)

while True:
    schedule.run_pending()
    time.sleep(1)
