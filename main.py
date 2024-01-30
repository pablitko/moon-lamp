# Complete project details at https://RandomNerdTutorials.com

#r, g, b = ap[0]

# def web_page():
#   bme = bme280.BME280(i2c=i2c)
#   
#   html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
#   <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Trebuchet MS", Arial;}
#   table { border-collapse: collapse; width:35%; margin-left:auto; margin-right:auto; }
#   th { padding: 12px; background-color: #0043af; color: white; }
#   tr { border: 1px solid #ddd; padding: 12px; }
#   tr:hover { background-color: #bcbcbc; }
#   td { border: none; padding: 12px; }
#   .sensor { color:white; font-weight: bold; background-color: #bcbcbc; padding: 1px;
#   </style></head><body><h1>ESP with BME280</h1>
#   <table><tr><th>MEASUREMENT</th><th>VALUE</th></tr>
#   <tr><td>Temp. Celsius</td><td><span class="sensor">""" + str(bme.values[0]) + """</span></td></tr>
#   <tr><td>Pressure</td><td><span class="sensor">""" + str(bme.values[1]) + """</span></td></tr>
#   <tr><td>Humidity</td><td><span class="sensor">""" + str(bme.values[2]) + """</span></td></tr></body></html>"""
#   return html

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('', 80))
# s.listen(5)

from machine import Pin
from ir_rx.nec import NEC_16
from neopixel import NeoPixel

class APA106(NeoPixel):
    ORDER = (0, 1, 2, 3)
    
#import esp
#esp.osdebug(None)
#import gc
num_of_pixels = 18
pin = Pin(12, Pin.OUT) #PIN
ap = NeoPixel(pin, num_of_pixels, bpp=4) # how many pixels
ap[0] = (0, 255, 255,0)
ap[1] = (255, 0, 0,0)
ap.write()
#import webrepl
#webrepl.start()
#gc.collect()
print("Started")

global white_color
white_color = 0
buttons_data = {
    68: (255,255,255,white_color), #White
    24: (255,255,0,0), #yellow
    80: (204,102,0,0), #orange
    77: (102,0,204,0), #violet
    69: (0,0,255,0), #blue
    88: (255,0,0,0), #red
    89: (0,255,0,0), #green
    64: (0,0,0,0), #off
    92: (255,255,255,0), #on
    84: (255,78,78,0), # light red
    28: (255,128,0,0),
    25: (125,204,223,0),                                
    }

print("Start")
brightness = 100  # brighness in % (0-100)


def bri(pos):
    global brightness
    pos = round(pos/100*brightness)
    return pos

def set_color(data, qty,brightness):
    if color == 68 and brightness != 0:
        white = 255
    else:
        white = 0
    new_color = [buttons_data[data][0],buttons_data[data][1],buttons_data[data][2],white]    
    new_color = list(map(bri, new_color))
    
    new_color = tuple(new_color)
    leds_qty = qty
    for i in range(qty):
        ap[i] = new_color
    ap.write()
    print(new_color)

global moon_phase
moon_phase = 0
global color
color = 64
def set_phase():    
    if moon_phase == 0:
        set_color(64,num_of_pixels,0) #off
    else:
        set_color(color,moon_phase*3,brightness)

def callback(data, addr, ctrl):
    global moon_phase
    global color
    global brightness
    if data>0:
        if data != 16 and data not in (64,92,18,19):  # NEC protocol sends repeat codes.            
            color = data
            set_color(color,moon_phase*3,brightness)
            print(data)
        elif data == 64: # Off button pressed
            set_color(data,moon_phase*3,0)
        elif data == 92: #on button
            set_color(color,moon_phase*3,brightness)
        elif data == 19: # increase white > change brightness
            brightness = brightness + 10
            if brightness > 100:
                brightness = 100
            set_color(color,moon_phase*3,brightness)
            print("brightness: " + str(brightness))
        elif data == 18: # decrease white > change brightness
            brightness = brightness - 10
            if brightness < 0:
                brightness = 0
            set_color(color,moon_phase*3,brightness)
            print("brightness: " + str(brightness))
        elif data == 16: #change moon phase            
            moon_phase = moon_phase + 1            
            if moon_phase > 6:
                moon_phase = 0
            print("Moon phase: " + str(moon_phase))
            set_phase()
        #print('Data {:02x} Addr {:04x}'.format(data, addr)) 
        
ir = NEC_16(Pin(14, Pin.IN), callback)

# while True:
#     data = 0




# while True:
#   
#   try:
#     if gc.mem_free() < 102000:
#       gc.collect()
#     conn, addr = s.accept()
#     conn.settimeout(3.0)
#     print('Got a connection from %s' % str(addr))
#     request = conn.recv(1024)
#     conn.settimeout(None)
#     request = str(request)
#     print('Content = %s' % request)
#     response = web_page()
#     conn.send('HTTP/1.1 200 OK\n')
#     conn.send('Content-Type: text/html\n')
#     conn.send('Connection: close\n\n')
#     conn.sendall(response)
#     conn.close()
#   except OSError as e:
#     conn.close()
#     print('Connection closed')

