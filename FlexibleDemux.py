'''
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
-|F|l|e|x|i|b|l|e|-|D|e|m|u|l|t|i|p|l|e|x|e|r|
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Author: Jeff P
Environment:
    Python 3.8.0 64-bit
    Ubuntu Linux
    Visual Studio Code
    Altera Quartus Prime 19.1 Lite Edition 
'''
UNIT_TEST_ENABLE = 0

from myhdl import *
import unittest



# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# -|M|y|H|D|L|-|U|t|i|l|i|t|i|e|s|
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def getIntbV(numBit):
    return intbv(0)[numBit:]

def getSignalBool():
    return Signal(bool(0))


# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# -|F|l|e|x|i|b|l|e|-|D|e|m|u|l|t|i|p|l|e|x|e|r|
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# def flexibleDemux(q, d, clk):
def flexibleDemux(pin_in, pins_select, pins_out):

    @always_comb
    def logic():
        intPinSel = pins_select

        pinOutBufferVal = getIntbV(8) #TODO refactor the hardcoded value
        
        for x in range(0,8):
            if pin_in==1 and intPinSel==x:
                pinOutBufferVal[x] = 1
            else:
                pinOutBufferVal[x] = 0

        pins_out.next = pinOutBufferVal


    return logic

def convert():
    pins_select = Signal(getIntbV(3))
    pins_out = Signal(getIntbV(8))
    pin_in = getSignalBool()
    toVHDL(flexibleDemux, pin_in, pins_select, pins_out)


# -+-+-+-+-+-+-+-+-+-+
# -|U|n|i|t|-|T|e|s|t|
# -+-+-+-+-+-+-+-+-+-+

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_intbvlength(self):
        b = getIntbV(3)
        self.assertEqual(len(b),3)



if UNIT_TEST_ENABLE:
    unittest.main()
else:
    convert()
