from pyb import Pin, Timer
from time import ticks_diff, ticks_us
from math import pi
# Motor encoder driver
class Encoder:
    #initializes encoder with given inputs. requires to motor pin inputs, a scalar value, a reload value and a channel number for the timer
    def __init__(self,
                 pin1: Pin,
                 pin2: Pin,
                 scaler: int,
                 reload: int,
                 channel: int):
        self.AutoR = reload
        self.AutoR12 = (self.AutoR + 1)/2
        self.NAutoR12 = -(self.AutoR + 1)/2
        self.tim = Timer(channel, period = self.AutoR, prescaler = scaler)
        #create an encoder channel on each pin
        self.tim.channel(1, pin = pin1, mode = Timer.ENC_AB)
        self.tim.channel(2, pin = pin2, mode = Timer.ENC_AB)
        self.delta = 0
        self.position = 0
        self.velocity = 0
        self.countNew = 0
        self.countOld = 0
        self.ticks1 = 0
        self.ticks2 = ticks_us()
    
    #updates encoders, must be done frequently in main to keep encoders accurate
    def update(self):
        self.countNew = self.tim.counter()
        self.delta = self.countNew - self.countOld
        if self.delta > self.AutoR12:
            self.delta -= self.AutoR + 1
        elif self.delta < self.NAutoR12:
            self.delta += self.AutoR + 1
        self.ticks2 = ticks_us()
        self.tickDiff = ticks_diff(self.ticks2, self.ticks1)
        self.position += self.delta
        self.velocity = (self.delta / 1440 * 2*pi) / (self.tickDiff * 1e-6) # rad/s
        self.countOld = self.countNew
        self.ticks1 = ticks_us()
    
    #reset running position count
    def reset(self):
        self.position = 0
        self.countOld = self.tim.counter()
        self.ticks1 = ticks_us()