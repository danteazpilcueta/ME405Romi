# Imports
from pyb import ADC, ExtInt, Pin, Timer
from time import ticks_diff, ticks_us
from math import exp, pi
import cotask
import micropython
import Motor
import encoder
import ReflectanceSensorArray
import FeedbackLoop
micropython.alloc_emergency_exception_buf(1000)




# Entire robot's emergency stop
class Toggle:
    #initilize the blue button on the romi as the kill switch. Requires pin number for the button, a list of current motors and encoders, an initialized feedback loop object, and a reflectance array object
    def __init__(self,
                 button: Pin,
                 motors: Motor,
                 encoders: Encoder,
                 loops: FeedbackLoop,
                 sensArrs: ReflectSensorArray):
        self.button = button
        self.motors = motors
        self.encoders = encoders
        self.loops = loops
        self.sensArrs = sensArrs
    
    #configure the button
    def setupInterrupt(self):
        buttonInt = ExtInt(self.button, ExtInt.IRQ_FALLING, Pin.PULL_NONE, self.toggle)
    
    #turn off all motors, sensors, and encoders that are on and reset the feedback loop
    def toggle(self, line):
        turnOff = False
        for motor in self.motors:
            turnOff = turnOff or motor.En.value()
        if turnOff:
            for motor in self.motors:
                motor.disable()
            for sensArr in self.sensArrs:
                sensArr.disable()
        else:
            for motor in self.motors:
                motor.enable()
            for sensArr in self.sensArrs:
                sensArr.enable()
            for encoder in self.encoders:
                encoder.reset()
            for loop in self.loops:
                loop.reset()

# Update motors for task scheduler
class UpdateMotor:
    #intialize a motor updater. Requires a motor object, an encoder object, and a feedback loop object to be passed through
    def __init__(self,
                 mot: Motor,
                 encoder: Encoder,
                 loop: FeedbackLoop):
        self.mot   = mot
        self.enc   = encoder
        self.loop  = loop
    
    #when run, updates encoder values, calculates feedback error, and sets the motor effort based on the feedback error
    def run(self):
        while True:
            # Update encoder, feedback loop, and motor
            self.enc.update()
            self.loop.update(self.enc.velocity)
            self.mot.setEffort(self.loop.result)
            print(f"{self.loop.err}, {self.loop.intErr}, {self.loop.derErr}") # For debugging, delete later
            yield

