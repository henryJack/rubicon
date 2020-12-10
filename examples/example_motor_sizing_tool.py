from sizing.motor_sizing_tool import MotorSizingTool
from physical_objects.motors.concept_motor import ConceptMotorAssembly, ConceptRotor, ConceptStator
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def get_concept_motor(dl_ratio) -> ConceptMotorAssembly:
    """Create Rotor & Stator"""
    rotor = ConceptRotor(name='ipmrotor', inner_diameter=0.03, outer_diameter=0.05, stack_length=0.1)
    stator = ConceptStator(name='ipmstator', inner_diameter=rotor.outer_diameter, outer_diameter=0.1, stack_length=0.1)

    """Set DL Ratio"""
    rotor.dl_ratio = dl_ratio

    """Add Rotor and Stator to Motor"""
    ipm_motor_assembly: ConceptMotorAssembly = ConceptMotorAssembly(name='IPM', rotor=rotor, stator=stator)

    return ipm_motor_assembly


def size_syn_rel_machine():
    pass

# def size_machine(dl_ratio, average_shear_stress, mrs, split_ratio):

# IPM, x-motor, PMaSynrel, Induction

def size_radial_machine():
    """Get Motor Assembly"""
    dl_ratio = 0.5  # typical dl_ratios = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    motor_assembly = get_concept_motor(dl_ratio=dl_ratio)

    """Initialise Sizing Tool & Size """
    sizing_tool: MotorSizingTool = MotorSizingTool(electrical_motor_assembly=motor_assembly,
                                                   average_shear_stress=80.0,
                                                   maximum_rotor_speed=12000.0,
                                                   max_torque=200.0,
                                                   base_speed=3000.0,
                                                   airgap_flux_density=1.0)

    """ Note: the shear stress can be changed according to the E-machine topology. Referring to IPM the shear stress is varied between 40 to 120 depends on the desired torque of the Machine, it can be estimated from the benchmark data directly.
    In addition, the shear stress in varied in lower range for PMaSynRel machine, as 30 to 50. Besides, It varies from 70 to 110 for the induction machine. Please, review the confluence page for more details. Done !!! """

    sizing_tool.size_motor()

    """Print common attributes"""
    rotor = motor_assembly.rotor
    stator = motor_assembly.stator

    rotor_volume = rotor.get_rotor_volume()
    stator_volume = stator.calc_stator_volume()

    print("rotor_volume ", rotor_volume)
    print("stator_volume ", stator_volume)

    plot_motor(motor_assembly)


def plot_motor(sized_motor: ConceptMotorAssembly):
    rotor = sized_motor.rotor
    stator = sized_motor.stator

    # calculate volumes

    rotor_volume = rotor.get_rotor_volume()
    stator_volume = stator.calc_stator_volume()

    # print results
    print("rotor.inner_diameter ", rotor.inner_diameter)
    print("rotor.outer_diameter ", rotor.outer_diameter)
    print("stator.outer_diameter ", stator.inner_diameter)
    print("stator.outer_diameter ", stator.outer_diameter)


    # plot motor 2D
    circle1 = plt.Circle((0, 0), rotor.inner_diameter, color='w')
    circle2 = plt.Circle((0, 0), rotor.outer_diameter, color='blue')
    circle3 = plt.Circle((0, 0), stator.outer_diameter, color='g')

    figure1, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
    # (or if you have an existing figure)
    # fig = plt.gcf()
    # ax = fig.gca()

    plt.xlim([0, 0.5])
    plt.ylim([0, 0.5])

    rectangle1 = patches.Rectangle((stator.outer_diameter + 0.1, 0), rotor.stack_length, rotor.inner_diameter,
                                   color='w')
    rectangle2 = patches.Rectangle((stator.outer_diameter + 0.1, 0), rotor.stack_length, rotor.outer_diameter,
                                   color='blue')
    rectangle3 = patches.Rectangle((stator.outer_diameter + 0.1, 0), rotor.stack_length, stator.outer_diameter,
                                   color='g')

    ax.add_artist(circle3)
    ax.add_artist(circle2)
    ax.add_artist(circle1)

    ax.add_patch(rectangle3)
    ax.add_patch(rectangle2)
    ax.add_patch(rectangle1)

    plt.title('Shear stress = 80, DLratio = 0.5')

    plt.show()


size_radial_machine()
