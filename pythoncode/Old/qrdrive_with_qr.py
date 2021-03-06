#!/usr/bin/python
from __future__ import division
from sys import argv
import zbar
from PIL import Image
from graphics import *
if len(argv) < 2: exit(1)
import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import socket


WHEEL_RADIUS=30
WHEEL_SEPARATION_WIDTH = 93
WHEEL_SEPARATION_LENGTH = 90
linearX = 000
linearY = 2000
angularZ = 0
speedcalib = 2.55

def drive(coX0, coX1, coY0, coY1):
  LFspeed = -100 
  RFspeed = -100
  LBspeed = -100
  RBspeed = -100

  LFspeed = (1/WHEEL_RADIUS) * (linearX - linearY - (WHEEL_SEPARATION_WIDTH + WHEEL_SEPARATION_LENGTH)*angularZ) * speedcalib
  RFspeed = (1/WHEEL_RADIUS) * (linearX + linearY + (WHEEL_SEPARATION_WIDTH + WHEEL_SEPARATION_LENGTH)*angularZ) * speedcalib
  LBspeed = (1/WHEEL_RADIUS) * (linearX + linearY - (WHEEL_SEPARATION_WIDTH + WHEEL_SEPARATION_LENGTH)*angularZ) * speedcalib
  RBspeed = (1/WHEEL_RADIUS) * (linearX - linearY + (WHEEL_SEPARATION_WIDTH + WHEEL_SEPARATION_LENGTH)*angularZ) * speedcalib

  coXdiff = coX0-coX1
  coYdiff = coY0-coY1
  


  print str(LFspeed) + " " + str(RFspeed) + " " + str(LBspeed) + " " + str(RBspeed) + "\r"
  return str(LFspeed) + " " + str(RFspeed) + " " + str(LBspeed) + " " + str(RBspeed) + "\r"

def camqr():
  if len(argv) < 2: exit(1)

  # create a reader
  scanner = zbar.ImageScanner()

  # configure the reader
  scanner.parse_config('enable')

  # obtain image data
  pil = Image.open('image.jpg').convert('L')
  width, height = pil.size
  raw = pil.tostring()

  # wrap image data
  image = zbar.Image(width, height, 'Y800', raw)

  # scan the image for barcodes
  scanner.scan(image)

  # extract results
  for symbol in image:
      # do something useful with results
      print 'decoded', symbol.type, symbol.location, 'symbol', '"%s"' % symbol.data
      barloc = symbol.location


  print barloc[0][0]

  # clean up
  del(image)

  win = GraphWin('qr', 500, 500)
  pt = Circle(Point(barloc[0][0],barloc[0][1]),20)
  pt.draw(win)
  pt = Circle(Point(barloc[1][0],barloc[1][1]),5)
  pt.draw(win) 
  i = 0
  while (i<3):
      line = Line(Point(barloc[i][0],barloc[i][1]), Point(barloc[i+1][0], barloc[i+1][1]))
      line.draw(win)
      i = i + 1
  line = Line(Point(barloc[i][0],barloc[i][1]), Point(barloc[0][0], barloc[0][1]))
  line.draw(win)
  sqrt =((barloc[0][0] - barloc[2][0])**2 + (barloc[0][1] - barloc[2][1])**2)**0.5
  a =float(barloc[0][0] - barloc[2][0])
  b =float(barloc[0][1] - barloc[2][1])
  a = a / sqrt
  b = b / sqrt
  print sqrt
  print a
  print b

  a = a * 100
  b = b * 100
  c = 250

  line = Line(Point(c,c), Point(c+a,c+b))
  line.draw(win)

  #win.getMouse() #pause for click in window


# main() function
def main():
#  camqr()
#  Address=("127.0.0.1",5000)
#  s = socket.socket()
#  try:
#    s.connect(Address)
#  except Exception, e:
  print "The server is not running"
      

  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  #strPort = 'COM8'
  strPort = args.port

  ser = serial.Serial(strPort, 115200)
  printx = 0
  cnt = 1
  velX = 0
  posX = 0
  totvelX = 0
  totposX = 0
  velY = 0
  calib = 0
  totcalib = 0
  calibcnt = 100
  dt = .05  

  A = 0
  B = 1
  C = 2
  D = 3
  E = 4
  F = 5
  G = 6

  # A X - -
  # - X - -
  # - X X X
  # - - - -
  
  route  = (A,0),(A,1),(B,1),(C,1),(C,2),(C,3)
  routelen = 5

  print route[0][0]
  print route[1]



  print('reading from serial port %s...' % strPort)

  print('plotting data...')

  
  frameCnt = 0
  while True:
    try:
      line = ser.readline()
      data = [float(val) for val in line.split()]
     
      # print data
      frameCnt = int(cnt / 10)

      if frameCnt < routelen:
        ser.write(drive(route[frameCnt][0],route[frameCnt+1][0],
                    route[frameCnt][1],route[frameCnt+1][1])) 
        #ser.write(driveY() 

      
      if(len(data) == 10):
        dt = data[9]
        accXcurr = data[0]- calib
        totvelX += accXcurr*dt
        if (cnt < calibcnt):
          totcalib += accXcurr
          calib = totcalib/cnt
        #velX = totvelX/cnt
        velX += accXcurr*dt
        totposX += velX*dt
        #posX = totposX/cnt
        posX += velX*dt
        velY += data[1]/cnt 
        if printx:
          print('X\'\' %s' % accXcurr)
          print('X\'  %s' % velX)
          print('X   %s' % posX)
          print(' ')
        cnt += 1

      
  
  
    except ValueError:
        print('Not a float')
        
    except KeyboardInterrupt:
        ser.write("0 0 0 0\r")
        raise SystemExit

      

  
  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
