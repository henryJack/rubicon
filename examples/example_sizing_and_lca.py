from physical_objects.motors.concept_motor import ConceptMotorAssembly
from physical_objects.motors.concept_motor import ElectricMachineBom
from sizing.motor_sizing_tool import MotorSizingTool
from lca.EM_production_environmental_impact import get_pei_matrix



mst: MotorSizingTool = MotorSizingTool()
bom: ElectricMachineBom = mst.get_electric_machine_bom()
get_pei_matrix(bom)
