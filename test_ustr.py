from ustr import Ustr
# import ustr
# ustr.core.box_char_width = 2


def test_test():
    # all eng
    t = Ustr('test')
    assert len(t) == 4
    assert t.width == 4
    assert t.widthdiff == 0
    assert t.maxwidth is None

    # some double width chars
    t = Ustr('测试test')
    assert len(t) == 8
    assert t.width == 8
    assert t.widthdiff == 2
    assert t.maxwidth is None

    assert t[0] == '测'
    assert t[1] == '测'
    assert t[2] == '试'
    assert t[3] == '试'
    assert t[4] == 't'
    assert t[5] == 'e'
    assert t[6] == 's'
    assert t[7] == 't'
    try:
        _ = t[8]
    except Exception as e:
        assert type(e) is IndexError

    assert t[-1] == 't'
    assert t[-2] == 's'
    assert t[-3] == 'e'
    assert t[-4] == 't'
    assert t[-5] == '试'
    assert t[-6] == '试'
    assert t[-7] == '测'

    assert t[0:2] == t[:2]
    # assert t[0:2] == t[0] + t[1]

    assert t[0:2] == '测'
    assert t[0:3] == '测试'
    assert t[2:3] == '试'
    assert t[2:4] == '试'
    assert t[2:5] == '试t'
    assert t[::-1] == '测试test'[::-1]
    assert t[4:2:-1] == t[4] + t[3]
    assert t[6:1:-2] == 'st试'
    assert t[6:1:-2] == t[6] + t[4] + t[2]

    assert t.ljust(10) == '测试test  '
    assert t.rjust(10) == '  测试test'
    assert t.zfill(10) == '00测试test'

    # stripped by maxlength
    t = Ustr('测试test', 6)
    assert len(t) == 6
    assert t.width == 6
    assert t.widthdiff == 2
    assert t.maxwidth == 6
    assert t.maxwidth == len(t)

    assert t[0] == '测'
    assert t[1] == '测'
    assert t[2] == '试'
    assert t[3] == '试'
    assert t[4] == 't'
    assert t[5] == 'e'
    try:
        _ = t[6]
    except Exception as e:
        assert type(e) is IndexError

    assert Ustr.diff('测试test') == 2
    assert Ustr.diff('测试test测试') == 4
    assert Ustr.diff('测试test测试', 6) == 2

    assert Ustr.len('测试test') == 8
    assert Ustr.len('测试test测试') == 12
    assert Ustr.len('测试test测试', 6) == 6

    assert Ustr('测试test测试', 6).content == '测试test测试'
    assert Ustr('测试test测试', 6) == '测试te'
