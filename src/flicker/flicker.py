#!/usr/bin/env python3.7

import time
import board
import neopixel
import random
import threading

from flask import Flask, request, jsonify

def gamma_correction(max_in, max_out, gamma):
    gamma_table = []
    for i in range(0, max_in):
        g = round(((i / max_in) ** gamma) * max_out + 0.5)
        gamma_table.append(g)
    return gamma_table

# Init pixel control
pixel_pin = board.D12
num_pixels = 2
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=True, pixel_order=ORDER)

# Base orange colour values
orange_g_min = 40
orange_g_max = 70

orange_r_min = 50
orange_r_max = 255

# Default dim values
dim_left = 100 
dim_right = 100

# Init with orange colour
g_base = orange_g_max
r_base = orange_r_max
b_base = 0

# Gamma correction parameters
gamma = 2.8
g_gamma = gamma_correction(g_base, g_base, gamma)
r_gamma = gamma_correction(r_base, r_base, gamma)

def flicker_gamma():
    global g_base
    global r_base
    global b_base
    global dim_left
    global dim_right

    while True:
        diff = random.randint(90, 100) / 100
        g_out_left_index = round(g_base * diff * (dim_left /100))
        g_out_left = g_gamma[g_out_left_index - 1]
        
        r_out_left_index = round(r_base * diff * (dim_left /100))
        r_out_left = r_gamma[r_out_left_index - 1]

        b_out_left = round(b_base * diff * (dim_left /100))
        pixels[0] = (g_out_left, r_out_left, b_out_left)


        g_out_right_index = round(g_base * diff * (dim_right / 100))
        g_out_right = g_gamma[g_out_right_index - 1]
        
        r_out_right_index = round(r_base * diff * (dim_right / 100))
        r_out_right = r_gamma[r_out_right_index - 1]
        
        b_out_right = round(b_base * diff * (dim_right /100))
        pixels[1] = (g_out_right, r_out_right, b_out_right)

        time.sleep(random.randint(40,70)/1000)


def flicker_original():
    global g_base
    global r_base
    global b_base
    global dim_left
    global dim_right

    while True:
        diff = random.randint(75, 100) / 100
        g_out_left = round(g_base * diff * (dim_left /100))
        r_out_left = round(r_base * diff * (dim_left /100))
        b_out_left = round(b_base * diff * (dim_left /100))
        pixels[0] = (g_out_left, r_out_left, b_out_left)

        g_out_right = round(g_base * diff * (dim_right /100))
        r_out_right = round(r_base * diff * (dim_right /100))
        b_out_right = round(b_base * diff * (dim_right /100))
        pixels[1] = (g_out_right, r_out_right, b_out_right)

        time.sleep(random.randint(40,60)/1000)


def flicker_relative_diff():
    global g_base
    global r_base
    global b_base
    global dim_left
    global dim_right

    while True:
        diff = random.randint(75, 100) / 100
        print(f"diff: {diff}")
        g_out_left = g_min + round((g_max - g_min) * diff * (dim_left /100))
        r_out_left = r_min + round((r_max - r_min) * diff * (dim_left /100))
        b_out_left = round(b_base * diff * (dim_left /100))
        pixels[0] = (g_out_left, r_out_left, b_out_left)

        g_out_right = g_min + round((g_max - g_min) * diff * (dim_right /100))
        r_out_right = r_min + round((r_max - r_min) * diff * (dim_right /100))
        b_out_right = round(b_base * diff * (dim_right /100))
        pixels[1] = (g_out_right, r_out_right, b_out_right)

        time.sleep(random.randint(40,60)/1000)


t = threading.Thread(target=flicker_original)
# t = threading.Thread(target=flicker_gamma)
# t = threading.Thread(target=flicker_relative_diff)
t.start()


### Fask API ###

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/flicker', methods=['GET'])
def set_flicker():
    global dim_left
    global dim_right
    ret_val = ""
    value_error = "Invalid value. Must be betwee 1 and 100."
    if 'dim_left' in request.args:
        in_dim_left = int(request.args.get('dim_left'))
        if in_dim_left in range(1, 101):
            dim_left = in_dim_left
            ret_val += f"left={dim_left}\n"
        else:
            return value_error, 410

    if 'dim_right' in request.args:
        in_dim_right = int(request.args.get('dim_right'))
        if in_dim_right in range(1, 101):
            dim_right = in_dim_right
            ret_val += f"right={dim_right}\n"
        else:
            return value_error, 410

    if 'dim_all' in request.args:
        in_dim_all = int(request.args.get('dim_all'))
        if in_dim_all in range(1, 101):
            dim_left = in_dim_all
            dim_right = in_dim_all
            ret_val = f"left={dim_left}\nright={dim_right}\n"
        else:
            return value_error, 410
    return ret_val, 200

if __name__ == "__main__":
    app.run(host="localhost", port=3101)
