# ME405Romi

<img width="280" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/8e0b24fc-4d8f-4719-aa1f-3cbce11d7065">

# Challenge Statement
This code is intended to allow the romi to autonomously travel from the start line to the finish line on the following track while following the black line. The robot must then make its way back to the start.

<img width="508" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/681e7036-03b6-41a1-ad1a-17d01de2f549">


# Mechanical And Electrical Design:
Hardware Used:

Bump sensor:

<img width="486" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/b0798f74-07a5-4cc0-90ae-6edb1e82e8f0">

Reflectance Sensor front:

<img width="621" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/dc6dce64-26e6-4e9a-9c4a-af41f4047346">

Reflectance sensor rear:

<img width="619" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/d88d9389-548d-4b5e-acdd-6889a7b75596">


Romi:

<img width="482" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/05005833-971f-4511-aa9a-9d69a3da0471">

Front Sensor Mount(3D printed; Files in repository):

<img width="718" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/a3563ead-d874-453a-884a-83ccc514232d">

IMU: Bno055:

<img width="976" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/98b543f3-d0fc-4c4d-b316-4f852099de4b">


# Electrical pinouts:

<img width="523" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/e215202c-36c0-439c-9f3d-ba34b19bb6c5">

<img width="520" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/aafda54f-8511-4a21-a191-a4919f4643b1">

<img width="522" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/a8a71b60-9146-488e-b369-ef74da8c2ff0">


