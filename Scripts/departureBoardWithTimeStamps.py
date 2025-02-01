import os
import pygame
import requests
from datetime import datetime, timezone, timedelta
import time


os.environ["DISPLAY"] = ":0"

STATION_ID = os.getenv("STATION_ID", "8591175")

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

font = pygame.font.Font(None, 25)  
big_font = pygame.font.Font(None, 30)

API_URL = "http://transport.opendata.ch/v1/stationboard"

def fetch_stationboard():
    params = {"id": STATION_ID, "limit": 8}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        stationboard = data.get("stationboard", [])
        departures = []
        station_name = data.get("station", {}).get("name", "Unknown")

        current_time = datetime.now(timezone.utc).astimezone()

        for entry in stationboard:
            destination = entry.get("to", "Unknown")
            departure_str = entry.get("stop", {}).get("departure", "Unknown")
            delay = entry.get("stop", {}).get("delay", 0)
            bus_number = entry.get("number", "Unknown")  # Extract bus number

            if departure_str != "Unknown":
                departure_time = datetime.fromisoformat(departure_str)
                departure_time_local = departure_time.astimezone()  

                # Format the departure time to "HH:MM"
                formatted_time = departure_time_local.strftime("%H:%M")

                # Add delay to departure time
                if delay:
                    departure_time_local += timedelta(minutes=delay)
                    formatted_time = departure_time_local.strftime("%H:%M")

                departures.append(f"{bus_number}    {destination}		 {formatted_time}")
            else:
                departures.append(f"Bus {bus_number} to {destination}: Time unknown (Delay: {delay} min)")

        return departures, station_name
    else:
        return ["Error fetching data"], "Unknown Station"


running = True
while running:
    
    departures, station_name = fetch_stationboard()

    
    screen.fill((0, 0, 0))  # Black background

    
    title_text = big_font.render(station_name, True, (128, 128, 128))  # Orange title
    screen.blit(title_text, (50, 20))

    
    y_offset = 60
    screen_width = screen.get_width()  
    for departure in departures:
       
        parts = departure.split("		 ") 

        # Render left part (bus number + destination)
        left_text = parts[0] if len(parts) > 0 else ""
        left_surface = font.render(left_text, True, (255, 165, 0))  # Orange color

        # Render right part (departure time)
        right_text = parts[1] if len(parts) > 1 else ""
        right_surface = font.render(right_text, True, (255, 165, 0))  # Orange color

        # Calculate the width of the left text and position it at the left side
        left_width = left_surface.get_width()
        left_x_position = 50  # Fixed padding from the left edge

        # Calculate the width of the right text and position it on the right side
        right_width = right_surface.get_width()
        right_x_position = screen_width - right_width - 50  # 50 pixels padding from the right

        # Display left and right parts
        screen.blit(left_surface, (left_x_position, y_offset))
        screen.blit(right_surface, (right_x_position, y_offset))

        # Increment y_offset for the next line
        y_offset += 30

    
    pygame.display.update()

    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    
    time.sleep(60)

pygame.quit()
