from physical_objects.motors.concept_motor import ConceptMotorAssembly, ConceptRotor, ConceptStator
from physical_objects.motors.concept_motor import ElectricMachineBom
from sizing.motor_sizing_tool import MotorSizingTool
from lca.EM_production_environmental_impact import get_pei_matrix
import numpy as np

def get_concept_motor(dl_ratio) -> ConceptMotorAssembly:
    """Create Rotor & Stator"""
    rotor = ConceptRotor(name='ipmrotor', inner_diameter=0.03, outer_diameter=0.05, stack_length=0.1)
    stator = ConceptStator(name='ipmstator', inner_diameter=rotor.outer_diameter, outer_diameter=0.1, stack_length=0.1)

    """Set DL Ratio"""
    rotor.dl_ratio = dl_ratio

    """Add Rotor and Stator to Motor"""
    initial_motor_assembly: ConceptMotorAssembly = ConceptMotorAssembly(name='IPM', rotor=rotor, stator=stator)

    return initial_motor_assembly


x_motor_assembly = get_concept_motor(1/1.23)              # the inout is the dl_ratios, please, read the comment below
PmaSynRel_motor_assembly = get_concept_motor(0.5)
IM_motor_assembly = get_concept_motor(0.5)
IPM_motor_assembly = get_concept_motor(0.5)

""" typical dl_ratios for radial flux E-machines = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]  and o.5 has been set based on Benchmark data 
# for X-motor is ~ (1/1.23 = 0.813), please, refer to the confluence page for more details."""

# Min power High torque case


print(F"========================================================")
print(F"Min power High torque case")
print(F"========================================================")

# x-motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=x_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=70.0,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=59.4,                             # motor maximum torque
                                       base_speed=1976,                            # motor base speed
                                       motor_type="x-motor"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))



# IPM motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=IPM_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=80.0,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=59.4,                             # motor maximum torque
                                       base_speed=1976,                            # motor base speed
                                       motor_type="IPM"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))


# IM motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=IM_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=70.0,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=59.4,                             # motor maximum torque
                                       base_speed=1976,                            # motor base speed
                                       motor_type="IM"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))


# PmaSynRel motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=PmaSynRel_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=80,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=59.4,                             # motor maximum torque
                                       base_speed=1976,                            # motor base speed
                                       motor_type="PMaSynREL"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))



print(F"========================================================")
print(F"# Min Torque High power case")
print(F"========================================================")

# Min Torque High power case

# x-motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=x_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=70.0,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=46.4,                             # motor maximum torque
                                       base_speed=3279,                            # motor base speed
                                       motor_type="x-motor"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))


# IPM motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=IPM_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=80.0,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=46.4,                             # motor maximum torque
                                       base_speed=3279,                            # motor base speed
                                       motor_type="IPM"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))

# IM motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=IM_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=70.0,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=46.4,                             # motor maximum torque
                                       base_speed=3279,                            # motor base speed
                                       motor_type="IM"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))

# PmaSynRel motor
mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=PmaSynRel_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=80,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=7235,                  # motor maximum speed
                                       max_torque=46.4,                             # motor maximum torque
                                       base_speed=3279,                            # motor base speed
                                       motor_type="PMaSynREL"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
print("PEI Array--> ", np.transpose(get_pei_matrix(bom)))

""" PEI ~ production Environmental impact"""
""" Investigating Edison project different machines compared together """

# estimating the housing of the Edison motor prototype
D_housing_x = 0.230
L_housing_x = 0.425
Dso_x = 0.180
mass_density_Aluminum_alloy = 2790
Housing_vol = np.pi/4 * (D_housing_x**2 - Dso_x**2) * L_housing_x
Housing_weight = Housing_vol * mass_density_Aluminum_alloy


# End caps

DS_end_cap_thickness = 12 / 1000
DS_end_cap_outer_dia = 340 / 1000
DS_end_cap_inner_dia = 180 / 1000

NDS_end_cap_thickness = 30 / 1000
NDS_end_cap_outer_dia = 230 / 1000
NDS_end_cap_inner_dia = 80 / 1000


DS_end_cap_volume = np.pi/4 * (DS_end_cap_outer_dia**2 - DS_end_cap_inner_dia**2) * DS_end_cap_thickness
NDS_end_cap_volume = np.pi/4 * (NDS_end_cap_outer_dia**2 - NDS_end_cap_inner_dia**2) * NDS_end_cap_thickness

DS_end_cap_weight = DS_end_cap_volume * mass_density_Aluminum_alloy
NDS_end_cap_weight = NDS_end_cap_volume * mass_density_Aluminum_alloy

Aluminum_x = DS_end_cap_weight + NDS_end_cap_weight + Housing_weight

# emb = ElectricMachineBom("name", self.electrical_steel, self.other_steel, self.aluminium, self.copper, self.ndfeb, self.ferrite)

BOM_JLR = ElectricMachineBom(name="JLR Machine",
                                electrical_steel=19.392,
                                other_steel=2.872,
                                aluminum=Aluminum_x,
                                copper=4.742,
                                ndfeb=1.491,
                                ferrite=0)

print("PEI Array--> ", np.transpose(get_pei_matrix(BOM_JLR)))


BOM_two_stacks_x_motor = ElectricMachineBom(name="two_stacks_x_motor_concept Machine",
                                electrical_steel=17,
                                other_steel=4.5,
                                aluminum=Aluminum_x,
                                copper=4.742,
                                ndfeb=0,
                                ferrite=4.8)

print("PEI Array--> ", np.transpose(get_pei_matrix(BOM_two_stacks_x_motor)))


BOM_three_stacks_x_motor = ElectricMachineBom(name="three_stacks_x_motor_concept Machine",
                                electrical_steel=17.0531,
                                other_steel=5.4418,
                                aluminum=Aluminum_x,
                                copper=3.4672,
                                ndfeb=0,
                                ferrite=5.3877)

print("PEI Array--> ", np.transpose(get_pei_matrix(BOM_three_stacks_x_motor)))


BOM_three_stacks_x_motor_prototype = ElectricMachineBom(name="three_stacks_x_motor_prototype Machine",
                                electrical_steel=22.8552,
                                other_steel=7.7465,
                                aluminum=Aluminum_x,
                                copper=5.7366,
                                ndfeb=0,
                                ferrite=5.2161)

print("PEI Array--> ", np.transpose(get_pei_matrix(BOM_three_stacks_x_motor_prototype)))

BOM_PMaSynRel = ElectricMachineBom(name="PMaSynRel Machine",
                                electrical_steel=24.2196,
                                other_steel=2.5488,
                                aluminum=Aluminum_x,
                                copper=4.9891,
                                ndfeb=0,
                                ferrite=3.9689)

print("PEI Array--> ", np.transpose(get_pei_matrix(BOM_PMaSynRel)))