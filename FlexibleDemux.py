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
RUN_TEST_BENCH = 1
RUN_CONVERSION = 0

from myhdl import *
import unittest
from random import randrange


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

MUX_NUM_BIT_OUT = 8
MUX_SEL_NUM_BIT = 3

def flexibleDemux(pin_in, pins_select, pins_out):

    @always_comb
    def logic():
        intPinSel = pins_select

        pinOutBufferVal = getIntbV(MUX_NUM_BIT_OUT)
        
        for x in range(0,MUX_NUM_BIT_OUT):
            if pin_in==1 and intPinSel==x:
                pinOutBufferVal[x] = 1
            else:
                pinOutBufferVal[x] = 0

        pins_out.next = pinOutBufferVal


    return logic

def convert():
    pins_select = Signal(getIntbV(MUX_SEL_NUM_BIT))
    pins_out = Signal(getIntbV(MUX_NUM_BIT_OUT))
    pin_in = getSignalBool()
    toVHDL(flexibleDemux, pin_in, pins_select, pins_out)



# -+-+-+-+-+-+-+-+-+-+-+
# -|T|e|s|t|-|B|e|n|c|h|
# -+-+-+-+-+-+-+-+-+-+-+

# Test Bench example: Implementation

ACTIVE_LOW = 0

def testbench():

    clk = getSignalBool()
    pins_select = Signal(getIntbV(MUX_SEL_NUM_BIT))
    pins_out = Signal(getIntbV(MUX_NUM_BIT_OUT))
    pin_in = getSignalBool()

    flexDemuxInst = flexibleDemux(pin_in, pins_select, pins_out)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(clk.negedge)
    def stimulus():
        pin_in.next = randrange(2)

    return flexDemuxInst, clkgen, stimulus

def simulate(timesteps=5000):
    tb = traceSignals(testbench)
    sim = Simulation(tb)
    sim.run(timesteps)

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
if RUN_CONVERSION:
    convert()
if RUN_TEST_BENCH:
    simulate()
