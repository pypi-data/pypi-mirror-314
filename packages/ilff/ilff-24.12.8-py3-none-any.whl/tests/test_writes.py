import unittest

import os
import sys
import uuid
import json

sys.path.append('..')

import ilff

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestILFFWrites1(unittest.TestCase):

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    @classmethod
    def tearDownClass(self):
        ilff.unlink('test.ilff')

    def test_01_create(self):
        ilf = ilff.open('test.ilff', mode='w')
        self.assertTrue(os.path.exists('test.ilff'))
        ilf.close()

    def test_02_write(self):
        ilf = ilff.open('test.ilff', mode='w')
        rc = [*map(lambda x: ilf.write(x), self.linesnl)]
        self.assertTrue(os.path.exists('test.ilff'))
        self.assertTrue(ilf.nlines() == 3)
        ilf.dumpindex()
        ilf.close()

    def test_03_get1(self):
        ilf = ilff.open('test.ilff', mode='r')
        l1 = ilf.getline(0)
        print('L1:', l1)
        self.assertTrue(l1 == 'aaa\n')
        self.assertTrue(ilf.nlines() == 3)
        ilf.close()

    def test_04_get2(self):
        ilf = ilff.open('test.ilff')
        ilf.dumpindex()
        self.assertTrue(ilf.nlines() == 3)
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.lines[i] + '\n')
            self.assertTrue(l == self.lines[i] + '\n')
        self.assertTrue(ilf.nlines() == 3)
        ilf.close()

    def test_05_get3(self):
        ilf = ilff.open('test.ilff')
        for i in range(3):
            l = ilf.getline(i)
            self.assertTrue(l == self.lines[i] + '\n')
            print('L:', i, l, self.lines[i])
        ilf.close()

    def test_06_getlns(self):
        ilf = ilff.open('test.ilff')
        lns = ilf.getlines(0, 3)
        self.assertTrue(lns == self.linesnl)
        ilf.close()

    def test_07_getlnstxt(self):
        ilf = ilff.open('test.ilff')
        lns = ilf.getlinestxt(0, 3)
        print(f'7: "{lns}"')
        self.assertTrue(lns == '\n'.join(self.lines) + '\n')
        ilf.close()

    def test_08_getlnstxt2(self):
        ilf = ilff.open('test.ilff')
        lns = ilf.getlinestxt(0, 2)
        print(f'8: "{lns}"')
        self.assertTrue(lns == '\n'.join(self.lines[0:2]) + '\n')
        ilf.close()

    def test_09_getlnstxt3(self):
        ilf = ilff.open('test.ilff')
        lns = ilf.getlinestxt(1, 2)
        print(f'8: "{lns}"')
        self.assertTrue(lns == '\n'.join(self.lines[1:3]) + '\n')
        ilf.close()


class TestILFFWrites2(unittest.TestCase):

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    @classmethod
    def tearDownClass(self):
        ilff.unlink('test.ilff')

    def test_01_append(self):
        ilf = ilff.open('test.ilff', mode='w')
        r = [*map(lambda x: ilf.write(x), self.linesnl)]
        self.assertTrue(os.path.exists('test.ilff'))
        self.assertTrue(ilf.nlines() == 3)
        ilf.close()

    def test_02_get2(self):
        ilf = ilff.open('test.ilff', mode='r')
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.lines[i] + '\n')
            self.assertTrue(l == self.lines[i] + '\n')
        ilf.close()

    def test_03_append(self):
        ilf = ilff.open('test.ilff', mode='a')
        ilf.write(self.linesnl)
        self.assertTrue(os.path.exists('test.ilff'))
        self.assertTrue(ilf.nlines() == 6)
        ilf.close()

    def test_04_get(self):
        ilf = ilff.open('test.ilff', mode='r')
        for i in range(6):
            l = ilf.getline(i)
            print('Ldd:', i, '"%s"' % l, '"%s"' % self.lines[i % 3], l == self.lines[i % 3] + '\n')
            self.assertTrue(l == self.lines[i % 3] + '\n')
        ilf.close()

    def test_05_getlns(self):
        ilf = ilff.open('test.ilff')
        lns1 = ilf.getlinestxt(0, 3)
        lns = ilf.getlines(0, 3)
        self.assertTrue(ilf.nlines() == 6)
        self.assertTrue(lns == self.linesnl)
        lns = ilf.getlines(3, 3)
        self.assertTrue(lns == self.linesnl)
        ilf.close()

    def test_06_getlnstxt(self):
        ilf = ilff.open('test.ilff')
        lns = ilf.getlinestxt(0, 6)
        print(f'6: "{lns}"')
        self.assertTrue(lns == ''.join(self.linesnl *2))
        ilf.close()


