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

@block
def flexibleDemux(pin_in, pins_select, pins_out):

    @always_comb
    def logic():
        intPinSel = pins_select
        pinOutBufferVal = 0
        one =  intbv(1)[MUX_NUM_BIT_OUT:]
        
        for x in range(0,MUX_NUM_BIT_OUT):
            if pin_in==1 and intPinSel==x:
                pinOutBufferVal = pinOutBufferVal | (one<<x)

        pins_out.next =  pinOutBufferVal
    return logic


@block
def dflipflop(pin_in, pin_out, clk):
    
    @always(clk.posedge)
    def seq_logic():
        pin_out.next = pin_in
    return seq_logic


@block
def top(mux_pin_in, mux_pins_select, mux_pins_out, dff_pin_out, dff_clk):
    instflexmux = flexibleDemux(mux_pin_in, mux_pins_select, mux_pins_out)
    instdff = dflipflop(mux_pin_in, dff_pin_out, dff_clk)
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
    clk = Signal(intbv(0)[1:])
    pins_select = Signal(intbv(0)[MUX_SEL_NUM_BIT:])
    pins_out = Signal(intbv(0)[MUX_NUM_BIT_OUT:])
    pin_in = Signal(intbv(0)[1:])
    dff_clk_in = Signal(intbv(0)[1:])
    dff_pin_out = Signal(intbv(0)[1:])
    #flexDemuxInst = flexibleDemux(pin_in, pins_select, pins_out)
    inst = top(pin_in, pins_select, pins_out, dff_pin_out, dff_clk_in)

    @always(delay(10))
    def clkgen():
        clk.next = not clk
        pin_in.next = not pin_in

    @always(delay(5))
    def clkgendff():
        dff_clk_in.next = not dff_clk_in

    @always(clk.negedge)
    def stimulus():
        pins_select.next = randrange(8)

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
