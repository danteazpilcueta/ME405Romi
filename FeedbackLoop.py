# General purpose feedback loop

from time import ticks_diff, ticks_us
class FeedbackLoop:
    #Initializes a new feedback loop. Takes the mode, the minimum, the maximum, desired value, and proportional, integral and derivative gain constants
    def __init__(self,
                 mode: int,
                 minimum: float,
                 maximum: float,
                 ref: float,
                 pg: float,
                 ig: float,
                 dg: float):
        self.mode = mode
        self.min = minimum
        self.max = maximum
        self.ref = ref
        self.kp = pg
        self.ki = ig
        self.kd = dg
        self.prevErr = 0
        self.err = 0
        self.intErr = 0
        self.derErr = 0
        self.result = 0
        #initializes the ticks counter
        self.ticks1 = 0
        self.ticks2 = 0
    
    def update(self, measured: float):
        #calculates error based off the difference between the reference value and the current value given in the function call. Augmented by mode
        self.err = self.ref - self.mode * measured
        #measure the current tick value 
        self.ticks2 = ticks_us()
        #find the time elapsed via the difference in tick values
        self.tickDiff = ticks_diff(self.ticks2, self.ticks1)
        #add the integral of the error into the integral error value.
        self.intErr += self.err * self.tickDiff * 1e-6
        #determine the slope of the error by dividing by time
        self.derErr = (self.err - self.prevErr) / (self.tickDiff * 1e-6)
        #Create an overall error based on the 3 errors augmented by their respective gains set in the init function
        self.result = self.kp * self.err + self.ki * self.intErr + self.kd * self.derErr
        self.prevErr = self.err
        #check if the given error is higher then our maximum or lower then our minimum and saturate if they are
        if self.result < self.min:
            self.result = self.min
        if self.result > self.max:
            self.result = self.max
            #Reset ticks one for comparison with the next time the function is called
        self.ticks1 = ticks_us()
    
    #restore all running error values to 0
    def reset(self):
        self.prevErr = 0
        self.err = 0
        self.intErr = 0
        self.derErr = 0
        self.result = 0