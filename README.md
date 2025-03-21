# DeparturePi
This Repository Contains the software for creating a departure board for any train/tram or bus station within Switzerland using a Raspberry Pi and a compatible screen.

![image](https://github.com/user-attachments/assets/f003e030-1776-409f-8110-e5129b3912b0)

## Setup 

1. Connect the screen with the Raspberry Pi ([instructions](Instructions/Screen.txt))
2. Paste one of [the scripts](Scripts) into a directory on the Pi.
3. Set the environment variable 'STATION_ID' towards the value of the ID corresponding to the desired station (GET http://transport.opendata.ch/v1/locations?query=Basel helps to identify the ID).
4. Create a cronjob: `@reboot sleep 120 && export STATION_ID="desired ID" && /usr/bin/python3 /home/pi/path/to/depBoardMin.py >> /home/pi/cron.log 2>&1` such that the board boots at start up of the Pi.
 



 
## Hardware 
This subsection lists the hardware used. 

### Raspberry Pi 
The Raspberry Pi 3 model B+ was used for this project. The latest 64-bit version of the bookworm Raspberian OS was used for the operating system. 

<img src="https://github.com/user-attachments/assets/7208d5f6-3d73-4edd-b1d3-91b50f1cc50e" width="350">

### Screeen  

A 3.5 inch model with an LCD SPI interface was used for the screen.  The image, touchscreen and power supply function via the GPIO pins. It was bought [here on BerryBase](https://www.berrybase.ch/3-5-display-fuer-raspberry-pi-mit-resistivem-touchscreen).

<img src="https://github.com/user-attachments/assets/41912d4c-da8a-4623-9e54-fcc54ca22491" width="350">

### Case 

In order to have all the hardware packed in a handy way, a case was chosen which contains the Pi and the screen at the same time. The case was bought from BerryBase and can be found [here](https://www.berrybase.ch/gehaeuse-fuer-raspberry-pi-3-3b-und-3-5-display-schwarz).

<img src="https://github.com/user-attachments/assets/943d5809-fa1b-480e-9261-cd4498d070c5" width="350">


## Software

### API 

As an underlying API the [opendata Transport API](https://transport.opendata.ch/docs.html) was used. It provides an endoint which affords to query for an ID according to every bus and trainstation within Switzerland.

### Screen 

Connecting the screen to the Pi was difficult. Many tutorials were not helpful. [This Reddit](https://www.reddit.com/r/raspberry_pi/comments/1bnav0y/i_finally_have_the_35inch_gpio_spi_lcd_working/) post then gave the right [instructions](Instructions/Screen.txt).

### Scripts 

1. [This script](Scripts/departureBoardWithMin.py) performs a request every 15 seconds and displays the departures in minutes (e.g., 5') until departure. 
2. [This script](Scripts/departureBoardWithMin.py) performs a request every 30 seconds and displays the departures in timestamps (e.g., 18:30) until departure.
2. [This script](Scripts/departureBoard2Stations.py) performs a request every 15 seconds and displays the departures in timestamps (e.g., 18:30) until departure. It enables the use of two stations parallel. This however requires to add two env variables 'STATION_ID_1' 'STATION_ID_2' into the cronjob.























