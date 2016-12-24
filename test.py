# -*- coding: utf-8 -*-

# Librairies standards
#======================
import unittest

class TestMain(unittest.TestCase):

    def test_sys_path(self):
        import sys
        self.assertIn("/root/marcus", sys.path)

    def test_working_directory(self):
        import os
        self.assertEqual("/root/marcus", os.getcwd())

    def test_imports(self):
        try:
            from main import Marcus

        except ImportError:
            self.fail()

class TestPins(unittest.TestCase):

    def test_imports(self):
        try:
            import peripheriques.pins

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

if __name__ == '__main__':
    unittest.main(verbosity=2)

