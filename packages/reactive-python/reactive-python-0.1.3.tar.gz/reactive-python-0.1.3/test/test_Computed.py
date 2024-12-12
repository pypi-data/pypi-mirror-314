import unittest
from reactive import Computed, Reactive
class TestComputed(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("computed test start")
    
    @classmethod
    def tearDownClass(self):
        print("computed test end")

    def setUp(self):
        self.reactiveImpl1 = Reactive({"first_name": "John", "save_in_bank1": 20})
        self.reactiveImpl2 = Reactive({"last_name": "Bell", "save_in_bank2": 40})
        self.computedImpl1 = Computed(lambda: self.reactiveImpl1.first_name + " " + self.reactiveImpl2.last_name)
        self.computedImpl2 = Computed(lambda: self.reactiveImpl1.save_in_bank1 + self.reactiveImpl2.save_in_bank2)

    def tearDown(self):
        self.reactiveImpl1 = None
        self.reactiveImpl2 = None
        self.computedImpl1 = None
        self.computedImpl2 = None

    def test_getter(self):
        self.assertIsNone(self.computedImpl1.parent)
        self.assertIsNone(self.computedImpl2.address)
         # should be reactiveImpl1.first_name + " " + reactiveImpl2.last_name
        self.assertEqual(self.computedImpl1.value, "John Bell")
         # should be reactiveImpl1.save_in_bank1 + reactiveImpl2.save_in_bank2
        self.assertEqual(self.computedImpl2.value, 60)
    
    def test_setter(self):
        self.reactiveImpl1.first_name = "Yolo"
        self.assertEqual(self.reactiveImpl1.first_name, "Yolo")
        # reactiveImpl1.first_name + " " + reactiveImpl2.last_name should be recalculated automatically
        self.assertEqual(self.computedImpl1.value, "Yolo Bell")
        self.reactiveImpl2.save_in_bank2 = 21
        self.assertEqual(self.reactiveImpl2.save_in_bank2, 21)
        # reactiveImpl1.save_in_bank1 + reactiveImpl2.save_in_bank2 should be recalculated automatically
        self.assertEqual(self.computedImpl2.value, 41)
