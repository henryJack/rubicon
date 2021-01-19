from physical_objects.motors.concept_motor import ConceptMotorAssembly, ConceptRotor, ConceptStator
from physical_objects.motors.concept_motor import ElectricMachineBom
from sizing.motor_sizing_tool import MotorSizingTool
from lca.EM_production_environmental_impact import get_pei_matrix

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


mst: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=x_motor_assembly,   # you can type x_motor_assembly, PmaSynRel_motor_assembly ,IM_motor_assembly, or IPM_motor_assembly
                                       average_shear_stress=80.0,                    # set the shear stress for your motor topology, please, read more details in the confluence page or in the motor_sizing_tool script
                                       maximum_rotor_speed=12000.0,                  # motor maximum speed
                                       max_torque=200.0,                             # motor maximum torque
                                       base_speed=3000.0,                            # motor base speed
                                       motor_type="x-motor"                          # you can type x-motor, IPM, IM, PMaSynREL
                                       )
mst.size_motor()

bom: ElectricMachineBom = mst.get_electric_machine_bom()


get_pei_matrix(bom)