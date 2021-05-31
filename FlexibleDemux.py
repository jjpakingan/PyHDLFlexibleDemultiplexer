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
RUN_TEST_BENCH = 1
RUN_CONVERSION = 0

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
def dflipflop(pins:DFlipFlopPins):
    
    @always(pins.Clk.posedge)
    def seq_logic():
        pins.Out.next = pins.In
    return seq_logic

# -+-+-+-+-+-+-+-+-+-+
# -|T|o|p|-|B|l|o|c|k|
# -+-+-+-+-+-+-+-+-+-+

@block
def top(flexdemuxpins : FlexDemuxPins, dff_pins:DFlipFlopPins):
    instflexmux = flexibleDemux(flexdemuxpins)
    instdff = dflipflop(dff_pins)
    return instances()

# def convert():
#     pins_select = Signal(intbv(0)[MUX_SEL_NUM_BIT:])
#     pins_out = Signal(intbv(0)[MUX_NUM_BIT_OUT:])
#     pin_in = Signal(intbv(0)[1:])
#     toVHDL(flexibleDemux, pin_in, pins_select, pins_out)

def convert():
    pins_select = Signal(intbv(0)[MUX_SEL_NUM_BIT:])
    pins_out = Signal(intbv(0)[MUX_NUM_BIT_OUT:])
    pin_in = Signal(intbv(0)[1:])
    dff_clk_in = Signal(intbv(0)[1:])
    dff_pin_out = Signal(intbv(0)[1:])
    toVHDL(top, pin_in, pins_select, pins_out, dff_pin_out, dff_clk_in)

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

    clk = Signal(intbv(0)[1:])
    #flexDemuxInst = flexibleDemux(pin_in, pins_select, pins_out)
    inst = top(flexdemuxpins, dffpins)

    @always(delay(10))
    def clkgen():
        clk.next = not clk
        a = not flexdemuxpins.In
        flexdemuxpins.In.next = a
        dffpins.In.next = a

    @always(delay(5))
    def clkgendff():
        dffpins.Clk.next = not dffpins.Clk

    @always(clk.negedge)
    def stimulus():
        flexdemuxpins.Select = randrange(8)

    return inst, clkgen, clkgendff, stimulus

def simulate(timesteps=5000):
    # tb = traceSignals(testbench)
    tb = testbench()
    tb.config_sim(trace=True)
    tb.run_sim(timesteps)
    # sim = Simulation(tb)
    # sim.run(timesteps)
    # inst = testbench()
    # inst.run_sim(timesteps)

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
