#!/root/marcus/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep

# Librairies spéciales
#======================
from Adafruit_I2C import Adafruit_I2C

# Les pins suivantes peuvent être utiliées (i2c port 1) :

# P9_19: I2C2, SCL
# P9_20: I2C2, SDA

def connect():
    i2c = Adafruit_I2C(0x77)

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def main():
    pass

if __name__ == '__main__':
    main()
