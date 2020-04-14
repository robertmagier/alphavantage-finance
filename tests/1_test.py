import sys
import unittest
import os.path as path
# sys.path.append('../lib')

sys.path.append(path.join(sys.path[0],'..','lib'))
import prepareData as prep

class TestPrepareData(unittest.TestCase):

    def test_calculateHighBase(self):
        row = {
            'y_open':10,
            'y_close':1.1
        }
        max = prep.calculateHighBase(row)
        self.assertEqual(max, 10)

    def test_calculateLowBase(self):
        row = {
            'y_open':10,
            'y_close':1.1
        }
        min = prep.calculateLowBase(row)
        self.assertEqual(min, 1.1)

    def test_calculateLowError(self):
        row = {
            'y_low':12,
            'y_open':10,
            'y_close':1.1
        }
        lerr = prep.calculateLowError(row)
        self.assertEqual(lerr, 10.9)

    def test_calculateHighError(self):
        row = {
            'y_high':20,
            'y_open':11,
            'y_close':1.1
        }
        herr = prep.calculateHighError(row)
        self.assertEqual(herr, 9)

    def test_calculateDiff(self):
        row = {
            'y_open':11,
            'y_close':13
        }
        diff = prep.calculateDiff(row)
        self.assertEqual(diff, 2)

    def test_generateLegend(self):
        row = {
            'time':'Time Series (5min).2020-04-09 14:50:00.1. open',
        }
        output = prep.generateLegend(row)
        expected = "2020-04-09\n14:50"
        self.assertEqual(output,expected)

    def test_calculateColor(self):
        row = {
            'y_open':11,
            'y_close':13
        }
        color = prep.calculateColor(row)
        self.assertEqual(color, 'green')
        row = {
            'y_open':13.1,
            'y_close':13
        }
        color = prep.calculateColor(row)
        self.assertEqual(color, 'red')



if __name__ == '__main__':
    unittest.main()