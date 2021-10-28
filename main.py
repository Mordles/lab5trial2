#!/usr/bin/env python3

import PCF8591 as ADC
import time
import RPi.GPIO as GPIO

ADC.setup(0x48)

GPIO.setmode(GPIO.BCM)
pins = [18,21,22,23] # controller inputs: in1, in2, in3, in4
for pin in pins:
 GPIO.setup(pin, GPIO.OUT, initial=0)


GPIO.setup(26, GPIO.OUT)


ccw = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]

state = 0

def delay_us(tus): # use microseconds to improve time resolution
 endTime = time.time() + float(tus)/ float(1E6)
 while time.time() < endTime:
  pass

"""
From ADC code  

def loop(dir): # dir = rotation direction (cw or ccw)
 for i in range(512): # full revolution (8 cycles/rotation * 64 gear ratio)
  for halfstep in range(8): # 8 half-steps per cycle
   for pin in range(4):    # 4 pins that need to be energized
    GPIO.output(pins[pin], dir[halfstep][pin])
  delay_us(1000)
"""
"""
From ADC code

def setup():
  ADC.setup(0x48)
"""

"""
From ADC code

def loop():
  while True:
    print(ADC.read(0))
    ADC.write(ADC.read(0))


def destroy():
  ADC.write(0)
"""

#ZERO method 
GPIO.output(26, 1)

time.sleep(0.1)
while (ADC.read(0) < 200):
  # move motor to zero
  for i in range(512): # full revolution (8 cycles/rotation * 64 gear ratio)
   for halfstep in range(8): # 8 half-steps per cycle
    for pin in range(4):    # 4 pins that need to be energized
     GPIO.output(pins[pin], ccw[halfstep][pin])
    delay_us(1000)
  
  print(ADC.read(0))
  ADC.write(ADC.read(0))
GPIO.output(26, 0)
GPIO.cleanup()

"""
#ANGLE method

current_degree = 0

n = input("Enter Degree: ")
degrees = int(n)
def angle(degrees):
  steps = (degrees*512)/360
  for i in range(steps):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(pins[pin], ccw[halfstep][pin])
      delay_us(1000)

angle(degrees) 
"""

"""
From Prof code

def halfstep(dir):
  # dir +/- 1 (ccw/cw)
  state += dir
  if state > 7: state = 0
  elif state < 0: state = 7
  for pin in range(4):
    GPIO.output(pins[pin], sequence[state][pin])
  delay_us(1000)  

def moveSteps(steps, dir):
  # move sequence given number of half steps
  for step in steps:
    halfstep(dir)

"""








"""
From ADC code

if __name__ == "__main__":
  try:
    setup()
    loop()
  except KeyboardInterrupt:
   destroy()
"""
