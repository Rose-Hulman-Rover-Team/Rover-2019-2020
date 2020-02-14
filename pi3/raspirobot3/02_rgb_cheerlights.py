# 03_rgb_cheerlights.py
# Set the color to the latest color that
# anyone in the world tweeted as #cheerlights

from squid import *
import urllib, time

squid = Squid(18, 23, 24)
cheerlights_url = "http://api.thingspeak.com/channels/1417/field/1/last.txt"

# setup a map data structure with the RGB values for the different colors 
color_map = {"red":(100,0,0),
             "green":(0,100,0),
             "blue":(0,0,100),
             "cyan":(0,50,100),
             "white":(50,50,50),
             "warmwhite":(100,100,100),
             "purple":(50,0,100),
             "magenta":(100,0,100),
             "yellow":(100,100,0),
             "orange":(100,50,0),
             "pink":(100,0,100),
             "oldlace":(100,100,100)}

try:
    while True:
        cheerlights = urllib.urlopen(cheerlights_url) # Open cheerlights file via URL
        chosen_color = cheerlights.read()             # Read the last cheerlights colour
        cheerlights.close()                           # Close cheerlights file
        print(chosen_color)                       
        color = color_map.get(chosen_color, (0, 0, 0)) # LED off if color name not found
        squid.set_color(color)
        time.sleep(2)
        
finally: 
    GPIO.cleanup()
