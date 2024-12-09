import asyncio
import pytest
import pytest_asyncio
import os
import sys
import uuid
import json

sys.path.append('..')

import ilff
from aiaio import aio as aiomodule


@pytest_asyncio.fixture(loop_scope="module", scope="module")
async def per_module_fixture():
    yield True
    await aiomodule.release_globals()


pytestmark = pytest.mark.asyncio(loop_scope="module")
loop: asyncio.AbstractEventLoop


class TestStringMethods:

    async def test_upper(self, per_module_fixture):
        assert 'foo'.upper() == 'FOO'

    async def test_isupper(self):
        assert 'FOO'.isupper()
        assert not 'Foo'.isupper()

    async def test_split(self):
        s = 'hello world'
        assert s.split() == ['hello', 'world']


class TestILFFAWrites01:

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    @classmethod
    def teardown_class(self):
        ilff.unlink('test.ilff')

    async def test_01_create(self):
        ilf = await ilff.async_open('test.ilff', mode='w')
        assert (os.path.exists('test.ilff'))
        await ilf.close()

    async def test_02_write(self):
        ilf = await ilff.async_open('test.ilff', mode='w')
        rc = [*map(lambda x: ilf.write(x), self.linesnl)]
        await asyncio.gather(*rc)
        assert (os.path.exists('test.ilff'))
        assert (ilf.nlines() == 3)
        await ilf.dumpindex()
        await ilf.close()

    async def test_03_get1(self):
        ilf = await ilff.async_open('test.ilff', mode='r')
        l1 = await ilf.getline(0)
        print('L1:', l1)
        assert (l1 == 'aaa\n')
        assert (ilf.nlines() == 3)
        await ilf.close()

    async def test_04_get2(self):
        ilf = await ilff.async_open('test.ilff')
        await ilf.dumpindex()
        assert (ilf.nlines() == 3)
        for i in range(3):
            l = await ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.lines[i] + '\n')
            assert (l == self.lines[i] + '\n')
        assert (ilf.nlines() == 3)
        await ilf.close()

    async def test_05_get3(self):
        ilf = await ilff.async_open('test.ilff')
        for i in range(3):
            l = await ilf.getline(i)
            assert (l == self.lines[i] + '\n')
            print('L:', i, l, self.lines[i])
        await ilf.close()

    async def test_06_getlns(self):
        ilf = await ilff.async_open('test.ilff')
        lns = await ilf.getlines(0, 3)
        assert (lns == self.linesnl)
        await ilf.close()

    async def test_07_getlnstxt(self):
        ilf = await ilff.async_open('test.ilff')
        lns = await ilf.getlinestxt(0, 3)
        print(f'7: "{lns}"')
        assert (lns == '\n'.join(self.lines) + '\n')
        await ilf.close()

    async def test_08_getlnstxt2(self):
        ilf = await ilff.async_open('test.ilff')
        lns = await ilf.getlinestxt(0, 2)
        print(f'8: "{lns}"')
        assert (lns == '\n'.join(self.lines[0:2]) + '\n')
        await ilf.close()

    async def test_09_getlnstxt3(self):
        ilf = await ilff.async_open('test.ilff')
        lns = await ilf.getlinestxt(1, 2)
        print(f'8: "{lns}"')
        assert (lns == '\n'.join(self.lines[1:3]) + '\n')
        await ilf.close()


