#!/usr/bin/env python

import sys
import json

if __name__ == '__main__':
    if len(sys.argv)!= 2:
        print 'usage: %s' % sys.argv[0]
        sys.exit(1)
    else:
        j_str = sys.argv[1]
        j=json.loads(j_str)
        s=json.dumps(j,indent=4,ensure_ascii=False,encoding='utf-8')
        print "=========== JSON BEGIN ============"
        print s
        print "=========== JSON  END  ============"

    
