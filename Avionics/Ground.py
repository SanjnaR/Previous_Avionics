import time
import busio
import board
import adafruit_rfm9x
import RPi.GPIO as GPIO
import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime
from digitalio import DigitalInOut, Direction, Pull

ALT=0
GYRO=0,0,0

def parse():
    data=packet_text.split(" ")
    for i in data:
        print (i)
    ALT=0
    GYRO=0

def LORA():
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
      lcd1.clear()
      lcd2.clear()
      data=packet_text.split(" ")
      #for i in data:
       # print (i)
      ALT=data[7]
      #print(ALT[0:5])
      
      lcd2.message="Altitude:\n"+ALT[0:5]+" feet"
      GYRO1=data[1]
      GYRO2=data[2]
      GYRO3=data[3]
      GYRO=GYRO1[1:5]+"\n"+GYRO2[0:5]+ "       "+GYRO3[0:5]
      lcd1.message=GYRO

# Configure LoRa Radio
CS = DigitalInOut(board.D5)
RESET = DigitalInOut(board.D6)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23

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

lcd2_rs = DigitalInOut(board.D15) #pin 10
lcd2_en = DigitalInOut(board.D4)  #pin 7
lcd2_d4 = DigitalInOut(board.D7)  #pin 
lcd2_d5 = DigitalInOut(board.D8)  #pin 
lcd2_d6 = DigitalInOut(board.D27)  #pin 
lcd2_d7 = DigitalInOut(board.D14)  #pin 

lcd_columns = 16
lcd_rows = 2

lcd1 = characterlcd.Character_LCD_Mono(lcd1_rs, lcd1_en, lcd1_d4, lcd1_d5, lcd1_d6, lcd1_d7, lcd_columns, lcd_rows)
lcd2= characterlcd.Character_LCD_Mono(lcd2_rs, lcd2_en, lcd2_d4, lcd2_d5, lcd2_d6, lcd2_d7, lcd_columns, lcd_rows)


#pins and relays
sw2=20
sw3=26
sw4=16
sw5=19
relay=12

GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, GPIO.LOW)

while GPIO.input(sw2)!=1:

   print("waiting on switch 2\n")
   time.sleep(1)
 
print("sw2 activated")
#SET 8's on both LCDS
lcd1.clear()
lcd2.clear()
text = "888"
lcd1.message=text
lcd2.message=text
time.sleep(1)


while GPIO.input(sw3)!=1:
   print("waiting on switch 3\n")
   time.sleep(1)  

print("sw3 activated")
#SET LCDS TO ALTITUDE AND TIMER
lcd1.clear()
lcd2.clear()
lcd1.message="Timer:"
lcd2.message="Altitude:\n0"
time.sleep(1)  


while GPIO.input(sw4)!=1:

   print("waiting on switch 4\n")
   time.sleep(1)  

print("sw4 activated")
#start countdown
t=10
while(t>=0):
   text1 = t
   lcd1.clear()
   lcd1.message = "Countdown:\n"+str(t)
   time.sleep(1)
   t=t-1
   
if(GPIO.input(sw5)==1):
   GPIO.output(relay, GPIO.HIGH)
   print("button active")
else: 
    print("waiting on five")

print("launch")
file.write("ALL SYSTEMS GO: ")
file.write(str(datetime.now().time()))
file.write("\n")
file.close()


#Continuous Program
while True:
   LORA()

   time.sleep(.5)
   #lcd2.clear
   #lcd1.clear
   #lcd2.message=ALT
   #lcd1.message=GYRO1
   
