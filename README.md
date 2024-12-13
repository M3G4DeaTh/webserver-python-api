webserver-python-api

The main purpose of the project its to be a device that catches the sensor's data and send it to an API, the API by itself storage and checks if the pressure meets the requirements.
In the API we have a route to check the device, in this route we check if the device is already registered in the database, if not, the API return the '401' status.
In the client side, the API checks if the user is registered, if not gives back the same status (401).
After the login, the client granted the access to see the logs of the devices, register a new device or user, change password, disable the device, and update the standard pressure of which device that is already registered.
> [!NOTE]
> The API has a route description, that is in 'sensorLogAPI.yaml' archive.

> [!NOTE]
> Its already ready for a docker build and has a docker compose file to take the services in a container.

> [!NOTE] 
> In the archives, has a dump to restore the database.

> [!IMPORTANT]
> To make the first access, its important to manually insert a register in the user's table, its important to freeze the password its encrypted by the library bcrypt, so you must insert a password encrypted, the username its encrypted by the jwt library, taking only the second hash.

In the IOT device side, its a Arduino program, the device will check if has a USB drive to read the standard settings, like the standard pressure and wifi, and also will log all the sensor's data.
The device has a pattern to show its logging mode, if the USB drive its not connected the program will use the device standard (vars in the program).
After checking all the data, the device will search for the server, and will compare the standard to the server standard, if has some change, the program will use the server standard, and check the pressure in the sensors that is connected.

## How to run the application

First, you have to configure the IOT device, in that case we are using a OPTA by Finder, make sure that you connected the device in a source 24v and connected the sensors.

### Building the IOT app

Install the Arduino program in your machine and open 'main.ino' file in Arduino, after that, install the libraries Arduino_UnifiedStorage, ArduinoHttpClient and RS485, compile and upload your program to the device using a C cable.

> [!IMPORTANT]
> In the file 'arduino_secrets.h' define your wifi ssid, password and the host (in that case we will use a localhost one, than put your computer's ip adress with the 80 port), dont worry about tag and key, we'll set up later.

