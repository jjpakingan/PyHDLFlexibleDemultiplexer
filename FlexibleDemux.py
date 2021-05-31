'''
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
-|F|l|e|x|i|b|l|e|-|D|e|m|u|l|t|i|p|l|e|x|e|r|
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Author: Jeff P
Environment:
    Python 3.9.4 64-bit
    Visual Studio Code
    Altera Quartus Prime 20.1.1 Lite Edition 
    myHDL 0.11
'''

# -+-+-+-+-+-+-+-+-+-+
# -|C|o|n|s|t|a|n|t|s|
# -+-+-+-+-+-+-+-+-+-+

UNIT_TEST_ENABLE = 0
RUN_TEST_BENCH = 0
RUN_CONVERSION = 1

# -+-+-+-+-+-+-+-+
# -|I|m|p|o|r|t|s|
# -+-+-+-+-+-+-+-+

from myhdl import *
import unittest
from random import randrange



# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# -|F|l|e|x|i|b|l|e|-|D|e|m|u|l|t|i|p|l|e|x|e|r|
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

MUX_NUM_BIT_OUT = 8
MUX_SEL_NUM_BIT = 3

class FlexDemuxPins:
    In = None
    Select = None
    Out = None 

@block
def flexibleDemux(flexdemuxpins : FlexDemuxPins):

    @always_comb
    def logic():
        pinOutBufferVal = 0
        one =  intbv(1)[MUX_NUM_BIT_OUT:]
        
        for x in range(0,MUX_NUM_BIT_OUT):
            if flexdemuxpins.In==1 and flexdemuxpins.Select==x:
                pinOutBufferVal = pinOutBufferVal | (one<<x)

        flexdemuxpins.Out.next =  pinOutBufferVal
    return logic

# -+-+-+-+-+
# -|D|-|F|F|
# -+-+-+-+-+

class DFlipFlopPins:
    In = None
    Out = None
    Clk = None

@block
def dflipflop(dff_pins:DFlipFlopPins):
    
    @always(dff_pins.Clk.posedge)
    def seq_logic():
        dff_pins.Out.next = dff_pins.In
    return seq_logic

# -+-+-+-+-+-+-+-+-+-+
# -|T|o|p|-|B|l|o|c|k|
# -+-+-+-+-+-+-+-+-+-+

@block
def top(flexdemuxpins : FlexDemuxPins, dff_pins:DFlipFlopPins):
    instflexmux = flexibleDemux(flexdemuxpins)
    instdff = dflipflop(dff_pins)
    return instances()


def convert():
    flexdemuxpins = FlexDemuxPins()
    flexdemuxpins.Select = Signal(intbv(0)[MUX_SEL_NUM_BIT:])
    flexdemuxpins.In = Signal(intbv(0)[1:])
    flexdemuxpins.Out = Signal(intbv(0)[MUX_NUM_BIT_OUT:])

    dffpins = DFlipFlopPins()
    dffpins.In = Signal(intbv(0)[1:])
    dffpins.Out = Signal(intbv(0)[1:])
    dffpins.Clk = Signal(intbv(0)[1:])

    inst = top(flexdemuxpins, dffpins)
    inst.convert('VHDL')


# -+-+-+-+-+-+-+-+-+-+-+
# -|T|e|s|t|-|B|e|n|c|h|
# -+-+-+-+-+-+-+-+-+-+-+

@block
def testbench():
    flexdemuxpins = FlexDemuxPins()
    flexdemuxpins.Select = Signal(intbv(0)[MUX_SEL_NUM_BIT:])
    flexdemuxpins.In = Signal(intbv(0)[1:])
    flexdemuxpins.Out = Signal(intbv(0)[MUX_NUM_BIT_OUT:])

    dffpins = DFlipFlopPins()
    dffpins.In = Signal(intbv(0)[1:])
    dffpins.Out = Signal(intbv(0)[1:])
    dffpins.Clk = Signal(intbv(0)[1:])

    test_clk = Signal(intbv(0)[1:])
    inst = top(flexdemuxpins, dffpins)

    @always(delay(10))
    def clkgen():
        test_clk.next = not test_clk
        a = not flexdemuxpins.In
        flexdemuxpins.In.next = a
        dffpins.In.next = a

    @always(delay(5))
    def clkgendff():
        dffpins.Clk.next = not dffpins.Clk

    @always(test_clk.negedge)
    def stimulus():
        flexdemuxpins.Select = randrange(8)

    return inst, clkgen, clkgendff, stimulus

def simulate(timesteps=5000):
    tb = testbench()
    tb.config_sim(trace=True)
    tb.run_sim(timesteps)

# -+-+-+-+-+-+-+-+-+-+
# -|U|n|i|t|-|T|e|s|t|
# -+-+-+-+-+-+-+-+-+-+

class TestMyHDLMethods(unittest.TestCase):
    def test_intbvlength(self):
        b = intbv(0)[3:]
        self.assertEqual(len(b),3)

# -+-+-+-+-+
# -|M|a|i|n|
# -+-+-+-+-+

if UNIT_TEST_ENABLE:
    unittest.main()
if RUN_CONVERSION:
    convert()
if RUN_TEST_BENCH:
    simulate()
