import asyncio
import os, sys, shutil, io

#from aiofile import AIOFile, LineReader
from aiaio import AIOFile, LineReader

from .ilff import ILFFError, unlink, ILFFFile

class AILFFFile(ILFFFile):

    file = None

    def __init__(self, fname, mode='r', **kw):
        super().__init__(fname, mode=mode, **kw)

    def __del__(self):
        pass

    def __str__(self):
        return f'AILFFFile("{self.fname}", nlines={self._nlines}, @{self.idx})'

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def open(self):
        if self.file is not None:
            return
        self.file = AIOFile(self.fname, self.mode + 'b')
        await self.file.open()
        if self.isILFF or self.mode != 'r':
            self.idxfile = AIOFile(self.idxfilen, self.umode)
            await self.idxfile.open()
            self._nlines = int(os.path.getsize(self.idxfilen) / self.indexBytes)
            self.idx = (await self.readindex(self._nlines-1))[1]
            #print(f'lines: {self._nlines}, index: {self.idx}')
            if self._check:
                self.check()
        else:
            print(f'error: {self.fname} does not appear to be an indexed file')

    async def fsync(self):
        await self.idxfile.fsync()
        await self.file.fsync()

    async def close(self):
        await self.idxfile.close()
        await self.file.close()
        self.file = None

    async def readint(self, file, lnnum):
        if lnnum < 0:
            return (0, 0)
        idx1 = 0
        if lnnum > 0:
            offs = (lnnum-1)*self.indexBytes
            idxdata = await file.read(self.indexBytes*2, offset=offs)
            if len(idxdata) != self.indexBytes*2:
                raise ILFFError('ILFF: Error: Failed to read from index entry %d @ %d. Out of range?' %
                                (lnnum, offs))
            else:
                idx1 = int(0).from_bytes(idxdata[0:self.indexBytes], 'little')
                idx2 = int(0).from_bytes(idxdata[self.indexBytes:], 'little')
        else:
            assert(lnnum == 0)
            idxdata = await file.read(self.indexBytes)
            if len(idxdata) != self.indexBytes:
                raise ILFFError('ILFF: Error: Failed to read from index entry %d @ %d. Out of range?' %
                                (lnnum, 0))
            else:
                idx2 = int(0).from_bytes(idxdata, 'little')

        return (idx1, idx2)

    async def readindex(self, lnnum):
        return await self.readint(self.idxfile, lnnum)

    def nlines(self):
        return self._nlines

    def get_nlines(self):
        return self.nlines()

    async def writeLines(self, txt):
        if isinstance(txt, list):
            await self.write(txt)
        else:
            lines = txt.split(self.sep)
            if len(lines[-1]) == 0:
                lines = lines[0:-1]
            await self.write([v + self.sep for v in lines])

    async def write(self, txt):
        if isinstance(txt, list):
            await asyncio.gather(*[self.appendLine(v) for v in txt])
        else:
            await self.appendLine(txt)

    async def appendLine(self, txt):
        txtdata = txt.encode(self.encoding)
        llen = len(txtdata)
        curlns = self._nlines
        curidx = self.idx
        self.idx += llen
        self._nlines += 1
        await self.idxfile.write(self.idx.to_bytes(self.indexBytes, 'little'), offset=curlns*self.indexBytes)
        await self.file.write(txtdata, offset=curidx)

    async def buildindex(self):
        await self.idxfile.truncate()
        newidx = 0
        tasks = []
        i = 0
        async for s in LineReader(self.file):
            llen = len(s)
            if llen == 0:
                break
            newidx = newidx + llen
            tasks += [self.idxfile.write(newidx.to_bytes(self.indexBytes, 'little'), offset=i*self.indexBytes)]
            #res = await self.idxfile.write(newidx.to_bytes(self.indexBytes, 'little'), offset=i*self.indexBytes)
            #assert res == self.indexBytes
            i += 1
        await asyncio.gather(*tasks)

    async def fromfile(self, infile, empty=''):
        tasks = []
        async for s in LineReader(infile):
            if len(s) > 0 and s.strip() != empty:
                await self.appendLine(s)
            else:
                if len(s) > 0:
                    continue
                else:
                    break

    async def truncate(self):
        await self.file.truncate()
        await self.idxfile.truncate()
        self._nlines = 0
        self.idx = 0

    async def compact(self, empty=''):
        shutil.copy(self.fname, self.fname + '.bak')
        await self.truncate()
        async with AIOFile(self.fname + '.bak', 'r', encoding=self.encoding) as fcopy:
            await self.fromfile(fcopy, empty=empty)
        os.remove(self.fname + '.bak')

    async def getline(self, lnnum):
        (idx, idx2) = await self.readindex(lnnum)
        len = idx2 - idx
        if len == 0:
            return ""
        ln = await self.file.read(len, offset=idx)
        return ln.decode(self.encoding)

    async def getlines(self, start, nlines):
        (idx, idx2) = await self.readindex(start)
        len = idx2 - idx
        res = []
        for k in range(nlines):
            (idx, idx2) = await self.readindex(start + k)
            len = idx2 - idx
            ln = (await self.file.read(len, offset=idx)).decode(self.encoding)
            res.append(ln)
        return res

    async def getlinestxt(self, start, nlines):
        if nlines <= 0:
            return ''
        (idxs, idxs2) = await self.readindex(start)
        (idxe, idxe2) = await self.readindex(start+nlines-1)
        ramount = idxe2 - idxs
        ln = b''
        ln = await self.file.read(ramount, offset=idxs)
        return ln.decode(self.encoding)

    async def dumpindex(self):
        print('Number of Lines: ', self.get_nlines())
        for i in range(self.get_nlines()):
            (idx1, idx2) = await self.readindex(i)
            ln = idx2 - idx1
            print('%d: %d - %d (%d)' % (i, idx1, idx2, ln))

    async def eraseLine(self, ind, repl=""):
        (idx, idx2) = await self.readindex(ind)
        ln = idx2 - idx
        n = ln - len(repl) -1
        if n < 0:
            print('cannot erase line %d of %s (ln %d)' % (ind, self.fname, n))
            raise ILFFError('erase')
            return
        white = ' ' * (n)
        bts = (repl + white).encode(self.encoding)
        await self.file.write(bts[0:ln], offset=idx)


py_open = open
async def open(name, mode='r', encoding='utf8', **kw):
    ilff = AILFFFile(name, mode=mode, encoding=encoding, **kw)
    await ilff.open()
    return ilff
