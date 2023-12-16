from pyb import Pin, Timer
class Motor:
    #init function requrires a preconfigured timer channel, a timer channel number, enable pin, input pin, dir pin, and max effort
    def __init__(self,
                 PWMtim: Timer,
                 channel: int,
                 EnPin: Pin,
                 InPin: Pin,
                 DirPin: Pin,
                 effortLim: int):
        #creates a pwm on the input pin given using the given timer channel
        self.PWM = PWMtim.channel(channel, pin = InPin, mode = Timer.PWM)
        #configure enable and direction as output
        self.En = Pin(EnPin, mode = Pin.OUT_PP)
        self.Dir = Pin(DirPin, mode = Pin.OUT_PP)
        self.effortLim = effortLim
        #Enable the motor and set default effort to 0
        self.enable()
        self.setEffort(0)
    
    #takes a single float input and sets the motor speed accordingly
    def setEffort(self, effort: float):
        self.effort = effort
        #sets the numerical value of the input as the motor effort
        self.PWM.pulse_width_percent(abs(effort) if abs(effort) <= self.effortLim else self.effortLim)
        #Uses the sign of the input to decide direction
        if effort > 0:
            self.Dir.low()
        elif effort < 0:
            self.Dir.high()
        else:
            self.PWM.pulse_width_percent(0)
    #no inputs, enables motor
    def enable(self):
        self.En.high()
    #no inputs, enables motor
    def disable(self):
        self.En.low()
