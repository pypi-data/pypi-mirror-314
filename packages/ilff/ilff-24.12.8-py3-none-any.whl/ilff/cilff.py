import os, sys, shutil, errno

from .ilff import ILFFError

from ctypes import CDLL, POINTER, c_int, c_int64, c_char_p, c_void_p

c_iladdr = c_int64
c_iladdr_p = POINTER(c_iladdr)

c_char_pp = POINTER(c_char_p)


def configLib(lib):

    lib.ilffOpen.argtypes = (c_char_p, c_char_p, c_int)
    lib.ilffOpen.restype = c_void_p

    lib.ilffClose.argtypes = (c_void_p,)
    lib.ilffClose.restype = c_int

    lib.ilffFlush.argtypes = (c_void_p,)
    lib.ilffFlush.restype = c_int

    lib.ilffTruncate.argtypes = (c_void_p,)
    lib.ilffTruncate.restype = c_int

    lib.ilffWrite.argtypes = (c_void_p, c_char_p, c_iladdr)
    lib.ilffWrite.restype = c_int

    lib.ilffWriteLine.argtypes = (c_void_p, c_char_p, c_iladdr)
    lib.ilffWrite.restype = c_int

    lib.ilffGetLine.argtypes = (c_void_p, c_iladdr, c_char_p, c_iladdr_p)
    lib.ilffGetLine.restype = c_int

    lib.ilffGetLines.argtypes = (c_void_p, c_iladdr, c_iladdr, c_char_pp, c_iladdr_p)
    lib.ilffGetLines.restype = c_int

    lib.ilffGetRange.argtypes = (c_void_p, c_iladdr, c_iladdr, c_char_p, c_iladdr_p)
    lib.ilffGetRange.restype = c_int

    lib.ilffNLines.argtypes = (c_void_p,)
    lib.ilffNLines.restype = c_iladdr

    lib.ilffCheck.argtypes = (c_void_p,)
    lib.ilffCheck.restype = c_int

    lib.ilffReindex.argtypes = (c_void_p,)
    lib.ilffReindex.restype = c_int

    lib.ilffDumpindex.argtypes = (c_void_p,)
    lib.ilffDumpindex.restype = c_int

    lib.ilffRemove.argtypes = (c_char_p,)
    lib.ilffRemove.restype = c_int


def getLib():
    lib = None
    mfile = sys.modules['ilff.cilff'].__file__
    csrcdir = os.path.join(os.path.dirname(mfile), '..', 'src')
    libnames = ['ilff', os.path.join(csrcdir, 'ilff')] if os.name == "nt" else \
        ['libilff.so.0', os.path.join(csrcdir, 'libilff.so.0')]
    for name in libnames:
        try:
            lib = CDLL(name)
            # print(f'found cILFF library {name}')
            break
        except:
            pass
    if lib:
        configLib(lib)
    return lib


class CILFFError(ILFFError):
    def __init__(self, s):
        super().__init__(f'cILFF operation failed: {s}')


class CILFFFile:

    fname = ''
    mode = 'r'
    encoding = 'utf8'
    nameenc = 'utf8'
    isILFF = True
    lib = getLib()
    handle = 0

    def __init__(self, fname, mode='r', encoding='utf8', nameenc='utf8', symlinks=True, check=True, flushIndex=True):
        if self.lib is None:
            raise CILFFError('cILFF library not available')
        self.fname = fname
        self.idxfilen = fname + '.iidx'
        if encoding is not None:
            self.encoding = encoding
        if nameenc is not None:
            self.nameenc = nameenc
        self.mode = mode
        flags = (1 if check else 0) | (2 if symlinks else 0) | (4 if flushIndex else 0)
        self.handle = self.lib.ilffOpen(self.fname.encode(self.nameenc), self.mode.encode(self.nameenc), c_int(flags))
        if not self.handle:
            raise CILFFError('open')

    def __del__(self):
        self.close()

    def __str__(self):
        return f'CILFFFile("{self.fname}", nlines={self.nlines()}, @{self.handle})'

    def remove(self, name=None):
        if type(self) == str:
            name = self
            nameenc = CILFFFile.nameenc
        else:
            name = self.fname
            nameenc = self.nameenc
        return CILFFFile.lib.ilffRemove(name.encode(nameenc))

    def close(self):
        if self.handle:
            self.lib.ilffClose(self.handle)
            self.handle = None

    def dumpindex(self):
        return self.lib.ilffDumpindex(self.handle)

    def buildindex(self):
        return self.reindex()

    def reindex(self):
        return self.lib.ilffReindex(self.handle)

    def truncate(self):
        return self.lib.ilffTruncate(self.handle)

    def flush(self):
        return self.lib.ilffFlush(self.handle)

    def nlines(self):
        return self.lib.ilffNLines(self.handle)

    def get_nlines(self):
        return self.nlines()

    def writeLines(self, txt):
        if isinstance(txt, list):
            self.write(txt)
        else:
            lines = txt.split(self.sep)
            if len(lines[-1]) == 0:
                lines = lines[0:-1]
            self.write([v + self.sep for v in lines])

    def write(self, txt):
        if isinstance(txt, list):
            return any([self.appendLine(v) for v in txt])
        else:
            return self.appendLine(txt)

    def appendLine(self, txt):
        b = txt.encode(self.encoding)
        return self.lib.ilffWrite(self.handle, b, len(b))

    def fromfile(self, infile, empty=''):
        while True:
            s = infile.readline()
            if len(s) > 0 and s.strip() != empty:
                self.appendLine(s)
            else:
                if len(s) > 0:
                    continue
                else:
                    break

    def getline(self, lnnum):
        rlen = c_iladdr()
        self.lib.ilffGetLine(self.handle, lnnum, None, rlen)
        if rlen.value < 0:
            raise CILFFError('got negative line size')
        bln = b' ' * rlen.value
        self.lib.ilffGetLine(self.handle, lnnum, bln, rlen)
        tln = bln[0:rlen.value].decode(self.encoding)
        return tln

    def getlines(self, lnnum, nlines):
        rlens = (c_iladdr * nlines)()
        self.lib.ilffGetLines(self.handle, lnnum, nlines, None, rlens, nlines)
        lndata = (c_char_p * nlines)()
        for (i, rlen) in enumerate(rlens):
            lndata[i] = b'\00' * rlen
        self.lib.ilffGetLines(self.handle, lnnum, nlines, lndata, rlens, nlines)
        lines = [ln.decode(self.encoding) for ln in lndata]
        return lines

    def getlinestxt(self, start, nlines):
        rlen = c_iladdr()
        self.lib.ilffGetRange(self.handle, start, nlines, None, rlen)
        bln = b' ' * rlen.value
        self.lib.ilffGetRange(self.handle, start, nlines, bln, rlen)
        tln = bln[0:rlen.value].decode(self.encoding)
        return tln
