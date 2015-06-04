#!/usr/bin/env python

__author__ = 'linjunqi'

import sys
import base64
import binascii


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: %s <base64 str>" % sys.argv[0]
        sys.exit(1)
    else:
        base64Str = sys.argv[1]
        bin_data = base64.b64decode(base64Str)
        print "\n========= Result Begin ========="
        print binascii.hexlify(bin_data).upper()
        print "========= Result END =========\n"