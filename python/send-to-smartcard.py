#!/usr/bin/env python
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest

import sys
import binascii
import fileinput

"""
send apdu command via smartcard reader
"""
def send_smartcard_cmd(cmdstr_list):
    cardtype=AnyCardType()
    cardrequest=CardRequest(timeout=100000,cardType=cardtype)
    cardservice=cardrequest.waitforcard()

    conn=cardservice.connection
    try:
        conn.connect()

        count=1
        result=list()
        for cmdstr in cmdstr_list:
            cmd=list((ord(x) for x in binascii.unhexlify(cmdstr)))
            print ">>>%d %s" % (count,toHexString(cmd).replace(' ',''))
            data, sw1, sw2=conn.transmit(cmd)

            print "<<<%d data: %s sw: %02x%02x" % (count,toHexString(data).replace(' ',''),sw1,sw2)
            count+=1

    finally:
        conn.disconnect()

    return result.append((data, sw1, sw2))


"""
usage example 1: <PATH-OF-ME>/send-to-smartcard.py 00A4040000
usage example 2: <PATH-OF-ME>/send-to-smartcard.py 00A4040000 80CA9F7F00
"""
if __name__=='__main__':
    if(len(sys.argv)>1):
        if(sys.argv[1]=='-'):
            lines=list()
            for line in fileinput.input():
                lines.append(line.strip())
        else:
            lines=sys.argv[1:]

        send_smartcard_cmd(lines)
    else:
        print "no APDU found. usage: %s: <APDU> [,<APDU> [,<APDU>] ...]" % sys.argv[0]

