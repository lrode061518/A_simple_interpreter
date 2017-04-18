import unittest
from main import *

test_cases = [
        ('1+2+3+4', 10 ),
        ('1 + 2 + 3 + 4', 10 ),
        ('2-4', -2 ),
        ('3*3', 9),
        ('9/3', 3),
        ('38+3*5-20', 33),
        ('3 * 4 + 6 / 2', 15)
        ]

class testCalc( unittest.TestCase ):

    def test_some_case(self):
        for case in test_cases:
            result = Interpreter( case[0] ).go()
            self.assertEqual( result, case[1] )





if __name__ == '__main__':
	unittest.main()
