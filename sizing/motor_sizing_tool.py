import numpy as np
import math
from physical_objects.motors.concept_motor import ConceptMotorAssembly, ElectricMachineBom

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
                 airgap_flux_density=1.0,
                 motor_type="x-motor"
                 ):
        self.motor_type = motor_type

        if self.motor_type == "x-motor":
            self.PM_case = True
            self.radial_case = False
        elif self.motor_type == "IPM" or motor_type == "PMaSynREL":
            self.PM_case = True
            self.radial_case = True
        elif self.motor_type == "IM":
            self.PM_case = False
            self.radial_case = True

        self.electrical_motor_assembly = electrical_motor_assembly
        self.average_shear_stress = average_shear_stress
        self.maximum_rotor_speed = maximum_rotor_speed
        self.max_torque = max_torque
        self.airgap_flux_density = airgap_flux_density
        self.base_speed = base_speed
        self.tip_speed_error_flag = False
        self.shear_stress_out_of_range = False
        self.stacking_limit_exceeded_flag = False
        self.electrical_steel = 0
        self.other_steel = 0
        self.copper = 0
        self.aluminium = 0
        self.ndfeb = 0
        self. ferrite = 0

    def calc_rot_dimensions(self):
        """ The rotor volume computation using the reported equation in the confluence page.
        Note that, the dl.ratio is an inout in the main file at line 31 and it ranges from 0.5 to 2,
        as reported in the paper, attached on the confluence page or as Leon reported in his report
        In addition, it can be set as (1/1.23 ~ 0.813) for X-motor, as a part of the aforementioned range """

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


    def calc_rotor_inner_diameter(self):

        """ This function for estimating the rotor inner diameter, which will not be the same as the shaft diameter in case of X-motor. Besides, this function computes the shaft diameter"""

        Power =  self.base_speed * np.pi /30 * self.max_torque
        print(F"")
        print(F"========================================================")
        print(F" {self.motor_type}")
        print(F"========================================================")
        print(F"power = {Power/1000} kW")
        # print("{}{}{}".format("power = ", Power/1000, " kw"))

        shaft_diameter = np.power((1330*Power/self.base_speed), 1.0 / 3.0)/1000

        self.electrical_motor_assembly.rotor.shaft_diameter = shaft_diameter

        if self.radial_case == True:
            self.electrical_motor_assembly.rotor.inner_diameter = shaft_diameter
        else:
            self.electrical_motor_assembly.rotor.inner_diameter = self.electrical_motor_assembly.rotor.outer_diameter * 0.44
            D_Bush_outer = self.electrical_motor_assembly.rotor.inner_diameter
            D_Bush_inner = shaft_diameter


    def add_end_winding_length(self):
        self.electrical_motor_assembly.stator.end_winding_length = 0.03


    def material_size_wieght_cal(self):

        mass_density_copper = 8933
        mass_density_M235_25A = 7650
        mass_density_Mild_steel = 7800
        mass_density_N42UH = 7500
        mass_density_Aluminum_alloy= 2790
        pole_piece_density = 7850   # got it from FREMAT tool
        magnet_density = 5000
        bolt_density = 7870
        kfill = 0.4

        # stator side

        Dso = self.electrical_motor_assembly.stator.outer_diameter
        Dsi = self.electrical_motor_assembly.stator.inner_diameter
        Dro = Dsi
        Dsh = self.electrical_motor_assembly.rotor.shaft_diameter
        Lstk = self.electrical_motor_assembly.rotor.stack_length
        Dri = self.electrical_motor_assembly.rotor.inner_diameter
        D_Bush_outer = Dri
        D_Bush_inner = Dsh

        d = 0.88    # ration between the slot end diameter to the outer stator diameter, please refer to more details in the following script lines.

        print(F"Dso = {Dso} m")
        print(F"Dsi = {Dsi} m")
        print(F"Dro = {Dro} m")

        if self.radial_case == True:
            print(F"Dri = Dsh =  {Dri} m")
        else:
            D_B_o = D_Bush_outer
            D_B_i = D_Bush_inner
            alpha_p = 0.8 # the pole arc to pole pitch ratio. This value has been chosen based on the Paper published by Prof Kias In IEEE transaction on magnetics, please, refer to this paper for more details.
            print(F"Dri =  {Dri} m")
            print(F"Dsh =  {Dsh} m")
            print(F"D_B_o = Dri =  {D_B_o} m")
            print(F"D_B_i = Dsh =   {D_B_i} m")

        print(F"Lstk =  {Lstk} m")
        print(F"Typically shear stress =  {self.average_shear_stress} Kpa")

        """ from the benchmark data and MotorCAD EV examples, d is ranging from 0.86 to .9, where d = 0.86 for IM, d = 0.88 for IPM and d = 0.9 for PMaSynRel E-machines"""
        # stator side

        stator_cylinder_vol = np.pi/4 * (Dso**2 - Dsi**2) * Lstk
        stator_yoke_vol = np.pi/4 * (Dso**2 - (d*Dso)**2) * Lstk
        stator_teeth_slots_vol = stator_cylinder_vol - stator_yoke_vol
        stator_teeth_vol = stator_teeth_slots_vol * 0.5
        stator_slots_vol = stator_teeth_vol
        stator_core_lamination_vol = stator_teeth_vol + stator_yoke_vol
        copper_winding_vol = stator_slots_vol * (1/Lstk) * (Lstk + 0.03*2) * kfill

        stator_core_weight = stator_core_lamination_vol * mass_density_M235_25A
        stator_copper_weight = copper_winding_vol * mass_density_copper

        # rotor side
        rotor_cylinder_vol = np.pi / 4 * (Dsi ** 2 - Dri ** 2) * Lstk

        if self.radial_case == True:
            PM_vol = 0.2 * rotor_cylinder_vol
            Cage_vol = 0.5 * rotor_cylinder_vol
            shaft_vol = np.pi / 4 * (Dri ** 2) * (Lstk * 2)  # please refer to Benchmark data or MotorCAD templates for EV
            shaft_weight = shaft_vol * mass_density_Mild_steel
            """For these figures, please refer to MotorCAD Templates for EV applications"""
            if self.PM_case == True:
                rotor_lamination_vol = rotor_cylinder_vol - PM_vol
                rotor_core_weight = rotor_lamination_vol * mass_density_M235_25A
                PM_weight = PM_vol * mass_density_N42UH
                E_machine_active_component_weight = shaft_weight + rotor_core_weight + PM_weight + stator_core_weight + stator_copper_weight

            else:
                rotor_lamination_vol = rotor_cylinder_vol - Cage_vol
                rotor_core_weight = rotor_lamination_vol * mass_density_M235_25A
                Cage_weight = Cage_vol * mass_density_copper
                E_machine_active_component_weight = shaft_weight + rotor_core_weight + Cage_weight + stator_core_weight + stator_copper_weight

        else:
            LaPM = 0.012
            L_end_ring = 0.005
            Dbo = 0.012      # please refer to the Edison motor prototype data
            pole_pieces_vol = rotor_cylinder_vol * alpha_p
            circumferential_PM_vol = rotor_cylinder_vol * (1-alpha_p)
            axial_PM_vol = rotor_cylinder_vol/Lstk * LaPM
            Bush_vol = np.pi / 4 * (Dri ** 2 - Dsh ** 2) * Lstk
            shaft_vol = np.pi / 4 * (Dsh ** 2) * (Lstk * 2)
            Bolt_vol = np.pi / 4 * (Dbo ** 2) * (Lstk * 2)
            end_ring_vol = rotor_cylinder_vol/Lstk * L_end_ring * 2

            pole_pieces_weight = pole_pieces_vol * pole_piece_density
            circumferential_PM_weight = magnet_density * circumferential_PM_vol
            axial_PM_weight = axial_PM_vol * magnet_density
            PM_weight = circumferential_PM_weight + axial_PM_weight
            Bush_weight = Bush_vol * mass_density_Mild_steel
            bolt_weight = Bolt_vol * bolt_density
            end_ring_weight = end_ring_vol * pole_piece_density
            shaft_weight = shaft_vol * mass_density_Mild_steel
            E_machine_active_component_weight = shaft_weight + pole_pieces_weight + PM_weight + Bush_weight + bolt_weight + end_ring_weight + stator_core_weight + stator_copper_weight

        # Housing

        D_housing = Dso + 0.035      # this value has been achieved from Benchmark data and from MotorCAD templates for EV motors
        L_housing = Lstk * 2 - 0.01*2  # 10 mm has been assumed for front and end plate of the motor housing
        Housing_vol = np.pi/4 * (D_housing**2 - Dso**2) * L_housing
        Housing_weight = Housing_vol * mass_density_Aluminum_alloy

        # End caps

        end_cap_thickness = 5 / 1000
        Front_end_cap_volume = np.pi/4 * (D_housing**2 - Dri**2) * end_cap_thickness
        Front_end_cap_weight = Front_end_cap_volume * mass_density_Aluminum_alloy
        rear_end_cap_weight = Front_end_cap_weight
        total_end_caps_weight = Front_end_cap_weight + rear_end_cap_weight

        Aluminum = total_end_caps_weight + Housing_weight

        """ note: the bearing, wire insulation, slot liner, and winding impregnation have been ignored in these calculations"""

        total_motor_weight = E_machine_active_component_weight + Housing_weight + total_end_caps_weight

        # insulation, painting, and plastic materials

        winding_insulation_weight = 1/100 * stator_copper_weight    # please, refer to the sizing confluence page benchmark data
        Insulation_materials = winding_insulation_weight            # rename for BOM class
        impregnation_weight = 31.2/100 * stator_copper_weight       # please, refer to the sizing confluence page benchmark data
        Insulation_resins = impregnation_weight                     # rename for BOM class
        plastic_weight = 5/100 * stator_copper_weight               # please, refer to the Environmental impact paper
        Plastics = plastic_weight                                   # rename for BOM class

        Housing_paint_thickness = 1/1000
        end_caps_paint_thickness = 1/1000

        # painting_material_mass_density = 1600    # please refer to https://vodoprovod.blogspot.com/2017/12/convert-kg-paint-to-liters-online.html
        # Housing_paint_weight = np.pi/4 * ((D_housing+2*Housing_paint_thickness)**2 - D_housing**2) * L_housing * painting_material_mass_density
        # End_cap_paint_weight = np.pi/4 * (D_housing**2 - Dri**2) * end_caps_paint_thickness * 2 * 2   # I multiply by 2 for both front and rear end caps and then multiply again by 2 for considering both inner and outer surface of the caps

        total_paint_weight = 2/100 * Aluminum
        Paint = total_paint_weight                                  # rename for BOM class

        total_motor_weight = total_motor_weight + winding_insulation_weight + impregnation_weight + plastic_weight + total_paint_weight

        print(F"Housing_vol =  {Housing_vol} m3")
        print(F"stator_core_weight =  {stator_core_weight} kg")
        print(F"stator_copper_weight =  {stator_copper_weight} kg")
        print(F"shaft_weight = {shaft_weight} kg")
        print(F"winding_insulation_weight =  {winding_insulation_weight} kg")
        print(F"impregnation_weight =  {impregnation_weight} kg")
        print(F"plastic_weight =  {plastic_weight} kg")
        print(F"paint_weight =  {total_paint_weight} kg")


        if self.radial_case == True:
            if self.PM_case == True:
                print(F"PM_weight = {PM_weight} kg")
                print(F"rotor_core_weight = {rotor_core_weight} kg")
                Electrical_steel = stator_core_weight + rotor_core_weight
                Copper = stator_copper_weight
                Other_steel = shaft_weight
                NdFeB = PM_weight
                Ferrite = 0
            else:
                print(F"Cage_weight = {Cage_weight} kg")
                print(F"rotor_core_weight = {rotor_core_weight} kg")
                Electrical_steel = stator_core_weight + rotor_core_weight
                Copper = stator_copper_weight + Cage_weight
                Other_steel = shaft_weight
                NdFeB =0
                Ferrite = 0

        else:
            print(F"pole_pieces_weight = {pole_pieces_weight} kg")
            print(F"circumferential_PM_weight = {circumferential_PM_weight} kg")
            print(F"axial_PM_weight = {axial_PM_weight} kg")
            print(F"PM_weight = {PM_weight} kg")
            print(F"Bush_weight = {Bush_weight} kg")
            print(F"bolt_weight = {bolt_weight} kg")
            print(F"end_ring_weight = {end_ring_weight} kg")
            Electrical_steel = stator_core_weight + pole_pieces_weight + end_ring_weight
            Copper = stator_copper_weight
            Other_steel = shaft_weight + Bush_weight + bolt_weight
            Ferrite = PM_weight
            NdFeB =0


        print(F"E_machine_active_component_weight = {E_machine_active_component_weight} kg")
        print(F"Housing_weight = {Housing_weight} kg")
        print(F"total_end_caps_weight = {total_end_caps_weight} kg")
        print(F"total_motor_weight = {total_motor_weight} kg")

        """ In the following, the required parameters for the BOM Class has been printed with the same names used in the BOM class as shared by Radu"""
        print(F"")
        print(F"========================================================")
        print(F"Print BOM Variable= {self.motor_type}")
        print(F"========================================================")
        print(F"Electrical_steel = {Electrical_steel} kg")
        print(F"Other_steel = {Other_steel} kg")
        print(F"Aluminum = {Aluminum} kg")
        print(F"Copper = {Copper} kg")
        print(F"Insulation_materials = {Insulation_materials} kg")
        print(F"Insulation_resins = {Insulation_resins} kg")
        print(F"Paint = {Paint} kg")
        print(F"Plastics = {Plastics} kg")
        if self.radial_case == True:
            if self.PM_case == True:
                print(F"NdFeB = {NdFeB} kg")
            else:
                pass
        else:
            print(F"Ferrite = {Ferrite} kg")

        BOM_array = [Electrical_steel, Other_steel, Aluminum, Copper, Insulation_materials, Insulation_resins, Paint, Plastics]
        print(F"BOM_array = {BOM_array}")
        self.electrical_steel = Electrical_steel
        self.other_steel = Other_steel
        self.aluminium = Aluminum
        self.copper = Copper
        self.ndfeb = NdFeB
        self.ferrite = Ferrite

    def size_motor(self):
        # size rotor
        MotorSizingTool.calc_rot_dimensions(self)
        MotorSizingTool.calc_tip_speed(self)
        MotorSizingTool.calc_stacking_limit(self)
        # size stator
        MotorSizingTool.calc_split_ratio_from_curve(self)
        MotorSizingTool.calc_rotor_inner_diameter(self)
        # weight calculation
        MotorSizingTool.material_size_wieght_cal(self)

    def get_electric_machine_bom(self):
        emb = ElectricMachineBom("name", self.electrical_steel, self.other_steel, self.aluminium, self.copper,self.ndfeb,self.ferrite)
        return emb




