import time
import busio
import board
import adafruit_rfm9x
import RPi.GPIO as GPIO
import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime
from digitalio import DigitalInOut, Direction, Pull


# Configure LoRa Radio
CS = DigitalInOut(board.D5) # pin 29 on Rpi Zero
RESET = DigitalInOut(board.D6) # pin 31 on Rpi Zero
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
print("Code Running")

#setup filesave
file=open("grounddata.txt", "a")
file.write("Data Received from Rocket for Intern Space Program\n")
file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
file.write("\n\n")

#pins for lcds
lcd1_rs = DigitalInOut(board.D22)
lcd1_en = DigitalInOut(board.D17)
lcd1_d4 = DigitalInOut(board.D25)
lcd1_d5 = DigitalInOut(board.D24)
lcd1_d6 = DigitalInOut(board.D23)
lcd1_d7 = DigitalInOut(board.D18)

lcd2_rs = DigitalInOut(board.D4)
lcd2_en = DigitalInOut(board.D14)
lcd2_d4 = DigitalInOut(board.D15)
lcd2_d5 = DigitalInOut(board.D27)
lcd2_d6 = DigitalInOut(board.D8)
lcd2_d7 = DigitalInOut(board.D7)

lcd_columns = 16
lcd_rows = 2

lcd1 = characterlcd.Character_LCD_Mono(lcd1_rs, lcd1_en, lcd1_d4, lcd1_d5, lcd1_d6, lcd1_d7, lcd_columns, lcd_rows)
lcd2= characterlcd.Character_LCD_Mono(lcd2_rs, lcd2_en, lcd2_d4, lcd2_d5, lcd2_d6, lcd2_d7, lcd_columns, lcd_rows)




#pins for switches+relay
sw2= DigitalInOut(board.D19) #set 8s
sw3=DigitalInOut(board.D16) #set altitude and timer
sw4= DigitalInOut(board.D26) #start countdown
sw5 = DigitalInOut(board.D20) #relay unlocked
relay = DigitalInOut(board.D21) 

while (sw2 != GPIO.LOW):

   print("waiting on switch 2\n")
   time.sleep(.1)
   
#SET 8's on both LCDS
lcd1.clear()
lcd2.clear()
text = "888"
lcd1.message(text)
lcd2.message(text)


while sw3 != GPIO.HIGH:

   print("waiting on switch 3\n")
   time.sleep(.1)  
 
#SET LCDS TO ALTITUDE AND TIMER
lcd1.clear()
lcd2.clear()
lcd1.message="timer"
lcd2.message="altitude"
  
   
while sw4 != GPIO.HIGH:

   print("waiting on switch 4\n")
   time.sleep(.1)  

#start countdown
t=10
while(t>0):
   text1 = t
   lcd1.message = t
   time.sleep(1)
   t=t-1
   

while sw5 != GPIO.HIGH:

   print("waiting on switch 5\n")
   time.sleep(.1)  

GPIO.output(relay, GPIO.HIGH)

#unlock relay

file.write("ALL SYSTEMS GO: ")
file.write(str(datetime.now().time()))
file.write("\n")
file.close()



#Continuous Program
while True:
   print("ready for packet")
   packet=rfm9x.receive()
   if packet is not None:
      packet_text=str(packet, 'ascii')
      file=open("grounddata.txt", "a")
      file.write(str(datetime.now().time()))
      file.write("\n")
      file.write(packet_text)
      file.write("\n\n")
      file.close()
      print("received packet!!!")
      print("Received: {0}".format(packet_text))
#   print("Code Running")
   time.sleep(.001)