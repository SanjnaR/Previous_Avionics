import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_mma8451
import adafruit_rfm9x
import adafruit_bmp280
from datetime import datetime


# Configure LoRa Radio
CS = DigitalInOut(board.D5)
RESET = DigitalInOut(board.D6)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23


#Configure BMP (0x77)and MMA (0x1d)
i2c = busio.I2C(board.SCL, board.SDA)

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = 1013.25

mma= adafruit_mma8451.MMA8451(i2c)
mma.range = adafruit_mma8451.RANGE_8G
mma.data_rate = adafruit_mma8451.DATARATE_400HZ
packet_num=0

#configure file to werite to
file=open("rocketdata.txt", "a")
file.write("Intern Space Program\n")
file.write(datetime.now().strftime('%Y -%m-%d %H:%M:%S'))
file.write("\n\n")
file.close()

#Continuous Program
while True:
   #print("Running Continous Program")
   file=open("rocketdata.txt", "a")
   x, y, z = mma.acceleration
   packet_num=packet_num+1
   timej=datetime.now().time()
   file.write(str(timej))
   print('\nPacket Num: '+ str(packet_num))
   file.write('\nPacket Num: '+ str(packet_num)+"\n")
   print('Acceleration: x={0:0.3f} m/s^2 y={1:0.3f} m/s^2 z={2:0.3f} m/s^2'.format(x, y, z))
   file.write('Acceleration: x={0:0.3f} m/s^2 y={1:0.3f} m/s^2 z={2:0.3f} m/s^2'.format(x, y, z)+"\n")
   orientation = mma.orientation
   print('Orientation: {0}'.format(orientation))
   file.write('Orientation: {0}'.format(orientation)+"\n")
   print("Temperature: %0.1f C" % bmp280.temperature)
   file.write("Temperature: %0.1f C" % bmp280.temperature+"\n")
   print("Pressure: %0.1f hPa" % bmp280.pressure)
   file.write("Pressure: %0.1f hPa" % bmp280.pressure+"\n")
   print("Altitude = %0.2f meters" % bmp280.altitude)
   file.write("Altitude = %0.2f meters" % bmp280.altitude+"\n\n")
   rfm9x.send(bytes(str(packet_num)+" "+str(mma.acceleration)+" "+str(mma.orientation)+" "+str(bmp280.temperature)+" "+str(bmp280.pressure)+" "+str(bmp280.altitude), "utf-8"))
   #rfm9x.send(bytes('Hello world!\r\n',"utf-8"))

   print("sent Lora packet")
   time.sleep(.5)
   file.close()