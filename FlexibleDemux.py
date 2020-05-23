'''

-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
-|F|l|e|x|i|b|l|e|-|D|e|m|u|l|t|i|p|l|e|x|e|r|
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Author: Jeff
Environment:
    Python 3.8.0 64-bit
    Ubuntu Linux
    Visual Studio Code
    Altera Quartus Prime 19.1 Lite Edition 
'''

from myhdl import *

def flexibleDemux(q, d, clk):

    @always(clk.posedge)
    def logic():
        q.next = d

    return logic

def convert():
    q, d, clk = [Signal(bool(0)) for i in range(3)]
    toVHDL(flexibleDemux, q, d, clk)

convert()