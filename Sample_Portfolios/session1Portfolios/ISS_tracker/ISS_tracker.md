# International Space Station Tracker

This project utilzies a pyportal which is an internet-capable microcontroller with a built in screen. The code calls an API that actively tracks the space station position to yield a latitude and longitude coordinate pair which then was mapped to x-y coordinates on a mercator projection. It also tracks the path of the space station as it orbits the earth every 90 or so minutes. The greatest challenge I faced was getting acquainted with the Pyportal's libraries and capabilities which was overcome just by scouring the documentation :(

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| Josh M | Cooper Union | Electrical Engineering | Incoming Junior |

![Headstone Image](ISS_tracker.png)
  
# Final Milestone

<iframe width="485" height="862" src="https://www.youtube.com/embed/HKJfoPRewhY" title="BlueStamp Engineering International Space Station Tracker" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

For your final milestone, explain the outcome of your project. Key details to include are:
- What you've accomplished since your previous milestone
- What your biggest challenges and triumphs were at BSE
- A summary of key topics you learned about
- What you hope to learn in the future after everything you've learned at BSE



# Second Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

<iframe width="560" height="315" src="https://www.youtube.com/embed/y3VAmNlER5Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your second milestone, explain what you've worked on since your previous milestone. You can highlight:
- Technical details of what you've accomplished and how they contribute to the final goal
- What has been surprising about the project so far
- Previous challenges you faced that you overcame
- What needs to be completed before your final milestone 

# First Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

<iframe width="560" height="315" src="https://www.youtube.com/embed/CaCazFBhYKs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your first milestone, describe what your project is and how you plan to build it. You can include:
- An explanation about the different components of your project and how they will all integrate together
- Technical progress you've made so far
- Challenges you're facing and solving in your future milestones
- What your plan is to complete your project

# Schematics 
Here's where you'll put images of your schematics. [Tinkercad](https://www.tinkercad.com/blog/official-guide-to-tinkercad-circuits) and [Fritzing](https://fritzing.org/learning/) are both great resoruces to create professional schematic diagrams, though BSE recommends Tinkercad becuase it can be done easily and for free in the browser. 

# Code
Here's where you'll put your code. The syntax below places it into a block of code. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize it to your project needs. 

Here is the main code.py executable:
```python
# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import math
import board
import displayio
from terminalio import FONT
from adafruit_pyportal import PyPortal
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label

#--| USER CONFIG |--------------------------
MARK_SIZE = 10           # marker radius
MARK_COLOR = 0xFF3030    # marker color
MARK_THICKNESS = 5       # marker thickness
TRAIL_LENGTH = 200       # trail length
TRAIL_COLOR = 0xFFFF00   # trail color
DATE_COLOR = 0x111111    # date color
TIME_COLOR = 0x111111    # time color
LAT_MAX = 80             # latitude (deg) of map top/bottom edge
UPDATE_RATE = 10         # update rate in seconds
#-------------------------------------------

DATA_SOURCE = "http://api.open-notify.org/iss-now.json"
DATA_LOCATION = ["iss_position"]

WIDTH = board.DISPLAY.width
HEIGHT = board.DISPLAY.height

# determine the current working directory needed so we know where to find files
cwd = ("/"+__file__).rsplit('/', 1)[0]
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    text_font=None,
                    default_bg=cwd+"/map.bmp")

# Connect to the internet and get local time
pyportal.get_local_time()

# Date and time label
date_label = Label(FONT, text="0000-00-00", color=DATE_COLOR, x=165, y=223)
time_label = Label(FONT, text="00:00:00", color=TIME_COLOR, x=240, y=223)
pyportal.splash.append(date_label)
pyportal.splash.append(time_label)

# ISS trail
trail_bitmap = displayio.Bitmap(3, 3, 1)
trail_palette = displayio.Palette(1)
trail_palette[0] = TRAIL_COLOR
trail = displayio.Group()
pyportal.splash.append(trail)

# ISS location marker
marker = displayio.Group()
for r in range(MARK_SIZE - MARK_THICKNESS, MARK_SIZE):
    marker.append(Circle(0, 0, r, outline=MARK_COLOR))
pyportal.splash.append(marker)

def get_location(width=WIDTH, height=HEIGHT):
    """Fetch current lat/lon, convert to (x, y) tuple scaled to width/height."""

    # Get location
    try:
        location = pyportal.fetch()
    except RuntimeError:
        return None, None

    # Compute (x, y) coordinates
    lat = float(location["latitude"])   # degrees, -90 to 90
    lon = float(location["longitude"])  # degrees, -180 to 180

    # Scale latitude for cropped map
    lat *= 90 / LAT_MAX

    # Mercator projection math
    # https://stackoverflow.com/a/14457180
    # https://en.wikipedia.org/wiki/Mercator_projection#Alternative_expressions
    x = lon + 180
    x = width * x / 360

    y = math.radians(lat)
    y = math.tan(math.pi / 4 + y / 2)
    y = math.log(y)
    y = (width * y) / (2 * math.pi)
    y = height / 2 - y

    return int(x), int(y)

def update_display(current_time, update_iss=False):
    """Update the display with current info."""

    # ISS location
    if update_iss:
        x, y = get_location()
        if x and y:
            marker.x = x
            marker.y = y
            if len(trail) >= TRAIL_LENGTH:
                trail.pop(0)
            trail.append(displayio.TileGrid(trail_bitmap,
                                            pixel_shader=trail_palette,
                                            x = x - 1,
                                            y = y - 1) )


    # Date and time
    date_label.text = "{:04}-{:02}-{:02}".format(current_time.tm_year,
                                                 current_time.tm_mon,
                                                 current_time.tm_mday)
    time_label.text = "{:02}:{:02}:{:02}".format(current_time.tm_hour,
                                                 current_time.tm_min,
                                                 current_time.tm_sec)

    try:
        board.DISPLAY.refresh(target_frames_per_second=60)
    except AttributeError:
        board.DISPLAY.refresh_soon()


# Initial refresh
update_display(time.localtime(), True)
last_update = time.monotonic()

# Run forever
while True:
    now = time.monotonic()
    new_position = False
    if now - last_update > UPDATE_RATE:
        new_position = True
        last_update = now
    update_display(time.localtime(), new_position)
    time.sleep(0.5)
```
Here is the settings.toml file necessary to connect to the internet:
```python
CIRCUITPY_WIFI_SSID = "Verizon_9KJTQ7"
CIRCUITPY_WIFI_PASSWORD = "left out for obvious reasons"
ADAFRUIT_AIO_USERNAME = "left out for obvious reasons"
ADAFRUIT_AIO_KEY = "left out for obvious reasons"
```

# Bill of Materials
Here's where you'll list the parts in your project. To add more rows, just copy and paste the example rows below.
Don't forget to place the link of where to buy each component inside the quotation marks in the corresponding row after href =. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize this to your project needs. 

| **Part** | **Note** | **Price** | **Link** |
|:--:|:--:|:--:|:--:|
| Adafruit Pyportal | Microcontroller and screen | $54.95 | <a href="https://www.adafruit.com/product/4116"> Link </a> |
| Micro USB Cable | Connect computer to pyportal | $4.95 | <a href="https://www.adafruit.com/product/592"> Link </a> |

# Other Resources/Examples
Here is a <a href="https://docs.circuitpython.org/projects/pyportal/en/latest/api.html"> link </a> to the documentation for the standard Pyportal library to help get you started.

To watch the BSE tutorial on how to create a portfolio, click <a href="https://drive.google.com/file/d/1GIGxyskToY8Ep137GnfTcfMCH4LaB6MF/view"> here </a>.
