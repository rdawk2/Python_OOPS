"""
590PR Spring 2018
Assignment 6 – Object Oriented Programming
For this assignment, you will complete the code for this object-oriented class in Python called 'IntWords'.
The class can store and interpret integer values as Python strings containing the proper English phrases for those
values, but with implementation of the methods needed so that the common standard arithmetic and comparison operators
work correctly. Note that as described on Summerfield page 380, simply implementing the < <= and == operators will
automatically generate the other comparison methods. Also, as a side-effect of implementing the comparison operators,
sorting functions like sorted() should automatically work properly too.
Like native Python integers and strings, the class should be immutable.  Therefore, as with Summerfield's "FuzzyBool"
class on page 249, the attribute(s) of the object must be private, and have no setter methods.
Make all class variables and instance variables private.
>>> a = IntWords('Forty Two')
>>> b = IntWords('Seven')
>>> print(a + b)
forty nine
>>> print(a // b)
six
>>> a + (b * IntWords('two'))
IntWords('fifty six')
>>> x = IntWords('two hundred, forty five') * IntWords('three hundred twelve')
>>> print(x)
seventy six thousand four hundred forty
>>> int(x)
76440
>>> a  # test object representation:
IntWords('forty two')
>>> print(a)  # test printability:
forty two
>>> c = IntWords('One thousand, three hundred five')
>>> int(c)
1305
>>> a <= a
True
>>> a < a
False
>>> c > a   # test automatic implementation of __gt__ method
True
>>> IntWords('three') <= IntWords('negative five')
False
>>> sorted([c, a, b, a])
[IntWords('seven'), IntWords('forty two'), IntWords('forty two'), IntWords('one thousand three hundred five')]
>>> some_dictionary = {a: 1, b: 2, c: 3}
>>> some_dictionary[c]
3
"""

one = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
tenp = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen',
        'nineteen']
tenp2 = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


