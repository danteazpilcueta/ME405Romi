# ME405Romi


#Mechanical And Electrical Design:
Hardware Used:

Bump sensor:

<img width="486" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/b0798f74-07a5-4cc0-90ae-6edb1e82e8f0">

Reflectance Sensor:

<img width="621" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/dc6dce64-26e6-4e9a-9c4a-af41f4047346">

Romi:

<img width="482" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/05005833-971f-4511-aa9a-9d69a3da0471">

Front Sensor Mount(3D printed; Files in repository):

<img width="718" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/a3563ead-d874-453a-884a-83ccc514232d">

IMU: Bno055:

<img width="976" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/98b543f3-d0fc-4c4d-b316-4f852099de4b">


Electrical pinouts:

<img width="523" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/e215202c-36c0-439c-9f3d-ba34b19bb6c5">

<img width="520" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/aafda54f-8511-4a21-a191-a4919f4643b1">



IMU Driver Commands and Documentation:

<img width="166" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/db3b533e-76b6-4583-9760-907e712edaac">
This command is used to initialize the IMU object. It requires an I2C object to be created and configured outside of the driver. The configured driver and the hardware address of the device must be passed through for initilization

<img width="142" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/d5ce7eb2-90c6-4f2c-b38b-18df03b6d92d">
This command changes the opperating mode. It takes a string as its input. If the string is within the list ['IMU', 'imu', 'Compass', 'compass', 'COMPASS','M4G', 'NDOF_FMC_OFF', 'NDOF','ONLYGYR'] then it switches the imu to the relevant mode

<img width="101" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/720150d3-1a8b-46e5-8764-0c3b96624531">
This requires no arguement and simply returns the current x y and z signed angular velocities as a 3 value list

<img width="96" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/3a5b3e22-348a-40d9-b1bb-a7632237d588">
This requires no arguement and simply returns the current x y and z signed accelerations as a 3 value list

<img width="85" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/e5cf407f-af53-43f2-aeb7-beeda40ce312">
This requires no arguement and simply returns the current x y and z signed magnetic field readings as a 3 value list

<img width="99" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/aab456d4-d909-4800-bf54-bb5440f97233">
This requires no arguement and simply returns the current x y and z signed euler angle readings as a 3 value list

<img width="130" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/a3ba5abb-af56-4da7-a7b6-8eb6c2b695f9">
This requires no arguement and simply returns the current 4 calibration status bits. when all 4 bits are 3, the device is calibrated

<img width="113" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/ede0031c-6d9c-44f9-af17-8589c6b5e690">
This requires no arguement and simply returns the 22 calibration constants as a list

<img width="112" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/0003d47a-1a9f-40cd-81ca-1972b45cfa3e">
Calibrates the romi directly from a file. Must have a file on the device named calibs.txt which must contain a list of the values in order












