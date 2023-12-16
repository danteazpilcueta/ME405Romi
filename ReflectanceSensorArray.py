from pyb import ADC, Pin

# Reflectance sensor array driver
class ReflectSensorArray:
    #initializes a single reflectance sensor. Single pin input for data, 1 enable pin, number of sensor on array
    def __init__(self,
                 EnPin: Pin,
                 sensorPins: Pin,
                 sensorPos: int):
        self.En = Pin(EnPin, mode = Pin.OUT_PP)
        self.sensors    = []
        for pin in sensorPins:
            self.sensors.append(ADC(pin))
        self.sensorPos  = sensorPos
        self.enable()
    
    #Compile data from all sensors in a single array and return it
    def read(self):
        vals = []
        for sensor in self.sensors:
            vals.append(sensor.read())
        return vals
    
    #enable the reflectance sensors
    def enable(self):
        self.En.high()
    
    #disable the reflectance sensors
    def disable(self):
        self.En.low()