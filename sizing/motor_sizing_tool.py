import numpy as np
import math
from physical_objects.motors.concept_motor import ConceptMotorAssembly, ConceptRotor, ConceptStator


class MotorSizingTool:
    """
    A MotorSizingTool will calculate the size of an electric motor based on some inputs

    :param ElectricalMotorAssembly electrical_motor_assembly: motor assembly which will be sized
    :param float average_shear_stress: similar to k-factor, a permissible benchmarking parameter
    :param float maximum_rotor_speed: max rotor speed calculated from torque speed curve
    :param float max_torque: Calculated from torque speed curve
    :param float base_speed: Calculated from torque speed curve - speed at which you reach maximum power
    """

    """ In the following, the EV requirements results from Jack's tool can be imported as the main design requirements of the EV E-Motor"""
    def __init__(self,
                 electrical_motor_assembly: ConceptMotorAssembly,
                 average_shear_stress: float = 80.0,
                 maximum_rotor_speed: float = 12000.0,
                 max_torque: float = 200.0,
                 base_speed: float = 3000.0,
                 airgap_flux_density=1.0):

        self.electrical_motor_assembly = electrical_motor_assembly
        self.average_shear_stress = average_shear_stress
        self.maximum_rotor_speed = maximum_rotor_speed
        self.max_torque = max_torque
        self.airgap_flux_density = airgap_flux_density
        self.base_speed = base_speed
        self.tip_speed_error_flag = False
        self.shear_stress_out_of_range = False
        self.stacking_limit_exceeded_flag = False

    def calc_rot_dimensions(self):
        """ The rotor volume computation using the reported equation in the confluence page.
        Note that, the dl.ratio is an inout in the main file at line 31 and it ranges from 0.5 to 2, as reported in the paper, attached on the confluence page or as Leon reported in his report"""

        volume = self.max_torque / self.average_shear_stress / 2.0 / 1000.0
        self.electrical_motor_assembly.rotor.outer_diameter = \
            np.power((volume * 4.0 / math.pi * self.electrical_motor_assembly.rotor.dl_ratio), 1.0 / 3.0)

        self.electrical_motor_assembly.rotor.stack_length = \
            self.electrical_motor_assembly.rotor.outer_diameter / self.electrical_motor_assembly.rotor.dl_ratio

    def calc_tip_speed(self):
        ''' Calculates rotor tip speed, compares value to maximum for silicon iron and
        returns error if tip speed is exceded'''

        tip_speed = self.electrical_motor_assembly.rotor.outer_diameter * \
                    self.maximum_rotor_speed * math.pi / 60.0
        if tip_speed >= 110:
            self.tip_speed_error_flag = True
        else:
            self.tip_speed_error_flag = False

    def calc_stacking_limit(self):

        # if the stack length is above 300 mm two separate stacks will be required
        if self.electrical_motor_assembly.rotor.stack_length > 0.3:
            self.stacking_limit_exceeded_flag = True
        else:
            self.stacking_limit_exceeded_flag = False

    def calc_split_ratio_from_curve(self):
        # the stator ID should be linked to the rotor OD; figure out if this can be done using a link object
        self.electrical_motor_assembly.stator.inner_diameter = \
            self.electrical_motor_assembly.rotor.outer_diameter
        self.electrical_motor_assembly.stator.stack_length = self.electrical_motor_assembly.rotor.stack_length

        # Curve fits split ratio from benchmark data
        if self.average_shear_stress > 120 or self.average_shear_stress < 40:
            self.shear_stress_out_of_range = True
        else:
            self.shear_stress_out_of_range = False

        stator_split_ratio = -0.0018 * self.average_shear_stress + 0.8062
        self.electrical_motor_assembly.stator.split_ratio = stator_split_ratio

        inner_diameter = self.electrical_motor_assembly.stator.inner_diameter
        outer_diameter = inner_diameter / stator_split_ratio
        self.electrical_motor_assembly.stator.outer_diameter = outer_diameter

        """ In the previous piece of code, for more details of the used Benchmark equation, or linear assumption, please follow the confluence page"""

    # def calc_rotor_inner_diameter(self):
    #
    #     '''some parameters must be assumed to be able to size the rotor inner dimensions
    #     assumed maximum iron flux density of 1.8, and airgap length of 1mm NdfeB Magnets and 4 pole rotor.
    #     This function computes the permanent magnet thickness for surface mounted permanent magnet E-Machine, which is out of scope of our study/project
    #
    #     In my opinion, it is better to size the shaft instead of sizing this special SMPM E_machine geometry (TODO)   Done !!!
    #     '''
    #     maximum_iron_flux_density = 1.8
    #     mur = 1.05
    #     airgap_diameter = 0.001
    #     remanance_flux_density = 1.2
    #     poles = 4
    #
    #     magnet_thickness=mur*airgap_diameter/(remanance_flux_density/self.airgap_flux_density-1)
    #
    #     back_iron_thickness = self.airgap_flux_density/maximum_iron_flux_density * \
    #                           math.pi*self.electrical_motor_assembly.rotor.outer_diameter / (4*poles)
    #
    #     inner_diameter = self.electrical_motor_assembly.rotor.outer_diameter - \
    #                      2*(magnet_thickness + back_iron_thickness)
    #
    #     self.electrical_motor_assembly.rotor.inner_diameter = inner_diameter


    def calc_rotor_inner_diameter(self):

        ''' this function computes the shaft diameter '''

        Power =  self.base_speed * np.pi /30 * self.max_torque
        print("power ", Power/1000)

        inner_diameter = np.power((1330*Power/self.base_speed), 1.0 / 3.0)/1000

        self.electrical_motor_assembly.rotor.inner_diameter = inner_diameter


    def add_end_winding_length(self):
        self.electrical_motor_assembly.stator.end_winding_length = 0.03


    def material_size_wieght_cal(self):

        PM_case = 1
        mass_density_copper = 8933
        mass_density_M235_25A = 7650
        mass_density_Mild_steel = 7800
        mass_density_N42UH = 7500

        # stator side

        Dso = self.electrical_motor_assembly.stator.outer_diameter
        Dsi = self.electrical_motor_assembly.stator.inner_diameter
        Dro = Dsi
        Dri = self.electrical_motor_assembly.rotor.inner_diameter
        Lstk =self.electrical_motor_assembly.rotor.stack_length
        d = 0.88
        """ from the benchmark data and MotorCAD EV examples, d is ranging from 0.86 to .9, where d = 0.86 for IM, d = 0.88 for IPM and d = 0.9 for PMaSynRel E-machines"""
        stator_cylinder_vol = np.pi/4 * (Dso**2 - Dsi**2) * Lstk
        stator_yoke_vol = np.pi/4 * (Dso**2 - (d*Dso)**2) * Lstk
        stator_teeth_slots_vol = stator_cylinder_vol - stator_yoke_vol
        stator_teeth_vol = stator_teeth_slots_vol * 0.5
        stator_slots_vol = stator_teeth_vol
        stator_core_lamination_vol = stator_teeth_vol + stator_yoke_vol
        copper_winding_vol = stator_slots_vol * (1 + (1/Lstk) * (Lstk + 0.03*2))

        stator_core_weight = stator_core_lamination_vol * mass_density_M235_25A
        stator_copper_weight = copper_winding_vol * mass_density_copper

        # rotor side

        rotor_cylinder_vol = np.pi/4 * (Dsi**2 - Dri**2) * Lstk
        PM_vol = 0.2 * rotor_cylinder_vol
        Cage_vol = 0.5 * rotor_cylinder_vol
        shaft_vol = np.pi/4 * (Dri**2) * (Lstk*2)     # please refer to Benchmark data or MotorCAD templates for EV motors
        shaft_weight = shaft_vol * mass_density_Mild_steel
        """For these figures, please refer to MotorCAD Templates for EV applications"""
        if PM_case == 1:
            rotor_lamination_vol = rotor_cylinder_vol - PM_vol
            rotor_core_weight = rotor_lamination_vol * mass_density_M235_25A
            PM_weight = PM_vol * mass_density_N42UH
            E_machine_active_component_weight = shaft_weight + rotor_core_weight + PM_weight + stator_core_weight + stator_copper_weight

        else:
            rotor_lamination_vol = rotor_cylinder_vol - Cage_vol
            rotor_core_weight = rotor_lamination_vol * mass_density_M235_25A
            Cage_weight = Cage_vol * mass_density_copper
            E_machine_active_component_weight = shaft_weight + rotor_core_weight + Cage_weight + stator_core_weight + stator_copper_weight


    def size_motor(self):
        # size rotor
        MotorSizingTool.calc_rot_dimensions(self)
        MotorSizingTool.calc_tip_speed(self)
        MotorSizingTool.calc_stacking_limit(self)
        # size stator
        MotorSizingTool.calc_split_ratio_from_curve(self)
        MotorSizingTool.calc_rotor_inner_diameter(self)
