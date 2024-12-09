import unittest

import os
import sys
import time
import threading
import json

sys.path.append('..')

import ilff

def mktext(i):
    return 'abc' * (i%7)

class TestILFFMultiThread(unittest.TestCase):

    ilf = None

    def threadRFun(arg):
        print(arg)
        results = []
        t0 = time.time()
        print('rfun', arg)
        sys.stdout.flush()
        ilf = ilff.ILFFFile('test.ilff', 'r', encoding='utf8')
        for i in range(20):
            n = ilf.get_nlines()
            lns = ilf.getlines(n-3, 3)
            print('r % 8.4f: % 4d' % (time.time() - t0, n))
            print(lns)
            for ln in lns:
                d = json.loads(ln)
                results.append(d['text'] != mktext(d['num']))
            time.sleep(1)
            sys.stdout.flush()
        ilf.close()
        res = min(results)
        print('read exit')
        return res

    id = 0

    def threadWFun(arg):
        print(arg)
        ilf = ilff.ILFFFile('test.ilff', 'w', encoding='utf8')
        for i in range(2000):
            n = ilf.get_nlines()
            ilf.appendLine('{ "num": %d, "text": "%s"}' % (i,mktext(i)))
            time.sleep(0.01)
        ilf.close()
        print('write exit')
        return 0

    def test_01_launchJobs(self):
        nwrt = 100
        tr = threading.Thread(target=self.threadRFun)
        for i in range(10):
            tw = threading.Thread(target=self.threadWFun)
            tw.start()
        time.sleep(1)
        tr.start()
        time.sleep(21)
        print('wait end')
        ilf = ilff.ILFFFile('test.ilff', 'w', encoding='utf8')
        ilf.close()
        ilf.remove()

if __name__ == '__main__':
    unittest.main()
