# -*- coding: utf-8 -*-

# Librairies standards
#======================
import logging

# Librairies spéciales
#======================
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

# Dictionnaire de pins digitales
#================================

# pins[index] = in/out

pins = dict()
pins['P8_7'] = None # Bumper - Avant droit
pins['P8_8'] = None # Bumper - Avant gauche
pins['P8_9'] = None # Bumper - Arrière droit
pins['P8_10'] = None # Bumper - Arrière gauche
pins['P8_11'] = None # Reservee pour unittest
pins['P8_12'] = None
pins['P8_13'] = None # Peut être utilisée en PWM
pins['P8_14'] = None
pins['P8_15'] = None
pins['P8_16'] = None
pins['P8_17'] = None
pins['P8_18'] = None
pins['P8_19'] = None # Peut être utilisée en PWM
pins['P8_26'] = None # Non-testée
pins['P8_27'] = None # Non-testée
pins['P8_28'] = None # Non-testée
pins['P8_29'] = None # Non-testée
pins['P8_30'] = None # Non-testée
pins['P8_31'] = None # Non-testée
pins['P8_32'] = None # Non-testée
pins['P8_33'] = None # Non-testée
pins['P8_34'] = None # Non-testée
pins['P8_35'] = None # Non-testée
pins['P8_36'] = None # Non-testée
pins['P8_37'] = None # Non-testée
pins['P8_38'] = None # Non-testée
pins['P8_39'] = None # Non-testée
pins['P8_40'] = None # Non-testée
pins['P8_41'] = None # Non-testée
pins['P8_42'] = None # Non-testée
pins['P8_43'] = None # Non-testée
pins['P8_44'] = None # Non-testée
pins['P8_45'] = None # Non-testée
pins['P8_46'] = None # Non-testée
pins['P9_11'] = None
pins['P9_12'] = None # Direction moteur droit
pins['P9_13'] = None # Direction moteur droit
pins['P9_14'] = None # Enable moteur droit (PWM)
pins['P9_15'] = None # Direction moteur gauche
pins['P9_16'] = None # Enable moteur gauche (PWM)
pins['P9_21'] = None # Direction moteur gauche
pins['P9_22'] = None
pins['P9_23'] = None
#pins['P9_24'] = None # Réservée pour UART1
pins['P9_25'] = None
#pins['P9_26'] = None # Réservée pour UART1
pins['P9_27'] = None
pins['P9_28'] = None
pins['P9_29'] = None
pins['P9_30'] = None
pins['P9_31'] = None
pins['P9_42'] = None

# Pins analogiques
#==================
# P9_39 - AIN0 # GP2D12 avant milieu
# P9_40 - AIN1 # GP2D12 avant gauche
# P9_37 - AIN2 # GP2D12 avant droite
# P9_38 - AIN3
# P9_33 - AIN4
# P9_36 - AIN5
# P9_35 - AIN6
#ADC.setup()

# Configurations
#================

def set_uart(uart_id):
    """Active le port de communication série.
    """

    if uart_id not in (1, 2, 3, 4, 5):
        logging.error("Port série invalide : UART{}".format(uart_id))
        return

    elif uart_id == 1:
        pins_uart = ("P9_26", "P9_24", "P9_20", "P9_19")
    elif uart_id == 2:
        pins_uart = ("P9_22", "P9_21")
    elif uart_id == 3:
        pins_uart = ("P9_42", "P8_36", "P8_34")
    elif uart_id == 4:
        pins_uart = ("P9_11", "P9_13", "P8_35", "P8_33")
    elif uart_id == 5:
        pins_uart = ("P8_38", "P8_37", "P8_31", "P8_32")

    for pin in pins_uart:
        try:
            if pins[pin] is not None:
                logging.error("{} est déjà configurée en '{}'".format(pin, pins[pin]))
                return
            else:
                pins[pin] = "uart{}".format(uart_id)
        except KeyError:
            continue
    UART.setup("UART{}".format(uart_id))

def set_pwm(pin):
    """Configure la pin en sortie PWM.
    """

    # Vérifie si la pin est déjà configurée
    if pins[pin] is not None and pins[pin] != "pwm":
        logging.error("{} est déjà configurée en '{}'".format(pin, pins[pin]))

    else:
        pins[pin] = "pwm"
        # Démarre le PWM avec un "duty cycle" de 0%
        PWM.start(pin, 0)

def reset_pwm(pin):
    """Désactive la pin de sortie PWM.
    """

    # Vérifie si la pin est bien configurée en PWM
    if pins[pin] != "pwm":
        logging.error("{} n'est pas configurée en PWM : '{}'".format(pin, pins[pin]))

    else:
        pins[pin] = None
        PWM.stop(pin)
        PWM.cleanup()

def set_output(pin):
    """Configure la pin en sortie numérique.
    """

    # Vérifie si la pin est déjà configurée
    if pins[pin] is not None and pins[pin] != "out":
        logging.error("{} est déjà configurée en '{}'".format(pin, pins[pin]))

    else:
        GPIO.setup(pin, GPIO.OUT)
        pins[pin] = 'out'

        # Met la pin à 3.3V (high) par défaut
        set_high(pin)

def set_input(pin):
    """Configure la pin en entrée numérique.
    """

    # Vérifie si la pin est déjà configurée
    if pins[pin] is not None and pins[pin] != "in":
        logging.error("{} est déjà configurée en '{}'".format(pin, pins[pin]))

    else:
        GPIO.setup(pin, GPIO.IN)
        pins[pin] = 'in'

# Lectures
#==========

def get_input(pin):
    """Retourne la valeur de la pin.
    """

    return GPIO.input(pin)

def get_adc(pin):
    """Retourne une valeur entre 0,0 et 1,0 correspondant à une
    lecture entre 0,0V et 3,3V.

    Selon https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/adc,
    en date du 2016-12-22 :

    There is currently a bug in the ADC driver. You'll need to read
    the values twice in order to get the latest value.
    """

    ADC.read(pin)
    reading = ADC.read(pin)
    return reading

# Écritures
#===========

def set_duty_cycle(pin, duty_cycle):
    """Règle le "duty cycle" de la pin en mode PWM.
    """

    # Vérifie si la pin est configurée en PWM
    if pins[pin] == "pwm":
        PWM.set_duty_cycle(pin, duty_cycle)

    else:
        logging.error("{} est configurée en '{}'".format(pin, pins[pin]))

def set_low(pin):
    """Règle la sortie numérique à 0V.
    """

    # Vérifie si la pin est configurée en sortie
    if pins[pin] == 'out':
        GPIO.output(pin, GPIO.LOW)

    else:
        logging.error("{} est configurée en '{}'".format(pin, pins[pin]))


def set_high(pin):
    """Règle la sortie numérique à 3,3V.
    """

    # Vérifie si la pin est configurée en sortie
    if pins[pin] == 'out':
        GPIO.output(pin, GPIO.HIGH)

    else:
        logging.error("{} est configurée en '{}'".format(pin, pins[pin]))
