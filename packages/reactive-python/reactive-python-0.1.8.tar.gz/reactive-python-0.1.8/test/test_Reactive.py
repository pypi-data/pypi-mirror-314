import unittest
from reactive import Reactive
class TestReactive(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("reactive test start")
    
    @classmethod
    def tearDownClass(self):
        print("reactive test end")

    def setUp(self):
        self.reactiveImpl1 = Reactive({"name": "John", "age": 20})
        self.reactiveImpl2 = Reactive({"address": "1234 lower residence road,Kelowna"})

    def tearDown(self):
        self.reactiveImpl1 = None
        self.reactiveImpl2 = None

    def test_getter(self):
        self.assertEqual(self.reactiveImpl1.age, 20)
        self.assertEqual(self.reactiveImpl1.name, "John")
        self.assertEqual(self.reactiveImpl2.address, "1234 lower residence road,Kelowna")
        # not exist property should return None
        self.assertIsNone(self.reactiveImpl2.age)

    def test_setter(self):
        self.reactiveImpl1.name = "Yolo"
        self.assertEqual(self.reactiveImpl1.name, "Yolo")
        self.assertIsNone(self.reactiveImpl1.address)
        self.reactiveImpl1.age = 21
        self.assertEqual(self.reactiveImpl1.age, 21)
        self.reactiveImpl1.address = "1 upper residence road,Kelowna"
        self.assertEqual(self.reactiveImpl1.address, "1 upper residence road,Kelowna")