# Update robot for task scheduler
class UpdateRobot:
    #Main robot updater to run calculations. Takes input for bump sensor pin, left motor object, right motor object, left encoder object, right encoder object, left motor feedback loop object, right motor feedback loop object, and the reflectance array object
    #additionally takes robot width, wheel radius, maximum linear velocity, maximum angular velocity, calibration location and calibration fraction
    def __init__(self,
                 wallSns: Pin,
                 motLeft: Motor,
                 motRght: Motor,
                 encLeft: Encoder,
                 encRght: Encoder,
                 fdbLeft: FeedbackLoop,
                 fdbRght: FeedbackLoop,
                 frntArr: ReflectSensorArray,
                 rearArr: ReflectSensorArray,
                 dR: float,
                 dW: float,
                 vRmax: float,
                 wRmax: float,
                 calLoc: float,
                 calFrac: float):
        # Calculate values, the details and derivation of these calculations are detailed in the read me file. 
        self.minLoc = min(frntArr.sensorPos)
        self.maxLoc = max(frntArr.sensorPos)
        aNum   = [calFrac * self.maxLoc * self.minLoc * (-self.maxLoc + self.minLoc),
                  calLoc**2 * (self.maxLoc + self.minLoc),
                  -calLoc * (self.maxLoc**2 + self.minLoc**2)]
        bNum   = [-calLoc**3 * (self.maxLoc + self.minLoc),
                  calFrac * self.maxLoc * (self.maxLoc - self.minLoc) * self.minLoc * (self.maxLoc + self.minLoc),
                  calLoc * (self.maxLoc**3 + self.minLoc**3)]
        cNum   = [calFrac * self.maxLoc**2 * self.minLoc**2 * (-self.maxLoc + self.minLoc),
                  calLoc**3 * (self.maxLoc**2 + self.minLoc**2),
                  -calLoc**2 * (self.maxLoc**3 + self.minLoc**3)]
        denPts = [calLoc * (calLoc - self.maxLoc),
                  self.maxLoc * (calLoc - self.minLoc),
                  (self.maxLoc - self.minLoc) * self.minLoc]
        den    = denPts[0] * denPts[1] * denPts[2]
        
        # Store values
        self.wallSns = Pin(wallSns, mode = Pin.IN, pull = Pin.PULL_DOWN)
        self.motLeft = motLeft # [Motor]
        self.motRght = motRght # [Motor]
        self.encLeft = encLeft # [Encoder]
        self.encRght = encRght # [Encoder]
        self.fdbLeft = fdbLeft # [FeedbackLoop]
        self.fdbRght = fdbRght # [FeedbackLoop]
        self.frntArr = frntArr # [ReflectSensorArray]
        self.rearArr = rearArr # [ReflectSensorArray]
        self.dR      = dR      # [cm]
        self.dW      = dW      # [cm]
        self.vRmax   = vRmax   # [cm/s]
        self.wRmax   = wRmax   # [rad/s]
        self.a = wRmax * sum(aNum) / den # Angular velocity equation coefficient
        self.b = wRmax * sum(bNum) / den # Angular velocity equation coefficient
        self.c = wRmax * sum(cNum) / den # Angular velocity equation coefficient
        self.state     = 1      # Task state
        self.oldPos    = [0]*20 # Previous front sensor weighted positions in mm
        self.wallState = 0      # Wall circling state
        self.wallStart = 0      # Wall circling start time in microseconds
        self.wallSpeed = pi     # Angular velocity of wheels when circling the wall
        self.wallWait  = [0.35, 1, 0.45, 1.5, 0.45, 1, 0.45] # Wall circling wait times for each state in seconds
    
    
    def run(self):
        while True:
            # Go to state to deal with the wall if the switch is pressed
            if self.wallSns.value():
                self.state = 2
                self.motLeft.disable()
                self.motRght.disable()
            
            # Line following state
            if self.state == 1:
                # Read and calibrate values
                rawVals = self.frntArr.read() # Raw reflectance sensor readings from 0 to 4095
                rawVals = rawVals[1:-1] # Left- and right-most sensors are buggy, so don't use them
                
                # Calculate values
                minVal = min(rawVals)
                vals = [each - minVal for each in rawVals] # Normalize the weighting for the position weighted average
                pos = sum([x * y for x, y in zip(self.frntArr.sensorPos[1:-1], vals)]) / sum(vals) # Position weighted average in mm
                
                # If the front array sees white, then go roughly in the same direction as previous positions
                if max(vals) <= 250:
                    pos = sum(self.oldPos) / len(self.oldPos)
                    
                    # If the positions have been consistent for a while, then go straight by setting positions to center (AKA zero)
                    diff = [abs(each - pos) for each in self.oldPos]
                    if sum(diff) <= 1:
                        self.oldPos = [0]*20
                        pos = 0
                    elif abs(pos) <= 1:
                        # Enhance turns for slight variations
                        pos = 1 if pos > 0 else -1
                
                # Continue calculating values
                wR = self.a * pos**3 + self.b * pos**2 + self.c * pos
                vR = self.vRmax * exp(-((pos / ((self.maxLoc - self.minLoc)/12))**2))
                wWL = (2 * vR - self.dR * wR) / self.dW
                wWR = (2 * vR + self.dR * wR) / self.dW
                
                # Assign values
                self.fdbLeft.ref = wWL
                self.fdbRght.ref = wWR
                
                # Store current weighted position and remove oldest weighted position
                self.oldPos.append(pos)
                self.oldPos = self.oldPos[(-len(self.oldPos) + 1):]
                
            # State to deal with the wall
            elif self.state == 2:
                # Reset
                self.encLeft.reset()
                self.encRght.reset()
                self.fdbLeft.reset()
                self.fdbRght.reset()
                self.oldPos = [0]*20
                
                # Set directions for each motion to get around the wall
                if self.wallState == 0:
                    # Turn 90 degrees right
                    self.fdbLeft.ref =  self.wallSpeed
                    self.fdbRght.ref = -self.wallSpeed
                elif self.wallState == 1:
                    # Go forward
                    self.fdbLeft.ref =  self.wallSpeed
                    self.fdbRght.ref =  self.wallSpeed
                elif self.wallState == 2:
                    # Turn 90 degrees left
                    self.fdbLeft.ref = -self.wallSpeed
                    self.fdbRght.ref =  self.wallSpeed
                elif self.wallState == 3:
                    # Go forward
                    self.fdbLeft.ref =  self.wallSpeed
                    self.fdbRght.ref =  self.wallSpeed
                elif self.wallState == 4:
                    # Turn 90 degrees left
                    self.fdbLeft.ref = -self.wallSpeed
                    self.fdbRght.ref =  self.wallSpeed
                elif self.wallState == 5:
                    # Go forward
                    self.fdbLeft.ref =  self.wallSpeed
                    self.fdbRght.ref =  self.wallSpeed
                elif self.wallState == 6:
                    # Turn 90 degrees right
                    self.fdbLeft.ref =  self.wallSpeed
                    self.fdbRght.ref = -self.wallSpeed
                
                # Go to waiting state
                self.state = 3
                self.wallStart = ticks_us()
            
            # Waiting state
            elif self.state == 3:
                # Wait until current movement has been completed for the specified amount of time
                self.wallStart = ticks_us()
                while ticks_diff(ticks_us(), self.wallStart) * 1e-6 < self.wallWait[self.wallState]:
                    yield
                
                # Go back to state 2 for the next movement around the wall
                self.state = 2
                if self.wallState < len(self.wallWait):
                    self.wallState += 1
                
                # Start line following again by going back to state 1
                if self.wallState >= len(self.wallWait):
                    self.state = 1
                    self.wallState = 0
                
            yield