class TestILFFAWrites02:

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    @classmethod
    def teardown_class(self):
        ilff.unlink('test.ilff')

    async def test_01_append(self):
        ilf = await ilff.async_open('test.ilff', mode='w')
        r = [*map(lambda x: ilf.write(x), self.linesnl)]
        await asyncio.gather(*r)
        assert (os.path.exists('test.ilff'))
        assert (ilf.nlines() == 3)
        await ilf.close()

    async def test_02_get2(self):
        ilf = await ilff.async_open('test.ilff', mode='r')
        for i in range(3):
            l = await ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.lines[i] + '\n')
            assert (l == self.lines[i] + '\n')
        await ilf.close()

    async def test_03_append(self):
        ilf = await ilff.async_open('test.ilff', mode='a')
        await ilf.write(self.linesnl)
        assert (os.path.exists('test.ilff'))
        assert (ilf.nlines() == 6)
        await ilf.close()

    async def test_04_get(self):
        ilf = await ilff.async_open('test.ilff', mode='r')
        for i in range(6):
            l = await ilf.getline(i)
            print('Ldd:', i, '"%s"' % l, '"%s"' % self.lines[i % 3], l == self.lines[i % 3] + '\n')
            assert (l == self.lines[i % 3] + '\n')
        await ilf.close()

    async def test_05_getlns(self):
        ilf = await ilff.async_open('test.ilff')
        lns1 = await ilf.getlinestxt(0, 3)
        lns = await ilf.getlines(0, 3)
        assert (ilf.nlines() == 6)
        assert (lns == self.linesnl)
        lns = await ilf.getlines(3, 3)
        assert (lns == self.linesnl)
        await ilf.close()

    async def test_06_getlnstxt(self):
        ilf = await ilff.async_open('test.ilff')
        lns = await ilf.getlinestxt(0, 6)
        print(f'6: "{lns}"')
        assert (lns == ''.join(self.linesnl *2))
        await ilf.close()


class TestILFFAWrites03:

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        of = open(self.fname, 'w', newline='\n')
        of.write('\n'.join(self.lines) + '\n')
        of.close()

    async def test_01a_buildindex(self):
        async with ilff.AILFFFile(self.fname, 'a+', check=False) as ilf:
            await ilf.buildindex()

    async def test_02_get(self):
        async with ilff.AILFFFile(self.fname) as ilf:
            for i in range(3):
                l = await ilf.getline(i)
                print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.linesnl[i])
                assert (l == self.linesnl[i])

    async def test_03_get2(self):
        async with await ilff.async_open(self.fname) as ilf:
            for i in range(3):
                l = await ilf.getline(i)
                print('L:', i, '"%s"' % l)
                assert (l == self.linesnl[i])

    async def test_04_getlns(self):
        async with await ilff.async_open(self.fname) as ilf:
            lns = await ilf.getlines(0, 3)
            print(lns)
            assert (lns == self.linesnl)

    async def test_05_getrange(self):
        async with await ilff.async_open(self.fname) as ilf:
            lns = await ilf.getlinestxt(0, 3)
            print(lns)
            assert (lns == ''.join(self.linesnl))


class TestILFFAWrites04:

    lines = ['aaa', 'bbbb b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]

    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        of = open(self.fname, 'w', newline='\n')
        of.write('\n'.join(self.lines))
        of.close()

    async def test_01a_buildindex(self):
        async with ilff.AILFFFile(self.fname, 'a+', check=False) as ilf:
            await ilf.buildindex()

    async def test_02_get(self):
        async with ilff.AILFFFile(self.fname) as ilf:
            for i in range(3):
                l = await ilf.getline(i)
                chck = l == self.linesnl[i] if i < 2 else l == self.lines[i]
                print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], chck)
                assert (chck)

    async def test_03_get2(self):
        async with ilff.AILFFFile(self.fname) as ilf:
            for i in range(3):
                l = await ilf.getline(i)
                print('L:', i, '"%s"' % l)
                assert (i > 1 or l == self.linesnl[i])
                assert (i < 2 or l == self.lines[i])

    async def test_04_getlns(self):
        async with ilff.AILFFFile(self.fname) as ilf:
            lns = await ilf.getlines(0, 3)
            print(f'4: "{lns}"')
            assert (lns == self.linesnl[0:2] + self.lines[2:3])

    async def test_05_getrange(self):
        async with ilff.AILFFFile(self.fname) as ilf:
            lns = await ilf.getlinestxt(0, 3)
            print(f'5: "{lns}"')
            assert (lns == '\n'.join(self.lines))


