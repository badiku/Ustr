from wcwidth import wcwidth
import re
import string

def getfont():
    # check terminal font, 11 means double width for box-drawing characters
    import win32console
    stdout = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
    return stdout.GetCurrentConsoleFont()[0]


currentfont = 1
try:
    currentfont = getfont()
except Exception as e:
    pass  # no need to check, ignore any error


def uwcwidth(wc):
    # box-drawing characters is 2 in some fonts
    if 0x2500 <= ord(wc) < 0x2573:
        if currentfont != 1:
            return 2
        else:
            return 1
    return wcwidth(wc)


class Ustr(str):
    # unicode string, length by wcwidth, without unprintable characters
    def __new__(cls, content, maxwidth=None):
        content = str(content)
        end = len(content)
        idx = slice(0, end)
        width = 0
        diff = 0
        need = []
        for char in content[idx]:
            wcw = uwcwidth(char)
            if wcw > 0:
                need.append(char)
                width += wcw
                diff += wcw - 1
            if maxwidth:
                if width >= maxwidth:
                    break
        txt = ''.join(need)
        s = str.__new__(cls, txt)
        s.width = width
        s.widthdiff = diff
        s.maxwidth = maxwidth
        s.content = content
        return s

    def __len__(self):
        return self.width

    def __getitem__(self, n):
        width = self.width
        if type(n) is slice:
            start = (n.start + width) % width if n.start else 0
            stop = (n.stop + width) % width if n.stop else width
            step = n.step if n.step else 1
            if n.start is None and n.stop is None and step < 0:
                start, stop = stop - 1, start - 1
            irange = range(start, stop, step)
            istep = 1 if step > 0 else -1
            return ''.join(self[i] for i in irange
                           if i == start
                           or (i - istep) % width not in irange
                           or self[i] != self[(i - istep) % width]
                           )
        if n < 0:
            n = width + n
        if n > width - 1:
            return ''[n]
        return str(Ustr(self, n + 1))[-1]

    @staticmethod
    def len(content, maxwidth=None):
        return Ustr(content, maxwidth).width

    @staticmethod
    def diff(content, maxwidth=None):
        return Ustr(content, maxwidth).widthdiff

    def ljust(self, n, char=' '):
        diff = n - self.width
        pad = Ustr(char * diff, diff)
        return self + pad

    def zfill(self, n):
        return self.rjust(n, char='0')

    def rjust(self, n, char=' '):
        diff = n - self.width
        pad = Ustr(char * diff, diff)
        return pad + self

    def format(self, *args, **kwargs):
        fields = list(string.Formatter.parse('', self))
        j = 0
        changed = False
        for i,n in enumerate(fields):
            if n[1] is None and n[2] is None and n[3] is None:
                continue
            name = n[1]
            value = string.Formatter.get_value('', name if name else j, args, kwargs)
            if not name:
                j = j +1
            if not issubclass(type(value), str):
                continue
            diff = Ustr.diff(value)
            oldlength = n[2]
            if oldlength and diff:
                reresult = re.search('\d+', oldlength)
                if reresult:
                    changed = True
                    oldlen = int(reresult.group(0))
                    newlen = oldlen - diff
                    newlength = re.sub('\d+', str(newlen), oldlength, 1)
                    fields[i] = (fields[i][0], fields[i][1], newlength, fields[i][3])

        if changed:
            format_string = ''.join(['{0[0]}{{{0[1]}!{0[3]}:{0[2]}}}'.format(n).replace('!None', '').replace('{None:None}', '').replace(':}', '}')  for i,n in enumerate(fields)])
            return format_string.format(*args,**kwargs)
        else:
            return str(self).format(*args,**kwargs)
