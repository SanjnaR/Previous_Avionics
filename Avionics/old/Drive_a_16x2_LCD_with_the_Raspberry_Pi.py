from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd1_rs = digitalio.DigitalInOut(board.D22)
lcd1_en = digitalio.DigitalInOut(board.D17)
lcd1_d4 = digitalio.DigitalInOut(board.D25)
lcd1_d5 = digitalio.DigitalInOut(board.D24)
lcd1_d6 = digitalio.DigitalInOut(board.D23)
lcd1_d7 = digitalio.DigitalInOut(board.D18)

lcd2_rs = digitalio.DigitalInOut(board.D4)
lcd2_en = digitalio.DigitalInOut(board.D14)
lcd2_d4 = digitalio.DigitalInOut(board.D15)
lcd2_d5 = digitalio.DigitalInOut(board.D27)
lcd2_d6 = digitalio.DigitalInOut(board.D8)
lcd2_d7 = digitalio.DigitalInOut(board.D7)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd1_rs, lcd1_en, lcd1_d4, lcd1_d5, lcd1_d6, lcd1_d7, lcd1_columns, lcd1_rows)

# looking for an active Ethernet or WiFi device
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

# find an active IP on the first LIVE network device
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

# wipe LCD screen before we start
lcd.clear()

# before we start the main loop - detect active network device and ip address
sleep(2)
interface = find_interface()
ip_address = parse_ip()

while True:

    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')

    # current ip address
    lcd_line_2 = "IP " + ip_address

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(2)