class TestILFFAWrites05:

    lines = ['aaa4 5 d', 'bbbb b b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        ilf = await ilff.async_open(self.fname, 'w', check=False)
        await asyncio.gather(*[ilf.write(l) for l in self.linesnl])
        await ilf.close()

    async def test_02_get(self):
        ilf = await ilff.async_open(self.fname)
        for i in range(3):
            l = await ilf.getline(i)
            print('L:', i, '"%s"' % l, '"%s"' % self.lines[i], l == self.linesnl[i])
            assert (l == self.linesnl[i])
        assert ilf.nlines() == 3
        await ilf.close()

    async def test_03_getln(self):
        self.lines += ['dddddddd dddddddd ddddd dddd', 'eeeee eeeeee eeeeeee eeeeee']
        ilf = await ilff.async_open(self.fname, mode='r+')
        l = await ilf.getline(1)
        await ilf.write(self.lines[3])
        assert l == self.linesnl[1]
        assert ilf.nlines() == 4
        assert await ilf.getline(3) == self.lines[3]
        await ilf.close()


class TestILFFAWrites06:

    lines = ['aaa4 5 d', 'bbbb b b', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        ilf = await ilff.async_open(self.fname, 'w', check=False)
        await asyncio.gather(*[ilf.write(l) for l in self.linesnl])
        await ilf.close()

    async def test_04_erase(self):
        ilf = await ilff.async_open(self.fname, mode="r+")
        await ilf.eraseLine(1)
        assert ilf.nlines() == 3
        await ilf.close()

    async def test_05_get2(self):
        ilf = await ilff.async_open(self.fname)
        for i in range(3):
            l = await ilf.getline(i)
            print('L:', i, '"%s"' % l)
            assert (i == 1 or l == self.linesnl[i])
            assert (i != 1 or l.strip() == "")
        assert ilf.nlines() == 3
        await ilf.close()

    async def test_06_compact(self):
        ilf = await ilff.async_open(self.fname, mode="r+")
        await ilf.compact()
        assert ilf.nlines() == 2
        await ilf.close()

    async def test_07_get2(self):
        ilf = await ilff.async_open(self.fname)
        for i in range(2):
            l = await ilf.getline(i)
            print('L:', i, '"%s"' % l)
            assert (i != 0 or l == self.linesnl[0])
            assert (i != 1 or l == self.linesnl[2])
        await ilf.close()

    async def test_08_erase2(self):
        ilf = await ilff.async_open(self.fname, mode="r+")
        self.lines += ['dddddddd dddddddd ddddd dddd', 'eeeee eeeeee eeeeeee eeeeee']
        await ilf.write(self.lines[3])
        await ilf.eraseLine(1)
        await ilf.write(self.lines[4] + '\n')
        assert ilf.nlines() == 4
        await ilf.close()

    async def test_08_get3(self):
        ilf = await ilff.async_open(self.fname, mode="r")
        print(await ilf.getlines(0, 4))
        for i in range(4):
            l = await ilf.getline(i)
            print('L:', i, '"%s"' % l)
            if i == 0:
                assert (l == self.linesnl[0])
            if i == 1:
                assert (l.strip() == '')
            if i == 2:
                assert (l == self.lines[3])
            if i == 3:
                assert (l == self.lines[4] + '\n')
        await ilf.close()


class TestILFFAWrites07:

    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + '\n' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        ilf = await ilff.async_open(self.fname, 'w')
        await ilf.write(self.linesnl)
        assert ilf.nlines() == len(self.lines)
        await ilf.close()

    async def test_02_get1(self):
        ilf = await ilff.async_open(self.fname)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = await ilf.getline(i)
            assert (l == self.linesnl[i])
        await ilf.close()


class TestILFFAWrites08:

    sep = 'ü'
    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + 'ü' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        ilf = await ilff.async_open(self.fname, 'w', sep=self.sep)
        await ilf.writeLines(self.txt)
        assert ilf.nlines() == len(self.lines)
        await ilf.close()

    async def test_02_get1(self):
        ilf = await ilff.async_open(self.fname)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = await ilf.getline(i)
            assert l == self.linesnl[i]
        await ilf.close()

    async def test_03_get2(self):
        ilf = await ilff.async_open(self.fname)
        print(await ilf.getlinestxt(0, len(self.lines)))
        print(await ilf.getlines(0, len(self.lines)))
        await ilf.close()


class TestILFFAWrites09:

    sep = 'xyz'
    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + 'xyz' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'
    enc = 'latin1'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        print(dir(ilff))
        ilf = await ilff.async_open(self.fname, 'w', sep=self.sep, encoding=self.enc)
        await ilf.writeLines(self.txt)
        assert ilf.nlines() == len(self.lines)
        await ilf.close()

    async def test_02_get1(self):
        ilf = await ilff.async_open(self.fname, encoding=self.enc)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = await ilf.getline(i)
            assert l == self.linesnl[i]
        await ilf.close()

    async def test_03_get2(self):
        ilf = await ilff.async_open(self.fname, encoding=self.enc)
        txt = await ilf.getlinestxt(0, len(self.lines))
        assert(txt == self.txt)
        lns = await ilf.getlines(0, len(self.lines))
        assert(lns == self.linesnl)
        await ilf.close()

    async def _test_04_compact(self):
        # does not work, arbitrary ewline required
        return
        ilf = await ilff.async_open(self.fname, 'a+', sep=self.sep, encoding=self.enc)
        await ilf.compact(empty=None)
        await ilf.dumpindex()
        await ilf.close()

    async def test_05_get3(self):
        ilf = await ilff.async_open(self.fname, encoding=self.enc)
        txt = await ilf.getlinestxt(0, len(self.lines))
        assert ilf.nlines() == len(self.lines)
        assert(txt == self.txt)
        lns = await ilf.getlines(0, len(self.lines))
        assert(lns == self.linesnl)
        await ilf.close()


class TestILFFAWrites10:

    sep = 'äöü'
    lines = ['aaa4 5 d', '', 'bbbb b b', '   ', 'ccccc cccc cc c']
    linesnl = [l + 'äöü' for l in lines]
    txt = ''.join(linesnl)
    fname = str(uuid.uuid4()) + '.ilff'
    enc = 'utf8'

    @classmethod
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        ilf = await ilff.async_open(self.fname, 'w', sep=self.sep, encoding=self.enc)
        await ilf.writeLines(self.txt)
        await ilf.dumpindex()
        assert ilf.nlines() == len(self.lines)
        await ilf.close()

    async def test_02_get1(self):
        ilf = await ilff.async_open(self.fname, encoding=self.enc)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = await ilf.getline(i)
            assert l == self.linesnl[i]
        await ilf.close()

    async def test_03_get2(self):
        ilf = await ilff.async_open(self.fname, encoding=self.enc)
        print(await ilf.getlinestxt(0, len(self.lines)))
        print(await ilf.getlines(0, len(self.lines)))
        await ilf.close()


class TestILFFAWrites11:

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
    def teardown_class(self):
        ilff.unlink(self.fname)

    async def test_01_write(self):
        print(self.lines)
        print(self.linesnl)
        ilf = await ilff.async_open(self.fname, 'w', sep=self.sep, encoding=self.enc)
        await asyncio.gather(*[ilf.write(record) for record in self.lines])
        await ilf.dumpindex()
        assert ilf.nlines() == len(self.lines)
        await ilf.close()

    async def test_02_get1(self):
        ilf = await ilff.async_open(self.fname, encoding=self.enc)
        assert ilf.nlines() == len(self.lines)
        for i in range(len(self.lines)):
            l = await ilf.getline(i)
            assert l == self.lines[i]
            d = json.loads(l)
            assert d == self.data[i]
        await ilf.close()

    async def test_03_get2(self):
        ilf = await ilff.async_open(self.fname, encoding=self.enc)
        print('all text', await ilf.getlinestxt(0, len(self.lines)))
        print('all records', await ilf.getlines(0, len(self.lines)))
        await ilf.close()
