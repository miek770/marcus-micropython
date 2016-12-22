# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2013 Michel Lavoie <lavoie.michel@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

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

