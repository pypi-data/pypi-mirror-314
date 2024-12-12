import unittest
from reactive.observer.Watch import Watch
from reactive.observable import Reactive, Computed

class TestWatch(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('Watch test start')
    
    @classmethod
    def tearDownClass(self):
        print('Watch test end')

    def setUp(self):
        self.R1 = Reactive({"first_name": "John", "last_name": "Doe", "age": 20})
        # this flag is used to check if the watch effect is triggered
        self.effect1_exeuted = False
        def watchLambda1():
            self.R1.name
            self.R1.age
            # effect is triggered and flag to be true
            self.effect1_exeuted = True
        self.W1 = Watch(watchLambda1)
        self.effect1_exeuted = False

        self.full_name = Computed(lambda: self.R1.first_name + " " + self.R1.last_name)
        self.effect2_exeuted = False
        def watchLambda2():
            self.full_name.value
            self.effect2_exeuted = True
        self.W2 = Watch(watchLambda2)
        self.effect2_exeuted = False

        

    def tearDown(self):
        self.R1 = None
        self.W1.stop()
        self.W1 = None
        self.effect1_exeuted = False

        self.full_name = None
        self.W2.stop()
        self.W2 = None
        self.effect2_exeuted = False
    
    def test_name(self):
        self.R1.first_name = "Mike"
        self.R1.last_name = "Smith"
        # watch effect should be triggered for reactive and computed
        # and flag is true means the watch effect is triggered
        self.assertTrue(self.effect1_exeuted)
        self.assertTrue(self.effect2_exeuted)

        self.effect1_exeuted = False
        self.effect2_exeuted = False
        self.W1.stop()
        self.W2.stop()
        self.R1.first_name = "Jane"
        self.R1.last_name = "Doe"
        # watch stoped, watch effect should not be triggered
        # and flag is false means the watch effect is not triggered
        self.assertFalse(self.effect1_exeuted)
        self.assertFalse(self.effect2_exeuted)

    def test_age(self):
        self.R1.age = 25
        # age changed, the watch of reactive should be triggered
        self.assertTrue(self.effect1_exeuted)
        # age changed, the watch of computed name should not be triggered
        self.assertFalse(self.effect2_exeuted)

        self.effect1_exeuted = False
        self.effect2_exeuted = False
        self.W1.stop()
        self.W2.stop()
        self.R1.age = 45
        # watch stoped, the watch effect should not be triggered
        self.assertFalse(self.effect1_exeuted)
        self.assertFalse(self.effect2_exeuted)










    

