import unittest
from reactive.observable.Reactive import Reactive
from reactive.observer.Watch import Watch
from reactive.observer.WatchAttr import WatchAttr

class TestWatchAttr(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("WatchAttr test start")
    
    @classmethod
    def tearDownClass(self):
        print("WatchAttr test end")

    def setUp(self):
        self.R1 = Reactive({"name": "John", "age": 20})
        self.R2 = Reactive({"name": "Steven", "age": 22})
        self.R3 = Reactive({"name": "Alan", "age": 27})
        self.R4 = Reactive({"name": "Max", "age": 32})
        # this flag is used to check if the watch effect is triggered
        self.effect1_exeuted = False
        def watchLambda1():
            print("R1 name:", self.R1.name, "R1 age:", self.R1.age)
            print("R2 name:", self.R2.name, "R2 age:", self.R2.age)
            # effect is triggered and flag to be true
            self.effect1_exeuted = True
        self.WA1 = WatchAttr(attributes = [self.R3, self.R4], effect = watchLambda1)
        # init the flag to false for further check
        self.effect1_exeuted = False

        self.effect2_exeuted = False
        def watchLambda2():
            print("R3 name:", self.R3.name, "R3 age:", self.R3.age)
            print("R4 name:", self.R4.name, "R4 age:", self.R4.age)
            self.effect2_exeuted = True
        self.WA2 = WatchAttr(attributes = [self.R3, self.R4], effect = watchLambda2)
        self.effect2_exeuted = False

    def tearDown(self):
        self.R1 = None
        self.R2 = None
        self.WA1.stop()
        self.WA1 = None
        self.effect1_exeuted = False

        self.R3 = None
        self.R4 = None
        self.WA2.stop()
        self.WA2 = None
        self.effect2_exeuted = False
    
    def test_name(self):
        self.R1.name = "Mike"
        # no R1 watched, so effect1 and effect2 should not be triggered
        self.assertFalse(self.effect1_exeuted)
        self.assertFalse(self.effect2_exeuted)

        self.effect1_exeuted = False
        self.effect2_exeuted = False
        self.WA1.stop()
        self.WA2.stop()
        # stop the watch, so effect1 and effect2 should not be triggered
        self.R1.name = "Jane"
        self.R4.name = "Zeka"
        self.assertEqual(self.effect1_exeuted, False)
        self.assertEqual(self.effect2_exeuted, False)

    def test_age(self):
        self.R2.age = 25
        self.R4.age = 30
        # R2 and R4 are watched, so effect1 and effect2 should be triggered
        self.assertTrue(self.effect1_exeuted)
        self.assertTrue(self.effect2_exeuted)

        self.effect1_exeuted = False
        self.effect2_exeuted = False
        self.WA1.stop()
        self.WA2.stop()
        # stop the watch, so effect1 and effect2 should not be triggered
        self.R2.age = 45
        self.R3.age = 60
        self.assertEqual(self.effect1_exeuted, False)
        self.assertEqual(self.effect2_exeuted, False)