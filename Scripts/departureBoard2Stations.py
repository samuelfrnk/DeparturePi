import os
import pygame
import requests
from datetime import datetime, timezone
import time

os.environ["DISPLAY"] = ":0"

STATION_ID_1 = os.getenv("STATION_ID_1", "8503000")
STATION_ID_2 = os.getenv("STATION_ID_2", "8502113")

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

font = pygame.font.Font(None, 25)
big_font = pygame.font.Font(None, 30)

API_URL = "http://transport.opendata.ch/v1/stationboard"

def fetch_stationboard(station_id):
    params = {"id": station_id, "limit": 8}
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
            bus_number = entry.get("number", "Unknown")

            if departure_str != "Unknown":
                departure_time = datetime.fromisoformat(departure_str)
                departure_time_local = departure_time.astimezone()
                time_diff = departure_time_local - current_time
                remaining_minutes = max(0, time_diff.total_seconds() // 60)
                formatted_time = f"{int(remaining_minutes)}'"
                if delay:
                    remaining_minutes += delay
                    formatted_time = f"{int(remaining_minutes)}'"
                departures.append((remaining_minutes, f"{bus_number}    {destination}         {formatted_time}"))
            else:
                departures.append((float('inf'), f"Bus {bus_number} to {destination}: Time unknown (Delay: {delay} min)"))
        return departures, station_name
    else:
        return [(float('inf'), "Error fetching data")], "Unknown Station"
def clean_station_name(name):
	return name.replace("Zürich, ", "") if name.startswith("Zürich, ") else name

running = True
while running:
    screen.fill((0, 0, 0))  
    
    
    departures_1, station_name_1 = fetch_stationboard(STATION_ID_1)
    departures_2, station_name_2 = fetch_stationboard(STATION_ID_2)
    
    
    all_departures = departures_1 + departures_2
    all_departures.sort(key=lambda x: x[0])  
    
    
    y_offset = 20
    cleaned_station_name_1 = clean_station_name(station_name_1)
    cleaned_station_name_2 = clean_station_name(station_name_2)

    station_names_text = big_font.render(f"{cleaned_station_name_1} & {cleaned_station_name_2}", True, (128, 128, 128))
    screen.blit(station_names_text, (50, y_offset))
    y_offset += 40
    screen_width = screen.get_width()
    
    for _, departure in all_departures:
        parts = departure.split("         ")
        left_text = parts[0] if len(parts) > 0 else ""
        left_surface = font.render(left_text, True, (255, 165, 0))
        right_text = parts[1] if len(parts) > 1 else ""
        right_surface = font.render(right_text, True, (255, 165, 0))
        left_x_position = 50
        right_width = right_surface.get_width()
        right_x_position = screen_width - right_width - 50
        screen.blit(left_surface, (left_x_position, y_offset))
        screen.blit(right_surface, (right_x_position, y_offset))
        y_offset += 30
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    time.sleep(15)

pygame.quit()
