#!/usr/bin/env python

__author__ = 'linjunqi'

import sys
import base64
import binascii


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: %s <hex str>" % sys.argv[0]
        sys.exit(1)
    else:
        hex_str = sys.argv[1]
        base64_str = base64.b64encode(binascii.unhexlify(hex_str))
        print "\n========= Result Begin ========="
        print base64_str
        print "========= Result END =========\n"