class TestILFFWrites3(unittest.TestCase):

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
        with ilff.open(self.fname, 'a+', check=False) as ilf:
            ilf.buildindex()

    def test_02_get(self):
        with ilff.open(self.fname) as ilf:
            for i in range(3):
                l = ilf.getline(i)
                print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.linesnl[i])
                self.assertTrue(l == self.linesnl[i])

    def test_03_get2(self):
        with ilff.open(self.fname) as ilf:
            for i in range(3):
                l = ilf.getline(i)
                print('L:', i, '"%s"' % l)
                self.assertTrue(l == self.linesnl[i])

    def test_04_getlns(self):
        with ilff.open(self.fname) as ilf:
            lns = ilf.getlines(0, 3)
            print(lns)
            self.assertTrue(lns == self.linesnl)

    def test_05_getrange(self):
        with ilff.open(self.fname) as ilf:
            lns = ilf.getlinestxt(0, 3)
            print(lns)
            self.assertTrue(lns == ''.join(self.linesnl))


class TestILFFWrites4(unittest.TestCase):

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
        with ilff.ILFFFile(self.fname, 'a+', check=False) as ilf:
            ilf.buildindex()

    def test_02_get(self):
        with ilff.ILFFFile(self.fname) as ilf:
            for i in range(3):
                l = ilf.getline(i)
                chck = l == self.linesnl[i] if i < 2 else l == self.lines[i]
                print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], chck)
                self.assertTrue(chck)

    def test_03_get2(self):
        with ilff.ILFFFile(self.fname) as ilf:
            for i in range(3):
                l = ilf.getline(i)
                print('L:', i, '"%s"' % l)
                self.assertTrue(i > 1 or l == self.linesnl[i])
                self.assertTrue(i < 2 or l == self.lines[i])

    def test_04_getlns(self):
        with ilff.ILFFFile(self.fname) as ilf:
            lns = ilf.getlines(0, 3)
            print(f'4: "{lns}"')
            self.assertTrue(lns == self.linesnl[0:2] + self.lines[2:3])

    def test_05_getrange(self):
        with ilff.ILFFFile(self.fname) as ilf:
            lns = ilf.getlinestxt(0, 3)
            print(f'5: "{lns}"')
            self.assertTrue(lns == '\n'.join(self.lines))


class TestILFFWrites5(unittest.TestCase):

    lines = ['aaa4 5 d', 'bbbb b b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        ilf = ilff.open(self.fname, 'w', check=False)
        [ilf.write(l) for l in self.linesnl]
        ilf.close()

    def test_02_get(self):
        ilf = ilff.open(self.fname)
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.linesnl[i])
            self.assertTrue(l == self.linesnl[i])
        assert ilf.nlines() == 3
        ilf.close()

    def test_03_getln(self):
        self.lines += ['dddddddd dddddddd ddddd dddd', 'eeeee eeeeee eeeeeee eeeeee']
        ilf = ilff.open(self.fname, mode='r+')
        l = ilf.getline(1)
        ilf.write(self.lines[3])
        assert l == self.linesnl[1]
        assert ilf.nlines() == 4
        assert ilf.getline(3) == self.lines[3]
        ilf.close()


class TestILFFWrites6(unittest.TestCase):

    lines = ['aaa4 5 d', 'bbbb b b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        ilf = ilff.open(self.fname, 'w', check=False)
        [ilf.write(l) for l in self.linesnl]
        ilf.close()

    def test_04_erase(self):
        ilf = ilff.open(self.fname, mode="r+")
        ilf.eraseLine(1)
        assert ilf.nlines() == 3
        ilf.close()

    def test_05_get2(self):
        ilf = ilff.open(self.fname)
        for i in range(3):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l)
            self.assertTrue(i == 1 or l == self.linesnl[i])
            self.assertTrue(i != 1 or l.strip() == "")
        assert ilf.nlines() == 3
        ilf.close()

    def test_06_compact(self):
        ilf = ilff.open(self.fname, mode="r+")
        ilf.compact()
        assert ilf.nlines() == 2
        ilf.close()

    def test_07_get2(self):
        ilf = ilff.open(self.fname)
        for i in range(2):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l)
            self.assertTrue(i != 0 or l == self.linesnl[0])
            self.assertTrue(i != 1 or l == self.linesnl[2])
        ilf.close()

    def test_08_erase2(self):
        ilf = ilff.open(self.fname, mode="r+")
        self.lines += ['dddddddd dddddddd ddddd dddd', 'eeeee eeeeee eeeeeee eeeeee']
        ilf.write(self.lines[3])
        ilf.eraseLine(1)
        ilf.write(self.lines[4] + '\n')
        assert ilf.nlines() == 4
        ilf.close()

    def test_08_get3(self):
        ilf = ilff.open(self.fname, mode="r")
        print(ilf.getlines(0, 4))
        for i in range(4):
            l = ilf.getline(i)
            print('L:', i, '"%s"' % l)
            if i == 0:
                self.assertTrue(l == self.linesnl[0])
            if i == 1:
                self.assertTrue(l.strip() == '')
            if i == 2:
                self.assertTrue(l == self.lines[3])
            if i == 3:
                self.assertTrue(l == self.lines[4] + '\n')


