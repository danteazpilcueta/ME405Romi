import ustruct
from pyb import I2C, Pin
from time import sleep_ms
import os

class IMU:
    #the Driver requires a configured I2C object to be passed through along with the relevant hardware address
    def __init__(self, i2c, add):
        self.i2c = i2c
        self.add = add
        
       
    def setmode(self, mode):
        if mode in ['IMU', 'imu', 'Compass', 'compass', 'COMPASS','M4G', 'NDOF_FMC_OFF', 'NDOF','ONLYGYR']:
            #writes the mode bit corresponding to the passed through variable into the opperating mode register
            I2C.mem_write(0x00, 0x28, 0x3D)
            if mode in ['ONLYGYR']:
                self.i2c.mem_write(0x03, self.add, 0x3D)
            if mode in ['IMU', 'imu']:
                self.i2c.mem_write(0x08, self.add, 0x3D)
            if mode in ['Compass', 'compass', 'COMPASS']:
                self.i2c.mem_write(0b00001001, self.add, 0x3D)
           
            if mode in ['M4G']:
                self.i2c.mem_write(0x0A, self.add, 0x3D) 
            if mode in ['NDOF_FMC_OFF']:
                self.i2c.mem_write(0x0B, self.add, 0x3D) 
            if mode in ['NDOF']:
                self.i2c.mem_write(0x0C, self.add, 0x3D) 
            print('mode switched')
        else:
            print('Invalid; Enter IMU, Compass, M4G, NDOF_FMC_OFF, or NDOF')
            
    def getvel(self):
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x14)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x15)
        Value = bytearray(2)
        Value[0] = MSB[0]
        Value[1] = LSB[0]
     
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x16)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x17)
        Value2 = bytearray(2)
        Value2[0] = MSB[0]
        Value2[1] = LSB[0]
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x18)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x19)
        Value3 = bytearray(2)
        Value3[0] = MSB[0]
        Value3[1] = LSB[0]
        
        Printed = [ustruct.unpack('>h', Value)[0]/900, ustruct.unpack('>h', Value2)[0]/900, ustruct.unpack('>h', Value3)[0]/900]
        return Printed
    
    
    
    def getacc(self):
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x08)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x09)
        Value = bytearray(2)
        Value[0] = MSB[0]
        Value[1] = LSB[0]
     
        
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x0A)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x0B)
        Value2 = bytearray(2)
        Value2[0] = MSB[0]
        Value2[1] = LSB[0]
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x0C)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x0D)
        Value3 = bytearray(2)
        Value3[0] = MSB[0]
        Value3[1] = LSB[0]
        
        Printed = [ustruct.unpack('>h', Value)[0]/100, ustruct.unpack('>h', Value2)[0]/100, ustruct.unpack('>h', Value3)[0]/100]
        return Printed
    
    def Mag(self):
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x0E)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x0F)
        Value = bytearray(2)
        Value[0] = MSB[0]
        Value[1] = LSB[0]
     
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x10)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x11)
        Value2 = bytearray(2)
        Value2[0] = MSB[0]
        Value2[1] = LSB[0]
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x12)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x13)
        Value3 = bytearray(2)
        Value3[0] = MSB[0]
        Value3[1] = LSB[0]
        
        Printed = [int.from_bytes(Value, 'big', True)/900, int.from_bytes(Value2, 'big', True)/900, int.from_bytes(Value3, 'big', True)/900]
        return Printed
        
    def getEUL(self):
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x1A)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x1B)
        Value = bytearray(2)
        Value[0] = MSB[0]
        Value[1] = LSB[0]

        
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x1C)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x1D)
        Value2 = bytearray(2)
        Value2[0] = MSB[0]
        Value2[1] = LSB[0]
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x1E)
        MSB = bytearray(1)
        MSB = self.i2c.mem_read(MSB, self.add, 0x1F)
        Value3 = bytearray(2)
        Value3[0] = MSB[0]
        Value3[1] = LSB[0]
        
        Printed = [ustruct.unpack('>h', Value)[0]/900, ustruct.unpack('>h', Value2)[0]/900, ustruct.unpack('>h', Value3)[0]/900]
        return Printed
        
    def Calibstatus(self):
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x35)
        bins = LSB[0]
        if bins & 0b00000001:
            bit1 = 1
        else:
            bit1 = 0
            
        if bins & 0b00000010:
            bit2 = 1
        else:
            bit2 = 0
            
        calib1 = ((bit2 << 1) + bit1)


        if bins & 0b00000100:
            bit1 = 1
        else:
            bit1 = 0
            
        if bins & 0b00001000:
            bit2 = 1
        else:
            bit2 = 0
            
        calib2 = ((bit2 << 1) + bit1)

        if bins & 0b00010000:
            bit1 = 1
        else:
            bit1 = 0
            
        if bins & 0b00100000:
            bit2 = 1
        else:
            bit2 = 0

        calib3 = ((bit2 << 1) + bit1)


        if bins & 0b01000000:
            bit1 = 1
        else:
            bit1 = 0
            
        if bins & 0b10000000:
            bit2 = 1
        else:
            bit2 = 0

        calib4 = ((bit2 << 1) + bit1)
        return calib1, calib2, calib3, calib4
        #must be split into 4 sections per each 2 bit section. Works otherwwise
        
    def getcalib(self):
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x55)
        Val1 = LSB
  
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x56)
        Val2 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x57)
        Val3 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x58)
        Val4 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x59)
        Val5 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x5A)
        Val6 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x5B)
        Val7 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x5C)
        Val8 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x5D)
        Val9 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x5E)
        Val10 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x5F)
        Val11 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x60)
        Val12 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x61)
        Val13 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x62)
        Val14 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x63)
        Val15 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x64)
        Val16 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x65)
        Val17 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x66)
        Val18 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x67)
        Val19 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x68)
        Val20 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x69)
        Val21 = LSB
        
        LSB = bytearray(1)
        LSB = self.i2c.mem_read(LSB, self.add, 0x6A)
        Val22 = LSB
        Printed = [Val1[0], Val2[0], Val3[0], Val4[0], Val5[0], Val6[0], Val7[0], Val8[0], Val9[0], Val10[0], Val11[0], Val12[0], Val13[0], Val14[0], Val15[0], Val16[0], Val17[0], Val18[0], Val19[0], Val20[0], Val21[0], Val22[0]]
        return Printed
        
    def precalib(self):
        self.i2c.mem_write(0x03, self.add, 0x00)
        f = open('calibs.txt', 'r')
        parse = f.read()
        f.close()
        val = ''
        values = []
        for each in parse:
            if each not in ['[', ']']:
                if each not in [',']:
                    val +=each
                  
                else:
                    values.append(val)
                    val = ''
        for each in range(len(values)):
            values[each] = hex(int(values[each]))
        
        
        self.i2c.mem_write(values[0], self.add, 0x55)
        self.i2c.mem_write(values[1], self.add, 0x56)
        self.i2c.mem_write(values[2], self.add, 0x57)
        self.i2c.mem_write(values[0], self.add, 0x58)
        self.i2c.mem_write(values[1], self.add, 0x59)
        self.i2c.mem_write(values[2], self.add, 0x5A)
        self.i2c.mem_write(values[0], self.add, 0x5B)
        self.i2c.mem_write(values[1], self.add, 0x5C)
        self.i2c.mem_write(values[2], self.add, 0x5D)
        self.i2c.mem_write(values[0], self.add, 0x5E)
        self.i2c.mem_write(values[1], self.add, 0x5F)
        self.i2c.mem_write(values[2], self.add, 0x60)
        self.i2c.mem_write(values[0], self.add, 0x61)
        self.i2c.mem_write(values[1], self.add, 0x62)
        self.i2c.mem_write(values[2], self.add, 0x63)
        self.i2c.mem_write(values[0], self.add, 0x64)
        self.i2c.mem_write(values[1], self.add, 0x65)
        self.i2c.mem_write(values[2], self.add, 0x66)
        self.i2c.mem_write(values[0], self.add, 0x67)
        self.i2c.mem_write(values[1], self.add, 0x68)
        self.i2c.mem_write(values[2], self.add, 0x69)
        self.i2c.mem_write(values[0], self.add, 0x6A)
        self.i2c.mem_write(0x0C, self.add, 0x3D) 
        print('mode switched to NDOF, calibrated')
       
