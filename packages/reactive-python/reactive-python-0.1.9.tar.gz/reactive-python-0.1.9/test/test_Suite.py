import unittest
from test_Reactive import TestReactive
from test_Computed import TestComputed
from test_Watch import TestWatch
from test_WatchAttr import TestWatchAttr


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()

    suite.addTest(TestReactive('test_getter'))
    suite.addTest(TestReactive('test_setter'))

    suite.addTest(TestComputed('test_getter'))
    suite.addTest(TestComputed('test_setter'))

    suite.addTest(TestWatch('test_name'))
    suite.addTest(TestWatch('test_age'))

    suite.addTest(TestWatchAttr('test_name'))
    suite.addTest(TestWatchAttr('test_age'))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))
    print(result)

my_suite()