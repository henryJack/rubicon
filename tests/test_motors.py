import unittest
from physical_objects.motors.concept_motor import ConceptMotorAssembly, ConceptRotor, ConceptStator


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test_rotor = ConceptRotor("test rotor", 0.1, 0.03, 0.1)
        self.assertIsInstance(test_rotor, ConceptRotor)

if __name__ == '__main__':
    unittest.main()
