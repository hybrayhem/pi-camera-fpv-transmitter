#Initial Pi Zero overlay + recording code

import picamera
import time
import numpy
from PIL import Image, ImageDraw, ImageFont


# Video Resolution
VIDEO_HEIGHT = 720
VIDEO_WIDTH = 1280

# Cross Hair Image
crossHair = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT))
crossHairPixels = crossHair.load()
for x in range (0, VIDEO_WIDTH):
   crossHairPixels[x, 360] = (255, 255, 0)

for x in range(0, VIDEO_HEIGHT):
   crossHairPixels[640, x] = (255, 255, 0)

with picamera.PiCamera() as camera:
   camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
   camera.framerate = 30
   camera.led = False
   camera.start_preview()
   camera.start_recording('timestamped.h264')

   img = crossHair.copy()
   overlay = camera.add_overlay(img.tostring(), layer = 3, alpha = 100)

   time.sleep(1)
   try:
      while True:
         text = time.strftime('%H:%M:%S', time.gmtime())
         img = crossHair.copy()
         draw = ImageDraw.Draw(img)
         draw.font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)
         draw.text((10, 10), text, (255, 255, 255))
         draw.text((10, 100), text, (0, 255, 255))
         draw.text((10, 200), text, (255, 0, 255))
         draw.text((10, 300), text, (255, 255, 0))
         draw.text((200, 10), text, (255, 255, 255))
         draw.text((300, 100), text, (0, 255, 255))
         draw.text((400, 200), text, (255, 0, 255))
         draw.text((500, 300), text, (255, 255, 0))
         overlay.update(img.tostring())
         camera.wait_recording(0.9)

   finally:
      camera.remove_overlay(overlay)
      camera.stop_recording()