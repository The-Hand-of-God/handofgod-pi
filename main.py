import requests

from flask import Flask
from gpiozero import LED
app = Flask(__name__)

red = LED(14)
yellow = LED(15)
green = LED(18)
blue = LED(23)

lights = [red, yellow, green, blue]

addresses = ['192.168.5.56', '192.168.5.164:5000', '192.168.5.251']

access_token="BQAP39lmYAS2ybg3uvfESNjhebqDk1xTYQTMHkN3T0g8yd68tn4k9r_HIdMvQlZ47bGt2EWwwjxTxw8u67V3tugE0KByLad3XKXX_MptFeP5xcokmQ_4TLmxqPOwCq9uqxgUChZ_fZteFMNK-rQGhaO9oH7BR4V2XY4"

@app.route('/')
def hello_world():
    return 'Hello, world!'

# Device Controlling Routes

@app.route('/device/<int:device_num>/on')
def device_on(device_num):
    requests.get(url='http://{}/on'.format(addresses[device_num]))

    return 'On'

@app.route('/device/<int:device_num>/off')
def device_off(device_num):
    requests.get(url='http://{}/off'.format(addresses[device_num]))

    return 'Device off'

@app.route('/device/<int:device_num>/toggle')
def device_toggle(device_num):
    requests.get(url='http://{}/toggle'.format(addresses[device_num]))

    return 'device toggled'


# LED controlling routes

@app.route('/on')
def on():
    for light in lights:
        light.on()

    return 'on'

@app.route('/off')
def off():
    for light in lights:
        light.off()

    return 'off'

@app.route('/toggle')
def toggle():
    for light in lights:
        light.toggle()

    return 'toggled'


@app.route('/play')
def play_spotify():
     return requests.put("https://api.spotify.com/v1/me/player/play", 
        headers={'Authorization': 'Bearer {}'.format(access_token)}).content

@app.route('/pause')
def pause_spotify():
    return requests.put("https://api.spotify.com/v1/me/player/pause",
        headers={'Authorization': 'Bearer {}'.format(access_token)}).content

@app.route('/toggle-play')
def toggle_spotify():
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
        headers={'Authorization': 'Bearer {}'.format(access_token)})

    if response.status_code == 200 and response.json()['is_playing']:
        return pause_spotify()

    elif response.status_code == 200 or response.status_code == 204:
        return play_spotify()

    return 'Uh oh'

@app.route('/next')
def next_song():
    return requests.post("https://api.spotify.com/v1/me/player/next",
        headers={'Authorization': 'Bearer {}'.format(access_token)}).content

@app.route('/prev')
def previous_song():
    return requests.post("https://api.spotify.com/v1/me/player/previous",
        headers={'Authorization': 'Bearer {}'.format(access_token)}).content

