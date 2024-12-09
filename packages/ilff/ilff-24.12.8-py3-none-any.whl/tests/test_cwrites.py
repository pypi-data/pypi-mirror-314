import unittest

import os
import sys
import uuid

sys.path.append('..')

import ilff

class TestCILFFWrites1(unittest.TestCase):

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    @classmethod
    def tearDownClass(self):
        ilff.unlink('test.ilff')

    def test_01_create(self):
        ilf = ilff.CILFFFile('test.ilff', mode='w', encoding='utf8')
        self.assertTrue(os.path.exists('test.ilff'))
        ilf.close()

    def test_02_write(self):
        ilf = ilff.CILFFFile('test.ilff', mode='w', encoding='utf8')
        rc = [*map(lambda x: ilf.appendLine(x), self.lines)]
        self.assertTrue(os.path.exists('test.ilff'))
        self.assertTrue(ilf.nlines() == 3)
        ilf.close()

    def test_03_get1(self):
        ilf = ilff.CILFFFile('test.ilff', mode='r', encoding='utf8')
        l1 = ilf.getline(0)
        print('L1:', l1)
        self.assertTrue(l1 == 'aaa\n')
        self.assertTrue(ilf.nlines() == 3)
        ilf.close()

    def test_04_get2(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        self.assertTrue(ilf.nlines() == 3)
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.lines[i] + '\n')
            self.assertTrue(l == self.lines[i] + '\n')
        self.assertTrue(ilf.nlines() == 3)
        ilf.close()

    def test_05_get3(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        for i in range(3):
            l = ilf.getline(i)
            self.assertTrue(l == self.lines[i] + '\n')
            print('L:', i, l, self.lines[i])
        ilf.close()

    def test_06_getlns(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        lns = ilf.getlines(0, 3)
        self.assertTrue(lns == self.linesnl)
        ilf.close()

    def test_07_getlnstxt(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        lns = ilf.getlinestxt(0, 3)
        print(f'7: "{lns}"')
        self.assertTrue(lns == '\n'.join(self.lines) + '\n')
        ilf.close()

    def test_08_getlnstxt2(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        lns = ilf.getlinestxt(0, 2)
        print(f'8: "{lns}"')
        self.assertTrue(lns == '\n'.join(self.lines[0:2]) + '\n')
        ilf.close()

    def test_09_getlnstxt3(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        lns = ilf.getlinestxt(1, 2)
        print(f'8: "{lns}"')
        self.assertTrue(lns == '\n'.join(self.lines[1:3]) + '\n')
        ilf.close()


class TestCILFFWrites2(unittest.TestCase):

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    @classmethod
    def tearDownClass(self):
        ilff.unlink('test.ilff')

    def test_01_append(self):
        ilf = ilff.CILFFFile('test.ilff', mode='w', encoding='utf8')
        r = [*map(lambda x: ilf.appendLine(x), self.lines)]
        self.assertTrue(os.path.exists('test.ilff'))
        self.assertTrue(ilf.nlines() == 3)
        ilf.close()

    def test_02_get2(self):
        ilf = ilff.CILFFFile('test.ilff', mode='r', encoding='utf8')
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.lines[i] + '\n')
            self.assertTrue(l == self.lines[i] + '\n')
        ilf.close()

    def test_03_append(self):
        ilf = ilff.CILFFFile('test.ilff', mode='a', encoding='utf8')
        r = [*map(lambda x: ilf.appendLine(x), self.lines)]
        self.assertTrue(os.path.exists('test.ilff'))
        self.assertTrue(ilf.nlines() == 6)
        ilf.close()

    def test_04_get(self):
        ilf = ilff.CILFFFile('test.ilff', mode='r', encoding='utf8')
        for i in range(6):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i % 3], l == self.lines[i % 3] + '\n')
            self.assertTrue(l == self.lines[i % 3] + '\n')
        ilf.close()

    def test_05_getlns(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        lns1 = ilf.getlinestxt(0, 3)
        lns = ilf.getlines(0, 3)
        self.assertTrue(ilf.nlines() == 6)
        self.assertTrue(lns == self.linesnl)
        lns = ilf.getlines(3, 3)
        self.assertTrue(lns == self.linesnl)
        ilf.close()

    def test_06_getlnstxt(self):
        ilf = ilff.CILFFFile('test.ilff', encoding='utf8')
        lns = ilf.getlinestxt(0, 6)
        print(f'6: "{lns}"')
        self.assertTrue(lns == ''.join(self.linesnl *2))
        ilf.close()


class TestCILFFWrites3(unittest.TestCase):

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        of = open(self.fname, 'w', newline='\n')
        of.write('\n'.join(self.lines) + '\n')
        of.close()

    def test_01a_buildindex(self):
        ilf = ilff.CILFFFile(self.fname, 'a+', check=False)
        ilf.buildindex()
        ilf.close()

    def test_02_get(self):
        ilf = ilff.CILFFFile(self.fname)
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.linesnl[i])
            self.assertTrue(l == self.linesnl[i])
        ilf.close()

    def test_03_get2(self):
        ilf = ilff.CILFFFile(self.fname, encoding='utf8')
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l)
            self.assertTrue(l == self.linesnl[i])
        ilf.close()

    def test_04_getlns(self):
        ilf = ilff.CILFFFile(self.fname, encoding='utf8')
        lns = ilf.getlines(0, 3)
        print(lns)
        self.assertTrue(lns == self.linesnl)
        ilf.close()

    def test_05_getrange(self):
        ilf = ilff.CILFFFile(self.fname, encoding='utf8')
        lns = ilf.getlinestxt(0, 3)
        print(lns)
        self.assertTrue(lns == ''.join(self.linesnl))
        ilf.close()


class TestCILFFWrites4(unittest.TestCase):

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        of = open(self.fname, 'w', newline='\n')
        of.write('\n'.join(self.lines))
        of.close()

    def test_01a_buildindex(self):
        ilf = ilff.CILFFFile(self.fname, 'a+', check=False)
        ilf.buildindex()
        ilf.close()

    def test_02_get(self):
        ilf = ilff.CILFFFile(self.fname)
        for i in range(3):
            l = ilf.getline(i)
            chck = l == self.linesnl[i] if i < 2 else l == self.lines[i]
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], chck)
            self.assertTrue(chck)
        ilf.close()

    def test_03_get2(self):
        ilf = ilff.CILFFFile(self.fname, encoding='utf8')
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l)
            self.assertTrue(i > 1 or l == self.linesnl[i])
            self.assertTrue(i < 2 or l == self.lines[i])
        ilf.close()

    def test_04_getlns(self):
        ilf = ilff.CILFFFile(self.fname, encoding='utf8')
        lns = ilf.getlines(0, 3)
        print(f'4: "{lns}"')
        self.assertTrue(lns == self.linesnl[0:2] + self.lines[2:3])
        ilf.close()

    def test_05_getrange(self):
        ilf = ilff.CILFFFile(self.fname, encoding='utf8')
        lns = ilf.getlinestxt(0, 3)
        print(f'5: "{lns}"')
        self.assertTrue(lns == '\n'.join(self.lines))
        ilf.close()


class TestCILFFWrites5(unittest.TestCase):

    lines = ['aaa4 5 d', 'bbbb b b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        ilf = ilff.CILFFFile(self.fname, 'w', check=False)
        [ilf.write(l) for l in self.linesnl]
        ilf.close()

    def test_02_get(self):
        ilf = ilff.CILFFFile(self.fname)
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.linesnl[i])
            self.assertTrue(l == self.linesnl[i])
        assert ilf.nlines() == 3
        ilf.close()

    def test_03_getln(self):
        self.lines += ['dddddddd dddddddd ddddd dddd', 'eeeee eeeeee eeeeeee eeeeee']
        ilf = ilff.CILFFFile(self.fname, mode='r+')
        l = ilf.getline(1)
        ilf.write(self.lines[3])
        assert l == self.linesnl[1]
        assert ilf.nlines() == 4
        assert ilf.getline(3) == self.lines[3] + '\n'
        ilf.close()


if __name__ == '__main__':
    unittest.main()
