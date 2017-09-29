ustr
-------

unicode string, for better alignment with CJK characters


get length by wcwidth, without unprintable characters


    >>> from ustr import Ustr
    >>> mystr = Ustr('测试test', 6)
    >>>
    >>> print(mystr)
    测试te



    >>> print(mystr.ljust(8) + '|--')
    测试te  |--
    >>> print('mystr'.ljust(8) + '|--')
    mystr   |--



    >>> print(mystr.rjust(8) + '|--')
      测试te|--
    >>> print('mystr'.rjust(8) + '|--')
       mystr|--



    >>> print(mystr.zfill(8))
    00测试te



    >>> print(Ustr('{:>10}test').format('测试test'))
      测试testtest
    >>> print(Ustr('{:>10}test').format('test'))
          testtest



    >>> print(Ustr('{:<10}test').format('测试test'))
    测试test  test
    >>> print(Ustr('{:<10}test').format('test'))
    test      test



    >>> print(len('测试test'))
    8


    >>> print(mystr.maxwidth, mystr.widthdiff)
    6 2
    >>> print(len(mystr))
    6


    >>> print(Ustr.diff('测试test', 6))
    2
    >>> print(Ustr.len('测试test', 6))
    6
