from typing import List
import math


# class MotorBom:
#     def __init__(self, paint, plastic, insulation resin, insulation material, copper, aluminium, steel, laminated_steel):
#         self.insulation = insulation
#         self.copper = copper
#


# (1, 5, "hat", 4) # list
# {"key1": 1, "key2": 4} # dictionary

class ConceptRotor:
    """
        Section defining geometry of a electrical rotor object.

        :param float stack_length: length of the rotor core
        :param float inner_diameter: Inner diameter of the rotor
        :param float outer_diameter: Outer diameter of the rotor
        :param float dl_ratio: Diameter-length ratio of the rotor
        :param float outer_diameter: Outer diameter of the rotor
        :param float mass: mass of rotor, is calculated if density is specified, or can be set by user
        """

    def __init__(self, name: str,
                 stack_length: float = 0.1,
                 inner_diameter: float = 0.03,
                 outer_diameter: float = 0.1,
                 shaft_diameter: float = 0.025,     # has been added to highlight the difference between the inner rotor diameter and the shaft diameter. This is useful for the X-motor rotor parameters definition.
                 mass: float = None):
        self.name = name
        self.stack_length = stack_length
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.mass = mass
        self.dl_ratio = self.outer_diameter / self.stack_length
        self.shaft_diameter = shaft_diameter

    def get_rotor_volume(self):
        return (self.outer_diameter ** 2 - self.inner_diameter ** 2) * self.stack_length * math.pi / 4

    def set_dl_ratio_length(self, dl_ratio: float, stack_length: float):
        self.dl_ratio = dl_ratio
        self.stack_length = stack_length
        self.outer_diameter = dl_ratio * stack_length

    def set_dl_ratio_diameter(self, dl_ratio: float, outer_diameter: float):
        self.dl_ratio = dl_ratio
        self.outer_diameter = outer_diameter
        self.stack_length = outer_diameter / dl_ratio

        """ (TODO) , please, correct the mistake found on the previous function, as the second line is not correct, and the thirs line as well. 
        It should computes the stack length instead of the outer diameter. You can note that the outer diameter is one of the inputs to this function     DOne!!!
        """

    def set_rotor_mass_with_density(self, density=7650.0):

        """ We can change the mass density of the E-machine core material here in that line """

        volume = self.get_rotor_volume()
        self.mass = volume * density

    def set_rotor_mass(self, mass: float):
        self.mass = mass


class ConceptStator:
    """
        Section defining geometry of a electrical stator object.

        :param float stack_length: length of the stator
        :param float inner_diameter: Inner diameter of the stator
        :param float outer_diameter: Outer diameter of the stator
        :param float split_ratio: inner-outer ratio of the stator
        """

    def __init__(self, name: str, stack_length: float = 0.1, inner_diameter: float = 0.1, outer_diameter: float = 0.2):
        self.stack_length = stack_length
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.split_ratio = inner_diameter / outer_diameter
        self.end_winding_length = 0.03

    def set_split_ratio_inner(self, split_ratio: float, inner_diameter: float):
        self.split_ratio = split_ratio
        self.inner_diameter = inner_diameter
        self.outer_diameter = inner_diameter / split_ratio

    def set_split_ratio_outer(self, split_ratio: float, outer_diameter: float):
        self.split_ratio = split_ratio
        self.outer_diameter = outer_diameter
        self.inner_diameter = outer_diameter * split_ratio

    def calc_stator_volume(self):
        return (self.outer_diameter ** 2 - self.inner_diameter ** 2) * self.stack_length * math.pi / 4


class ConceptMotorAssembly:
    def __init__(self, name, rotor: ConceptRotor, stator: ConceptStator):
        self.name = name
        self.rotor: ConceptRotor = rotor
        self.stator: ConceptStator = stator

