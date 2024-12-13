webserver-python-api

The main purpose of the project its to be a device that catches the sensor's data and send it to an API, the API by its self storage and checks if the pressure meets the requirements.
In the API we have a route to check the device, in this route we check if the device is already registered in the database, if not, the API return the '401' status.
In the client side, the API checks if the user is registered, if not gives back the same status (401).
After the login, the client granted the access to see the logs of the devices, register a new device or user, change password, disable the device, and update the standard pressure of which device that is already registered.

The API has a route description, that is in 'sensorLogAPI.yaml' archive.
Its already ready for a docker build and has a docker compose file to take the services in a container.
In the archives, has a dump to restore the database.
To make the first access, its important to manually insert a register in the user's table, its important to freeze the password its encrypted by the library bcrypt, so you must insert a password encrypted, the username its encrypted by the jwt library, taking only the second hash.

In the IOT device side, its a Arduino program, the device will check if has a USB drive to read the standard settings, like the standard pressure and wifi, and also will log all the sensor's data.
The device has a pattern to show its logging mode, if the USB drive its not connected the program will use the device standard (vars in the program).
After checking all the data, the device will search for the server, and will compare the standard to the server standard, if has some change, the program will use the server standard, and check the pressure in the sensors that is connected.