import re
class IntWords:
    # put your class variables here, prefixed with __ to make them private:

    def __init__(self, number_name):
        # Set your instance variables here inside __init__().
        # Prefix their names with __ to make them private
        self.__number_name = IntWords.normalize_number_phrase(number_name.lower())
        self.__int_value = IntWords.parse_name(number_name)
        self.__str_name = self.__number_name
        #self.from_int(211000005)

    @staticmethod
    def normalize_number_phrase(phr: str) -> str:
        """Given a string which should contain a number in English words,
        normalize it to remove any commas, extra spaces, or the word 'and'"""
        phr = re.sub(r'\band\b\s+', "", phr)
        return phr.replace(',', '').strip().lower()  # remove any commas and outer spaces.

    @staticmethod
    def parse_name(expr: str) -> int:
        """Given a string name of an integer, convert it into the actual integer value.
        Ignores commas and the word 'and'.

        :param expr:
        :return: the integer equivalent of the phrase

        >>> IntWords.parse_name('Four hundred thirty five')
        435
        >>> IntWords.parse_name('four hundred and thirty five')
        435
        >>> IntWords.parse_name('twenty eight')
        28
        >>> IntWords.parse_name('thirteen trillion sixty seven billion nine hundred forty one million two hundred fifty three thousand')
        13067941253000
        >>> IntWords.parse_name('ninety four thousand, eight hundred ten')
        94810
        >>> IntWords.parse_name('negative twenty one')
        -21
        """
        expr = IntWords.normalize_number_phrase(expr.lower())

        numwords = {}
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]


        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)
        negative_flag = 0
        current = result = 0
        for word in expr.split():
            if word not in numwords:
                if word == 'negative':
                    negative_flag = 1
                    # raise Exception("Illegal word: " + word)

            else:

                scale, increment = numwords[word]
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
        if negative_flag == 1:
            return (0 - (result + current))
        else:
            return result + current

    def __repr__(self) -> str:
        """Return the eval() compatible object representation."""
        return "IntWords('{}')".format(self.__number_name)

    def __str__(self) -> str:
        """Return the string representation of the object (the English name for the value)."""
        #self.str_nam
        return self.__str_name


    def __int__(self) -> int:
        """Return the value as a Python integer."""
        return self.__int_value

    def __float__(self) -> float:
        """Return the value as a Python float."""

    @staticmethod
    def from_int(i: int) -> 'IntWords':
        """Given an integer, create a new IntWords object that corresponds. This should support any positive
        or negative integer whose absolute value is less than a quadrillion, so numbers in the trillions should work.

        :param i: an integer value
        :return: a IntWords object.
        >>> print(IntWords.from_int(211000005))
        two hundred eleven million five
        """

        def once(num):
            global one
            word = ''
            word = one[int(num)]
            word = word.strip()
            return word

        def ten(num):
            global tenp
            global tenp2
            word = ''
            if num[0] == '1':
                word = tenp[int(num[1])]
            else:
                text = once(num[1])
                word = tenp2[int(num[0])]
                word = word + " " + text
            word = word.strip()
            return word

        def hundred(num):
            global one
            word = ''
            text = ten(num[1:])
            word = one[int(num[0])]
            if num[0] != '0':
                word = word + " Hundred "
            word = word + text
            word = word.strip()
            return word

        def thousand(num):
            word = ''
            pref = ''
            text = ''
            length = len(num)
            if length == 6:
                text = hundred(num[3:])
                pref = hundred(num[:3])
            if length == 5:
                text = hundred(num[2:])
                pref = ten(num[:2])
            if length == 4:
                text = hundred(num[1:])
                word = one[int(num[0])]
            if num[0] != '0' or num[1] != '0' or num[2] != '0':
                word = word + " Thousand "
            word = word + text
            if length == 6 or length == 5:
                word = pref + word
            word = word.strip()
            return word

        def million(num):
            word = ''
            pref = ''
            text = ''
            length = len(num)
            if length == 9:
                text = thousand(num[3:])
                pref = hundred(num[:3])
            if length == 8:
                text = thousand(num[2:])
                pref = ten(num[:2])
            if length == 7:
                text = thousand(num[1:])
                word = one[int(num[0])]
            if num[0] != '0' or num[1] != '0' or num[2] != '0':
                word = word + " Million "
            word = word + text
            if length == 9 or length == 8:
                word = pref + word
            word = word.strip()
            return word

        def billion(num):
            word = ''
            pref = ''
            text = ''
            length = len(num)
            if length == 12:
                text = million(num[3:])
                pref = hundred(num[:3])
            if length == 11:
                text = million(num[2:])
                pref = ten(num[:2])
            if length == 10:
                text = million(num[1:])
                word = one[int(num[0])]
            if num[0] != '0':
                word = word + " Billion "
            word = word + text
            if length == 12 or length == 11:
                word = pref + word
            word = word.strip()
            return word

        negative_flag = 0
        a = str(i)
        if '-' in a:
            negative_flag = 1
            a = a.replace('-', '')
            a.strip()
            # print(a)
        # a = '-123'

        leng = len(a)

        if leng == 1:
            if a == '0':
                num = 'Zero'
            else:
                num = once(a)
        if leng == 2:
            num = ten(a)
        if leng == 3:
            num = hundred(a)
        if leng > 3 and leng < 7:
            num = thousand(a)
        if leng > 6 and leng < 10:
            num = million(a)
        if leng > 9 and leng < 13:
            num = billion(a)
        if negative_flag == 1:
            num = 'negative ' + num
        num = num.lower()
        # print(num)
        # return str(num)
        return IntWords(num)
        # (IntWords)num
        # print(type(num))
        # num1 = IntWords(num)

    def __eq__(self, other) -> bool:
        """Determine if two IntWords objects are equivalent. Implements the == operator.

        >>> IntWords('two hundred, forty five') == IntWords('two hundred forty five')
        True
        >>> IntWords('three') == IntWords('negative five')
        False
        """
        if int(self) == int(other):
            return True
        else:
            return False

    def __le__(self, other) -> bool:

        if int(self) <= int(other):
            return True
        else:
            return False

    def __lt__(self, other) -> bool:
        if int(self) < int(other):
            return True
        else:
            return False

    def __add__(self, other: 'IntWords') -> 'IntWords':
        """Implement the + operator.

        >>> x = IntWords('two hundred, forty five') + IntWords('three hundred twelve')
        >>> print(x)
        five hundred fifty seven
        >>> int(x)
        557
        """
        return IntWords.from_int(int(self) + int(other))

    def __sub__(self, other: 'IntWords') -> 'IntWords':
        """Implement the - operator.

        >>> x = IntWords('two hundred, forty five') - IntWords('three hundred twelve')
        >>> print(x)
        negative sixty seven
        """
        return IntWords.from_int(int(self) - int(other))

    def __mul__(self, other):
        return IntWords.from_int(int(self) * int(other))


    def __floordiv__(self, other: 'IntWords') -> 'IntWords':

        return IntWords.from_int(int(self) // int(other))


    def __hash__(self):
        return hash(id(self))



if __name__ == '__main__':
    #x = IntWords('two hundred, forty five') + IntWords('three hundred twelve')
    #print(x)
    print('This program will construct and display a range of large numbers, ' +
          'compute their sum and mean (floored integer), ' +
          'and display all values as English words, not digits.\n')

    ints = range(-20000000, +50000000, 3234123)
    # build list using a list comprehension:
    numbers = [IntWords.from_int(x) for x in ints]

    print(numbers)

    print('The numbers are:\n')


    total = IntWords.from_int(0)  # accumulate the total here
    for iw in numbers:
        print(iw)
        total += iw
    print()

    print('The sum is:', total)

    mean = total // IntWords.from_int(len(ints))
    print('the mean is:', mean)

    a = IntWords('Forty Two')
    b = IntWords('Seven')
    print(a + b)