![image](https://github.com/danteazpilcueta/ME405Romi/assets/25334862/69f88d9a-24f6-4290-8bb1-4494dc8442b4)






# IMU Driver Commands and Documentation:

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


# Tasks
<img width="346" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/c00e6fc8-f153-462b-acf5-6ca0fc9e711d">
There are 3 tasks that are being run together using cotask. Left motor and right motor update check and update the encoders and the closed loop function when they are run. They additionally used the closed loop function data to set the motors to the appropriate speed. Update robot reads the reflectance sensor array and uses our formulas to turn that into a speed for each motor that is then set as the reference value for the feedback loop controller. Our code does not use task share variables and instead calls functions to set values when needed. For example, the updaterobot task can influence the updatemotor task because it can call the closed loop function to set the reference velocity. 


# Finite State Machine
Update robot is the only task that uses a FSM.

<img width="512" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/613f9dd4-e185-4c3e-90be-8d40c8ac80ba">

We could not get the finish line detection and wall navigation to work concurrently with the line follower so in the final code this is unimplemented. The intention was for state 2 to be triggered by the switch on the front of the robot and for state 3 to be triggered by a value above a certain threshold in the rear reflectance array. The wall trigger works but the state remains unimplemented. The rear reflectance array was too volitile to be a reliable way to detect the finish line as it was too far up above the play field. 



# Motor Feedback Control
The motors are controlled entirely through the feedback controllers. Any code in other sections that changes the motors speed does so by changing the velocity setpoint of the feedback loop itself. The feedback loops all incorporate proportional, integral and derivative control and the gains for each are chosen on initialization. Although derivative control is supported in the code, its gain is extremely low as the high variance in the error due to noisy sensors causes undesirable instability in line following. Motor feedback requires the initialization of an encoder object to compare measured speed to reference speed. 

# Line Follower Calculations:
The following equations were created via analysis of the robots movement due to the 2 motors. These equations were used to create plots of velocities to use for the 2 motors to best follow the lines. 

<img width="1059" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/ceb8a77e-6098-447a-9602-12bfe8a636a3">

<img width="1118" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/52f0e026-7309-4803-b1eb-178d0df3d7a6">

<img width="1150" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/7ba5ef9c-8eeb-4035-83ec-7574e5695b5b">

The reflectance sensors give us 5 different values for equally spaced out spots on the front of the robot. By weighting each value and compiling them together we created a single term that could be used to tell the motor how hard to go and which way to go. Below is a plot that shows how these distances were turned into values for the robot
<img width="610" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/5481b0b2-f17f-4f0b-a80e-8684bbd8295a">

Small values result in small turning adjustments but the adjustments scale up quickly as the value gets larger so we push significantly harder when we are further of the line. 
This plot shows how that information is turned into 2 different speeds, one for each motor, that will result in the desired movement.

<img width="624" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/610a628b-e5e5-478f-8fb3-92546b15e0a8">

Each colored line corresponds to a different calibration setting allowing us to choose between multiple different behavior profiles. At a given value there are 2 corresponding lines of a single color which correspond to the values needed for each motor. Any time where our input is not zero we have are normal forward speed in both motors. This causes no turn and happens when the reflectance sensor does not see more of the line on one side. As soon as the sensors start to see more of the line on one side, we get a nonzero input. This results in 1 motor moving faster then the other which results in us turning in the appropriate direction. We selected the red curve as it performed the best. 

The last plot shows forward velocity with respect to our weighted input from the sensors.

<img width="552" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/9e2b1adc-830c-4ba1-803d-6c184dab7840">

As the sensors start to give higher values, the speed falls off accordingly. This allows us to hit sharper turns without driving past them. We selected the red curve as the sharp drop off was needed in order for us to hit the sharp turns. 

Using wolfram alpha, the equations were rearranged so that they could be solved for 3 calibration constants. These calibration constants are implemented in our code and by changing them we change the equation that governs the above plots. This allows us to tweak behavior in the code easily with few inputs. The cabration constants are shown below and are also documented in the code. 

<img width="1131" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/5a53fa60-145f-49be-a759-92bd93b47ccf">



# Robot Running and Line Following Protocol: 
Both motors are set by default to their max speed. Rather then increase speed when needed, we decrease speed instead. 
When one sensor starts to see black that means that that side of the robot is begining to cross the line. To fix this, the motor on that side slows down inducing a turn.  
This also means that for short gaps the robot continues straight at full speed. The short gap is not enough time for any significant drift to occur so it continues right on course after hitting the line again. 
For the branch segments, both motors see black at the same time and slow the same amount meaning there is no turn induced and the robot continues straight. Only the 5 inner sensors of the 7 sensor array are being used. The 2 outer sensors were very sensitive to outside light and resulted in more erratic reads and as such they are ignored by the code. 

https://github.com/danteazpilcueta/ME405Romi/assets/25334862/17d52362-d03a-4e68-ba87-83cca5522bbb

# Wall Avoiding Protocol
We use a single levered switch on the front of the robot to detect when we have run into the wall. Upon collision, the robot stops and backs up a small distance before turning and traveling a preprogrammed arc around the wall. Sensors are turned off during this time to prevent the robot from accidentally jumping onto another point on the track. Once the robot has traveled most of the path, the sensors are renabled to track back onto the line. In the video below this is shown. The movements after collision are hardcoded and have not been adjusted to most efficiently manuever around the box. 


https://github.com/danteazpilcueta/ME405Romi/assets/25334862/66551163-b3ae-472f-b0eb-9130f963eb91

This wall detection and avoidance code was not implemented into the rest of the code in time for the demo. It is included below to show the method used.

<img width="544" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/f3e34b48-8463-4fe6-ba4d-8de7ec8aa016">
<img width="587" alt="image" src="https://github.com/danteazpilcueta/ME405Romi/assets/25334862/129f91be-f254-4de2-8f35-05c2c41ebb74">

During these movements the robot moves slowly to ensure accuracy. Encoder ticks are counted to get a measurement of how far we have turned and moved to allow us to choose movements that get us around the box. 



# Finish line detection
We have a secondary reflectance sensor mounted a few inches to the left of the romi. It is offset far enough that it cannot see the pronged paths and will only trigger when it sees the box for the finish line. If this sensor sees black then that means that the back of the robot has reached the finish line. The robot then moves a small amount forward and turns around. It will then find the path again and follow the line back. When starting the sensor will also see the line of the starting box. To prevent this from effecting the robot, the control pin is turned off for the begining part of the journey. Initially we planned to use the IMU euler angles and acceleration in order to integrate a forward position and break it into x and y components but we believe this to be a bit more reliable and less prone to estimation errors. 

# Return Journey
To return back to the starting position, our robot simply follows the line back the way it came. It uses the same code and protocol on the way back. 

# Other Sources
The cotask file is necessary to run the main program and is included in this repository. This was not created by us and was provided by Cal Poly SLO.








