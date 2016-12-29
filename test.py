# -*- coding: utf-8 -*-

# Librairies standards
#======================
import unittest, sys, os

class TestMain(unittest.TestCase):

    def test_sys_path(self):
        self.assertIn("/root/marcus", sys.path)

    def test_working_directory(self):
        self.assertEqual("/root/marcus", os.getcwd())

    def test_imports(self):
        try:
            from main import Marcus
        except ImportError:
            self.fail()

class TestPins(unittest.TestCase):

    def test_import_adafruit(self):
        try:
            import Adafruit_BBIO
            del Adafruit_BBIO
        except ImportError:
            self.fail()

    def test_import_serial(self):
        try:
            import serial
        except ImportError:
            self.fail()

    def test_import_pins(self):
        try:
            import peripheriques.pins
            del peripheriques.pins
        except ImportError:
            self.fail()

    def test_set_low(self):
        import Adafruit_BBIO.GPIO as GPIO
        from peripheriques.pins import set_low, set_output, get_input
        pin = "P8_11"
        set_output(pin)
        set_low(pin)
        self.assertEqual(get_input(pin), GPIO.LOW)

    def test_set_high(self):
        import Adafruit_BBIO.GPIO as GPIO
        from peripheriques.pins import set_high, set_output, get_input
        pin = "P8_11"
        set_output(pin)
        set_high(pin)
        self.assertEqual(get_input(pin), GPIO.HIGH)

    def test_pwm(self):
        from peripheriques.pins import set_pwm, set_duty_cycle, reset_pwm
        pin = "P9_16"
        set_pwm(pin)
        set_duty_cycle(pin, 50)
        reset_pwm(pin)
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)