class TestILFFWrites7(unittest.TestCase):

    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        ilf = ilff.open(self.fname, 'w')
        ilf.write(self.linesnl)
        assert ilf.nlines() == len(self.lines)
        ilf.close()

    def test_02_get1(self):
        ilf = ilff.open(self.fname)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = ilf.getline(i)
            self.assertTrue(l == self.linesnl[i])
        ilf.close()


class TestILFFWrites8(unittest.TestCase):

    sep = 'ü'
    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + 'ü' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        ilf = ilff.open(self.fname, 'w', sep=self.sep)
        ilf.writeLines(self.txt)
        assert ilf.nlines() == len(self.lines)
        ilf.close()

    def test_02_get1(self):
        ilf = ilff.open(self.fname)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = ilf.getline(i)
            assert l == self.linesnl[i]
        ilf.close()

    def test_03_get2(self):
        ilf = ilff.open(self.fname)
        print(ilf.getlinestxt(0, len(self.lines)))
        print(ilf.getlines(0, len(self.lines)))


class TestILFFWrites9(unittest.TestCase):

    sep = 'xyz'
    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + 'xyz' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'
    enc = 'latin1'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        print(dir(ilff))
        ilf = ilff.open(self.fname, 'w', sep=self.sep, encoding=self.enc)
        ilf.writeLines(self.txt)
        assert ilf.nlines() == len(self.lines)
        ilf.close()

    def test_02_get1(self):
        ilf = ilff.open(self.fname, encoding=self.enc)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = ilf.getline(i)
            assert l == self.linesnl[i]
        ilf.close()

    def test_03_get2(self):
        ilf = ilff.open(self.fname, encoding=self.enc)
        txt = ilf.getlinestxt(0, len(self.lines))
        assert(txt == self.txt)
        lns = ilf.getlines(0, len(self.lines))
        assert(lns == self.linesnl)
        ilf.close()

    def _test_04_compact(self):
        # does not work, arbitrary ewline required
        return
        ilf = ilff.open(self.fname, 'a+', sep=self.sep, encoding=self.enc)
        ilf.compact(empty=None)
        ilf.dumpindex()
        ilf.close()

    def test_05_get3(self):
        ilf = ilff.open(self.fname, encoding=self.enc)
        txt = ilf.getlinestxt(0, len(self.lines))
        assert ilf.nlines() == len(self.lines)
        assert(txt == self.txt)
        lns = ilf.getlines(0, len(self.lines))
        assert(lns == self.linesnl)


class TestILFFWrites10(unittest.TestCase):

    sep = 'äöü'
    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + 'äöü' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'
    enc = 'utf8'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        ilf = ilff.open(self.fname, 'w', sep=self.sep, encoding=self.enc)
        ilf.writeLines(self.txt)
        ilf.dumpindex()
        assert ilf.nlines() == len(self.lines)
        ilf.close()

    def test_02_get1(self):
        ilf = ilff.open(self.fname, encoding=self.enc)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = ilf.getline(i)
            assert l == self.linesnl[i]
        ilf.close()

    def test_03_get2(self):
        ilf = ilff.open(self.fname, encoding=self.enc)
        print(ilf.getlinestxt(0, len(self.lines)))
        print(ilf.getlines(0, len(self.lines)))


class TestILFFWrites11(unittest.TestCase):

    sep = '\n'
    data = [dict(a=1,b=2,c=3),
            dict(d=1,e=2,f=3),
            dict(g=11,h=12,i=13)]
    lines = [json.dumps(v, indent=None) for v in data]
    linesnl = [l + '\n' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'
    enc = 'utf8'

    @classmethod
    def tearDownClass(self):
        ilff.unlink(self.fname)

    def test_01_write(self):
        print(self.lines)
        print(self.linesnl)
        ilf = ilff.open(self.fname, 'w', sep=self.sep, encoding=self.enc)
        [ilf.write(record) for record in self.lines]
        ilf.dumpindex()
        assert ilf.nlines() == len(self.lines)
        ilf.close()

    def test_02_get1(self):
        ilf = ilff.open(self.fname, encoding=self.enc)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = ilf.getline(i)
            assert l == self.lines[i]
            d = json.loads(l)
            assert d == self.data[i]
        ilf.close()

    def test_03_get2(self):
        ilf = ilff.open(self.fname, encoding=self.enc)
        print('all text', ilf.getlinestxt(0, len(self.lines)))
        print('all records', ilf.getlines(0, len(self.lines)))


if __name__ == '__main__':
    unittest.main()