if __name__ == "__main__":
    # System parameters
    efrtLim = 80   # [%], motors' saturation effort limit
    updtInt = 5    # [ms], feedback loop period and motors' update interval
    updtFrq = 5    # [#], number of motor updates per robot update
    motorKp = 2    # [% / (rad/s)], feedback loop proportional gain
    motorKi = 3    # [% / rad], feedback loop integral gain
    motorKd = 0.02 # [% / (rad/s^2)], feedback loop derivative gain
    ftSnLoc = list(range(-12, 13, 4)) # [mm], locations of sensors on front array relative to robot's center
    rbtWdth = 14.1 # [cm], distance between centers robot's wheels
    whlDmtr = 7    # [cm], diameter of robot's wheels
    vRmax   = 10   # [cm/s], robot's maximum linear velocity
    wRmax   = 10   # [rad/s], robot's maximum angular velocity
    calLoc  = 6    # [mm], calibration location for robot's angular velocity equation
    calFrac = 1/5  # [#], calibration fraction for robot's angular velocity equation
    
    # Left motor
    timLeft = Timer(3, freq = 20000)
    motLeft = Motor(timLeft, 2, Pin.cpu.A10, Pin.cpu.B5, Pin.cpu.B3, efrtLim)
    encLeft = Encoder(Pin.cpu.B6, Pin.cpu.B7, 0, 1500, 4)
    fdbLeft = FeedbackLoop(1, -efrtLim, efrtLim, 0, motorKp, motorKi, motorKd)
    motLeft.disable()
    
    # Right motor
    timRght = Timer(1, freq = 20000)
    motRght = Motor(timRght, 1, Pin.cpu.B4, Pin.cpu.A8, Pin.cpu.B10, efrtLim)
    encRght = Encoder(Pin.cpu.C6, Pin.cpu.C7, 0, 1500, 8)
    fdbRght = FeedbackLoop(1, -efrtLim, efrtLim, 0, motorKp, motorKi, motorKd)
    motRght.disable()
    
    # Front array of 7 reflectance sensors
    sensPns = [Pin.cpu.A0, Pin.cpu.A1, Pin.cpu.A4, Pin.cpu.B0, Pin.cpu.C1, Pin.cpu.C0, Pin.cpu.A5]
    frntArr = ReflectSensorArray(Pin.cpu.A9, sensPns, ftSnLoc)
    
    # Rear array of 1 reflectance sensor
    rearArr = ReflectSensorArray(Pin.cpu.A7, [Pin.cpu.B0, Pin.cpu.C1, Pin.cpu.C0], [11])
    
    # Entire robot's emergency stop
    emgStop = Toggle(Pin.cpu.C13, [motLeft, motRght], [encLeft, encRght], [fdbLeft, fdbRght], [frntArr, rearArr])
    emgStop.setupInterrupt()
    
    # Create task for updating left motor
    tskLeft = UpdateMotor(motLeft, encLeft, fdbLeft)
    tskLrun = cotask.Task(tskLeft.run, name = "Update left motor", priority = 2, period = updtInt)
    cotask.task_list.append(tskLrun)
    
    # Create task for updating right motor
    tskRght = UpdateMotor(motRght, encRght, fdbRght)
    tskRrun = cotask.Task(tskRght.run, name = "Update right motor", priority = 2, period = updtInt)
    cotask.task_list.append(tskRrun)
    
    # Create task for updating robot
    taskBot = UpdateRobot(Pin.cpu.A6, motLeft, motRght, encLeft, encRght, fdbLeft, fdbRght, frntArr, rearArr, rbtWdth, whlDmtr, vRmax, wRmax, calLoc, calFrac)
    tskBrun = cotask.Task(taskBot.run, name = "Update robot", priority = 3, period = 2 * updtFrq * updtInt)
    cotask.task_list.append(tskBrun)
    
    # Run tasks
    while True:
        try:
            cotask.task_list.pri_sched()
        except Exception as e:
            motLeft.disable()
            motRght.disable()
            print(e)
            break