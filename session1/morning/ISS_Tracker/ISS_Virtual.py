import pygame
import requests
import math
import time
from datetime import datetime

# --- Config ---
WIDTH, HEIGHT = 1000, 750
MARK_SIZE = 10
MARK_COLOR = (255, 48, 48)
TRAIL_COLOR = (255, 255, 0)
DATE_COLOR = (30, 30, 30)
LAT_MAX = 80  # Mercator projection can't show poles properly
UPDATE_RATE = 10  # seconds
TRAIL_LENGTH = 200
MAP_IMAGE_PATH = "map.png"  # Must be 320x240 Mercator projection

API_URL = "http://api.open-notify.org/iss-now.json"

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ISS Tracker")
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()

# Load map
try:
    earth_img = pygame.image.load(MAP_IMAGE_PATH)
    if earth_img.get_size() != (WIDTH, HEIGHT):
        raise ValueError("Map image wrong size")
except Exception as e:
    raise FileNotFoundError(f"Error loading map image: {e}")

trail = []

def get_iss_location():
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        return lat, lon
    except Exception as e:
        print(f"Error fetching ISS data: {e}")
        return None, None

def convert_to_screen(lat, lon):
    # Clamp latitude to prevent infinite values near poles
    lat = max(min(lat, LAT_MAX), -LAT_MAX)
    
    # Convert longitude (-180 to 180) to x (0 to WIDTH)
    x = (lon + 180) * (WIDTH / 360)
    
    # Convert latitude to Mercator projection y
    lat_rad = math.radians(lat)
    merc_n = math.log(math.tan(math.pi/4 + lat_rad/2))
    y = HEIGHT/2 - (HEIGHT * merc_n) / (2 * math.pi)
    
    # Ensure coordinates stay within screen bounds
    x = max(0, min(WIDTH-1, x))
    y = max(0, min(HEIGHT-1, y))
    
    return int(x), int(y)

def draw_marker(x, y):
    pygame.draw.circle(screen, MARK_COLOR, (x, y), MARK_SIZE, width=3)

def draw_trail(trail_points):
    if len(trail_points) >= 2:
        pygame.draw.lines(screen, TRAIL_COLOR, False, trail_points, 2)

def draw_time_and_date():
    now = datetime.now()
    date_text = font.render(now.strftime("%Y-%m-%d"), True, DATE_COLOR)
    time_text = font.render(now.strftime("%H:%M:%S"), True, DATE_COLOR)
    screen.blit(date_text, (165, 223))
    screen.blit(time_text, (240, 223))

# --- Main Loop ---
last_update = 0
current_pos = None

running = True
while running:
    screen.blit(earth_img, (0, 0))

    now = time.time()
    if now - last_update > UPDATE_RATE:
        lat, lon = get_iss_location()
        if lat is not None and lon is not None:
            x, y = convert_to_screen(lat, lon)
            current_pos = (x, y)
            trail.append((x, y))
            if len(trail) > TRAIL_LENGTH:
                trail.pop(0)
        last_update = now

    draw_trail(trail)
    if current_pos:
        draw_marker(*current_pos)
    draw_time_and_date()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()