"""
This module defines various test materials and cross sections.
The cross sections are identified by a unique number and all created by the
`get_wing_cross_section_geometry_definition_dict` function. This function returns a dict of the
cross section ids and the cross section geometry definitions. 
The cross section are grouped in series:

| Serie | Description                                              |
|-------|----------------------------------------------------------|
| 100   | Alu                                                      |
| 200   | Laminate 1                                               |
| 300   | Variation of fiber angle with Laminate 1                 |
| 400   | Variation of element size                                |
| 500   | Compare of shear center in origin or not                 |
| 600   | Variation of fiber angle with Laminate 3                 |
| 700   | Laminate 3                                               |
| 900   | For the paper                                            |
| 1000  | CAS, Variation of fiber angle with Laminate Shell        |
| 1100  | For validation of the material orientation               |
| 1200  |                                                          |
| 1300  | CAS, Variation of fiber angle with Laminate 3, 10° steps |
| 1400  | Validation rectangle from the Jung paper                 |

 The cross sections are described in the table below:

| Number | Geometry                                 | Material                                          | Comment                                    |
|--------|------------------------------------------|---------------------------------------------------|--------------------------------------------|
| 100    | Rectangle                                | Alu 2 mm                                          |                                            |
| 101    | Rectangle, web 1                         | Alu 2 mm                                          |                                            |
| 102    | Rectangle, web 2                         | Alu 2 mm                                          |                                            |
| 103    | Rectangle, web 2+3                       | Alu 2 mm                                          |                                            |
| 104    | NACA 0012, web 4                         | Alu 2 mm                                          |                                            |
| 105    | NACA 2412, web 4                         | Alu 2 mm                                          |                                            |
| 106    | NACA 2412, web 1+2                       | Alu 2 mm                                          |                                            |
| 107    | Rectangle centered, web x=0              | Alu 2 mm                                          |                                            |
| 108    | Rectangle centered                       | Alu 2 mm                                          |                                            |
| 109    | Rectangle centered, web x=-0.2           | Alu 2 mm                                          |                                            |
| 110    | Rectangle centered, web x=0              | Alu 2 mm                                          | = 107                                      |
| 111    | Rectangle centered, web x=-0.2 and x=0.2 | Alu 2 mm                                          |                                            |
| 200    | Rectangle                                | Laminate 1                                        |                                            |
| 201    | Rectangle, web 1                         | Laminate 1                                        |                                            |
| 202    | Rectangle, web 2                         | Laminate 1                                        |                                            |
| 203    | Rectangle, web 2+3                       | Laminate 1                                        |                                            |
| 204    | NACA 0012, web 4                         | Laminate 1                                        |                                            |
| 205    | NACA 2412, web 4                         | Laminate 1                                        |                                            |
| 206    | NACA 2412, web 1+2                       | Laminate 1                                        |                                            |
| 210    | Rectangle                                | Laminate 1 in CAS with 30°                        |                                            |
| 211    | Rectangle                                | Laminate 1 in CUS with 30°                        |                                            |
| 220    | NACA 2412, web 1+2                       | Laminate 1, web 2 Laminate 2                      | First web thicker                          |
| 221    | NACA 2412, web 1+2                       | Laminate 1, web 1 Laminate 2                      | Second web thicker                         |
| 222    | NACA 2412, web 1+2                       | Laminate 1, D-nose Laminate 2                     | D-nose                                     |
| 300    | Rectangle centered                       | CAS, Variation of fiber angle with Laminate 1     | 5° steps                                   |
| 400    | Rectangle                                | Laminate 1                                        | Variation of element size                  |
| 500    | Rectangle centered                       | Laminate 3                                        |                                            |
| 501    | Rectangle                                | Laminate 3                                        |                                            |
| 600    | Rectangle centered                       | CAS, Variation of fiber angle with Laminate 3     | 5° steps                                   |
| 700    | Rectangle                                | Laminate 3                                        |                                            |
| 701    | Rectangle, web 1                         | Laminate 3                                        |                                            |
| 702    | Rectangle, web 2                         | Laminate 3                                        |                                            |
| 703    | Rectangle, web 2+3                       | Laminate 3                                        |                                            |
| 704    | NACA 0012, web 4                         | Laminate 3                                        |                                            |
| 705    | NACA 2412, web 4                         | Laminate 3                                        |                                            |
| 706    | NACA 2412, web 1+2                       | Laminate 3                                        |                                            |
| 710    | Rectangle                                | Laminate 3 in CAS with 30°                        |                                            |
| 711    | Rectangle                                | Laminate 3 in CUS with 30°                        |                                            |
| 712    | Rectangle                                | Laminate 3 in CAS with 45°                        |                                            |
| 900    | Rectangle centered                       | Alu 2 mm                                          |                                            |
| 901    | Rectangle centered                       | Laminate Shell                                    |                                            |
| 902    | Rectangle centered                       | Laminate Shell in CAS with 30°                    |                                            |
| 903    | Rectangle centered                       | Laminate Shell in CUS with 30°                    |                                            |
| 910    | NACA 2412, web 1+2                       | Alu 2 mm                                          |                                            |
| 911    | NACA 2412, web 1+2                       | Laminate Shell, web Laminate Web                  |                                            |
| 1000   | Rectangle centered                       | CAS, Variation of fiber angle with Laminate Shell | 5° steps                                   |
| 1100   | Rectangle centered                       | Laminate Test                                     | For validation of the material orientation |
| 1200   | Rectangle centered                       | Alu 2 mm                                          | = 900                                      |
| 1201   | Rectangle centered                       | Laminate 3                                        | = 500                                      |
| 1202   | Rectangle centered                       | Laminate 3 in CAS with 30°                        |                                            |
| 1203   | Rectangle centered                       | Laminate 3 in CUS with 30°                        |                                            |
| 1210   | NACA 2412, web 1+2                       | Alu 2 mm                                          |                                            |
| 1211   | NACA 2412, web 1+2                       | Laminate 3                                        |                                            |
| 1300   | Rectangle centered                       | CAS, Variation of fiber angle with Laminate 3     | 10° steps                                  |
| 1400   | Rectangle Jung paper centered            | Laminate 7 15°                                    |                                            |
| 1401   | Rectangle Jung paper centered            | Laminate 7                                        |                                            |
| 1402   | Rectangle Jung paper midsurface centered | Laminate 7 15°                                    |                                            |
| 1403   | Rectangle Jung paper midsurface centered | Laminate 7                                        |                                            |

The laminates are:

| Laminate       | Description                                  |
|----------------|----------------------------------------------|
| Laminate 1     | Standard 0/45/90 Laminate                    |
| Laminate 2     | Like Laminate 1, but double number of layers |
| Laminate 3     | One layer with thickness of Laminate 1       |
| Laminate Shell | Standard 0/45/90 Laminate                    |
| Laminate Web   | 0/45 Laminate                                |
| Laminate Test  | 0/90/45                                      |
| Laminate 7     | Laminate in Jung Paper, 6 layers             |

The web positions are:

| Web   | Position |
|-------|----------|
| web 1 | x=0.5    |
| web 2 | x=0.3    |
| web 3 | x=0.7    |
| web 4 | x=0.4    |

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

import numpy as np

from PreDoCS.CrossSectionAnalysis.CrossSectionGeometry import load_profile_points, \
    WingCrossSectionGeometryDefinition
from PreDoCS.MaterialAnalysis.CLT import Ply
from PreDoCS.MaterialAnalysis.Materials import Transverse_Isotropic, Isotropic, Orthotropic
from PreDoCS.MaterialAnalysis.Shells import IsotropicShell, CompositeShell
from PreDoCS.util.vector import Vector


######### Ply data #########


def get_test_ply_data():
    p1 = Transverse_Isotropic(
        134.7e9, 7.7e9, 0.369, 0.5, 4.2e9, name='Hexcel T800/M21', density=1590,
    )
    p1_thickness = 0.184e-3
    return p1, p1_thickness


def get_ply7_data():
    E1 = 128e9
    E2 = 11.3e9
    G12 = G13 = 6e9
    G23 = 3.6e9
    nu12 = 0.3

    G21 = G12
    nu22 = E2 / (2 * G23) - 1

    p7 = Transverse_Isotropic(
        E1, E2, nu12, nu22, G21, name='AS4/3501-6', density=1500, 
    )
    p7_thickness = 0.127e-3
    return p7, p7_thickness


######### Laminate data #########


def get_laminate_1_layup(ply, ply_thickness, orientation):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
    ]


def get_laminate_2_layup(ply, ply_thickness, orientation):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
    ]


def get_laminate_3_layup(ply, ply_thickness, orientation):
    return [(ply, ply_thickness, orientation)]


def get_laminate_7_layup(ply, ply_thickness, orientation):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
    ]


def get_shell_layup(ply, ply_thickness, orientation):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
    ]


def get_web_layup(ply, ply_thickness, orientation=0.):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
    ]


def get_shell2_layup(ply, ply_thickness, orientation):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
    ]


def get_web2_layup(ply, ply_thickness, orientation=0.):
    return [
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
    ]


def get_cap_layup(ply, ply_thickness=0.125, orientation=0.):
    return [
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
    ]


######### Cross section generation #########


def get_fiber_angle_variation_geometry_dict(start_id, num_geometries, angle_increment, profile_file, layup_function):
    """
    Get geometry dict for a given cross section with a variation of the fiber orientation.
    """
    res = {}
    for i in range(num_geometries):
        angle = angle_increment * i
        res[start_id + i] = WingCrossSectionGeometryDefinition(
            load_profile_points(profile_file, False),
            CompositeShell(
                name='Material {}°'.format(angle),
                layup=layup_function(angle),
            )
        )
    return res


def get_circle_points(num_points):
    """ Returns points of a circular profile. """
    angles = np.array(range(num_points)) / num_points * 2 * np.pi
    return [(np.cos(a), np.sin(a)) for a in angles]


def get_wing_cross_section_geometry_definition_dict(profiles_path):
    """
    This function returns a dict of the cross section ids and the cross section geometry definitions.
    See module description for cross section description.
    

    Parameters
    ----------
    profiles_path: str
        Path to the profiles files.

    Returns
    -------
    dict(float, WingCrossSectionGeometryDefinition)
        The geometry definition dict.
    """
    alu_density = 2820
    alu_E = 71e9
    alu_nu = 0.32

    alu_material = Isotropic(alu_E, alu_nu, name='Alu', density=alu_density)
    alu = IsotropicShell(alu_material, 2e-3, name='Alu 2mm')
    alu_shell = IsotropicShell(alu_material, 4.416e-3, name='Alu 4.416mm')
    alu_shell2 = IsotropicShell(alu_material, 1.84e-3, name='Alu 1.84mm')

    i1 = IsotropicShell(alu_material, 5e-3, name='Alu 5mm')
    i2 = IsotropicShell(alu_material, 15e-3, name='Alu 15mm')
    i3 = IsotropicShell(alu_material, 10e-3, name='Alu 10mm')

    p1, p1_thickness = get_test_ply_data()

    p7, p7_thickness = get_ply7_data()

    l1 = CompositeShell(name='Laminat 1', layup=get_laminate_1_layup(p1, p1_thickness, 0.0))
    l1_pos_angle = CompositeShell(name='Laminat 1 +30°', layup=get_laminate_1_layup(p1, p1_thickness, 30))
    l1_neg_angle = CompositeShell(name='Laminat 1 -30°', layup=get_laminate_1_layup(p1, p1_thickness, -30))

    l2 = CompositeShell(name='Laminat 2', layup=get_laminate_2_layup(p1, p1_thickness, 0.0))

    p3 = p1
    p3_thickness = 12 * p1_thickness

    l3 = CompositeShell(name='Laminat 3', layup=get_laminate_3_layup(p3, p3_thickness, 0.0))
    l3_pos_angle = CompositeShell(name='Laminat 3 +30°', layup=get_laminate_3_layup(p3, p3_thickness, 30))
    l3_pos_angle_45 = CompositeShell(name='Laminat 3 +45°', layup=get_laminate_3_layup(p3, p3_thickness, 45))
    l3_neg_angle = CompositeShell(name='Laminat 3 -30°', layup=get_laminate_3_layup(p3, p3_thickness, -30))
    l3_thick = CompositeShell(name='Laminat 3 dick', layup=get_laminate_3_layup(p3, 10 * p3_thickness, 0.0))

    l7_15 = CompositeShell(name='Laminat 7 +15° from the beam axis°',
                              layup=get_laminate_7_layup(p7, p7_thickness, 15))

    l7 = CompositeShell(name='Laminat 7 0° from the beam axis°', layup=get_laminate_7_layup(p7, p7_thickness, 0))

    l_shell = CompositeShell(name='Laminat Shell', layup=get_shell_layup(p1, p1_thickness, 0.0))
    l_shell_pos_angle = CompositeShell(name='Laminat Shell +30°', layup=get_shell_layup(p1, p1_thickness, 30))
    l_shell_neg_angle = CompositeShell(name='Laminat Shell -30°', layup=get_shell_layup(p1, p1_thickness, -30))
    l_web = CompositeShell(name='Laminat Web', layup=get_web_layup(p1, p1_thickness, 0))

    l_shell2 = CompositeShell(name='Laminat Shell 2', layup=get_shell2_layup(p1, p1_thickness, 0.0))
    l_shell_pos_angle2 = CompositeShell(name='Laminat Shell 2 +30°', layup=get_shell2_layup(p1, p1_thickness, 30))
    l_shell_neg_angle2 = CompositeShell(name='Laminat Shell 2 -30°', layup=get_shell2_layup(p1, p1_thickness, -30))
    l_web2 = CompositeShell(name='Laminat Web2 ', layup=get_web2_layup(p1, p1_thickness, 0))


    p_chandra = Orthotropic(
        E_11=142e9,
        E_22=9.81e9,
        E_33=9.81e9,
        nu_12=0.3,
        nu_23=0.42,
        nu_13=0.3,
        G_12=6e9,
        G_23=3.77e9,
        G_13=6e9,
        name='Hercules AS4/3501-6',
        density=1578,
    )
    p_chandra_thickness = 0.127e-3
    l_chandra_pn = CompositeShell(
        name='Chandra Web pn',
        layup=[
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, -45.0),
        ],
    )
    l_chandra_np = CompositeShell(
        name='Chandra Web np',
        layup=[
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, 45.0),
        ],
    )
    l_chandra_n = CompositeShell(
        name='Chandra top',
        layup=[
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
        ],
    )
    l_chandra_p = CompositeShell(
        name='Chandra bottom',
        layup=[
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
        ],
    )

    l_chandra4_pn = CompositeShell(
        name='Chandra4 Web pn',
        layup=[
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, 45.0),
        ],
    )
    l_chandra4_np = CompositeShell(
        name='Chandra4 Web np',
        layup=[
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, -45.0),
        ],
    )
    l_chandra4_n = CompositeShell(
        name='Chandra4 top',
        layup=[
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
            (p_chandra, p_chandra_thickness, -45.0),
        ],
    )
    l_chandra4_p = CompositeShell(
        name='Chandra4 bottom',
        layup=[
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
            (p_chandra, p_chandra_thickness, 45.0),
        ],
    )

    # Real world materials
    biax_c = Orthotropic(
        E_11=51771470588,
        E_22=51771470588,
        E_33=7999647761,
        nu_12=0.039,
        nu_23=0.36,
        nu_13=0.36,
        G_12=2986259597,
        G_23=2812065934,
        G_13=2812065934,
        name='CCC 452',
        density=1413,
    )
    biax_g = Orthotropic(
        E_11=20808300613,
        E_22=20808300613,
        E_33=8530135940,
        nu_12=0.11,
        nu_23=0.32,
        nu_13=0.32,
        G_12=2888480615,
        G_23=2949605137,
        G_13=2949605137,
        name='CS-ITG 92125',
        density=1778,
    )
    ud_c = Orthotropic(
        E_11=98209621553,
        E_22=8788508647,
        E_33=8788508647,
        nu_12=0.26,
        nu_23=0.34,
        nu_13=0.26,
        G_12=3610994108,
        G_23=3117150410,
        G_13=3610994108,
        name='UD-Fabric CU300',
        density=1481,
    )
    foam = Orthotropic(
        E_11=75000000,
        E_22=75000000,
        E_33=75000000,
        nu_12=0.4,
        nu_23=0.4,
        nu_13=0.4,
        G_12=24000000,
        G_23=24000000,
        G_13=24000000,
        name='Rohacell 51',
        density=51,
    )

    l_real_shell = CompositeShell(name='Laminat Real Shell', layup=[
        (biax_c, 0.25e-3, 45),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (biax_c, 0.25e-3, 45),
        (biax_c, 0.25e-3, 45),
    ])
    l_real_web = CompositeShell(name='Laminat Real Web', layup=[
        (biax_g, 0.25e-3, 45),
        (biax_g, 0.25e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (foam, 1e-3, 0),
        (biax_g, 0.25e-3, 0),
        (biax_g, 0.25e-3, 45),
    ])
    l_real_cap = CompositeShell(name='Laminat Real Spar Cap', layup=[
        (biax_c, 0.25e-3, 45),
        (ud_c, 1e-3, 0),
        (ud_c, 1e-3, 0),
        (ud_c, 1e-3, 0),
        (ud_c, 1e-3, 0),
        (ud_c, 1e-3, 0),
        (ud_c, 1e-3, 0),
        (biax_c, 0.25e-3, 45),
        (biax_c, 0.25e-3, 45),
    ])


    #     p4 = p1
    #     p4_thickness = 0.05
    #     l4 = CompositeShell(name='Laminat 4', [(p4, p4_thickness, 90))])
    #     alu4 = IsotropicMaterial('Alu 50mm', p4_thickness, alu_density, alu_E, alu_nu)
    #
    #     p5 = p1
    #     p5_thickness = 0.1
    #     l5 = CompositeShell(name='Laminat 5', [(p5, p5_thickness, 90))])
    #     alu5 = IsotropicMaterial('Alu 100mm', p5_thickness, alu_density, alu_E, alu_nu)
    #
    #     p6 = p1
    #     p6_thickness = 0.15
    #     l6 = CompositeShell(name='Laminat 6', [(p6, p6_thickness, 90))])
    #     alu6 = IsotropicMaterial('Alu 150mm', p6_thickness, alu_density, alu_E, alu_nu)

    # From BECAS Manual
    iso1 = CompositeShell(name='Iso. #1', layup=[(Orthotropic(
        100, 100, 0.2, 0.2, 0.2, 41.667, 41.667, 41.667, 1, name='Iso. #1 Ply', density=100), 0.01, 0)]
                             )
    ortho1_pos = CompositeShell(name='Ortho. #1', layup=[(Orthotropic(
        120, 120, 0.19, 0.19, 0.26, 60, 60, 50, 1, name='Ortho. #1 Ply', density=480), 0.00999, 45)]
                                   )
    ortho1_neg = CompositeShell(name='Ortho. #1', layup=[(Orthotropic(
        120, 120, 0.19, 0.19, 0.26, 60, 60, 50, 1, name='Ortho. #1 Ply', density=480), 0.00999, 135)]
                                   )

    web_line_1 = (Vector([0.5, -1]), Vector([0.5, 1]))
    web_line_2 = (Vector([0.3, -1]), Vector([0.3, 1]))
    web_line_3 = (Vector([0.7, -1]), Vector([0.7, 1]))
    web_line_4 = (Vector([0.4, -1]), Vector([0.4, 1]))
    web_line_5 = (Vector([0, -1]), Vector([0, 1]))
    web_line_6 = (Vector([-2, 0]), Vector([2, 0]))

    airfoil_spline = {
        'DegMin': 3,
        'DegMax': 15,
        'Continuity': 4,  # = GeomAbs_C2
        'Tol3D': 1.0e-4,
    }

    profile_geometry_dict = {}

    # For the paper new
    element_size_paper = 0.01
    position_blurring = 1e-6
    profile_geometry_dict[0] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), alu_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), alu_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), alu_shell),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), alu_shell),
        ],
        element_size=element_size_paper,
    )
    profile_geometry_dict[1] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell),
        ],
        element_size=element_size_paper,
    )
    # CAS
    profile_geometry_dict[2] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_pos_angle),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_pos_angle),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_pos_angle),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_pos_angle),
        ],
        element_size=element_size_paper,
    )
    # CUS
    profile_geometry_dict[3] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_pos_angle),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_pos_angle),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_neg_angle),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_neg_angle),
        ],
        element_size=element_size_paper,
    )

    profile_geometry_dict[10] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu_shell,
        webs=[(web_line_2, alu_shell), (web_line_1, alu_shell)],
        element_size=element_size_paper,
        te_cutoff_x=0.98,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
    )
    profile_geometry_dict[11] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_shell,
        webs=[(web_line_2, l_web), (web_line_1, l_web)],
        element_size=element_size_paper,
        te_cutoff_x=0.98,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
    )

    profile_geometry_dict[20] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), alu_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), alu_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), alu_shell),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), alu_shell),
        ],
        element_size=1,
    )
    profile_geometry_dict[21] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell),
        ],
        element_size=1,
    )
    # CAS
    profile_geometry_dict[22] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_pos_angle),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_pos_angle),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_pos_angle),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_pos_angle),
        ],
        element_size=1,
    )
    # CUS
    profile_geometry_dict[23] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_neg_angle),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_neg_angle),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_pos_angle),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_neg_angle),
        ],
        element_size=1,
    )

    profile_geometry_dict[30] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu_shell2,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), alu_shell2),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), alu_shell2),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), alu_shell2),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), alu_shell2),
        ],
        element_size=element_size_paper,
    )
    profile_geometry_dict[31] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell2,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell2),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell2),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell2),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell2),
        ],
        element_size=element_size_paper,
    )
    # CAS
    profile_geometry_dict[32] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle2,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_pos_angle2),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_pos_angle2),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_pos_angle2),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_pos_angle2),
        ],
        element_size=element_size_paper,
    )
    # CUS
    profile_geometry_dict[33] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle2,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_pos_angle2),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_pos_angle2),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_neg_angle2),
            ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_neg_angle2),
        ],
        element_size=element_size_paper,
    )

    profile_geometry_dict[40] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu_shell2,
        webs=[(web_line_2, alu_shell2), (web_line_1, alu_shell2)],
        element_size=element_size_paper,
        te_cutoff_x=0.98,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
    )
    profile_geometry_dict[41] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_shell2,
        webs=[(web_line_2, l_web2), (web_line_1, l_web2)],
        element_size=element_size_paper,
        te_cutoff_x=0.98,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
    )

    # Load application point tests
    profile_geometry_dict[90] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), alu, element_size=0.01)
    profile_geometry_dict[91] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu, element_size=0.01)

    # Chandra validation
    profile_geometry_dict[95] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
        l_chandra_pn,
        material_regions=[
            ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
            ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_np),
            ((Vector([-0.0121, -0.0068]), Vector([0.0121 - position_blurring, -0.0068])), l_chandra_p),
        ],
        element_size=0.001,
    )
    profile_geometry_dict[96] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
        l_chandra_pn,
        material_regions=[
            ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
            ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_np),
            ((Vector([-0.0121, -0.0068]), Vector([0.0121 - position_blurring, -0.0068])), l_chandra_n),
        ],
        element_size=0.001,
    )
    profile_geometry_dict[97] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
        l_chandra_p,
        material_regions=[
            ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra_pn),
            ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
            ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_np),
            # ((Vector([0.011338, -0.006038]), Vector([0.011338, 0.006038])), l_chandra_pn),
            # ((Vector([-0.011338, 0.006038]), Vector([0.011338, 0.006038])), l_chandra_n),
            # ((Vector([-0.011338, 0.006038]), Vector([-0.011338, -0.006038])), l_chandra_np),
        ],
        element_size=0.001,
        profile_thickness_direction='outside',
    )
    # profile_geometry_dict[97] = WingCrossSectionGeometryDefinition(
    #     load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
    #     l_chandra_n,
    #     material_regions=[
    #         ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra_pn),
    #         ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_p),
    #         ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_np),
    #     ],
    #     element_size=0.001,
    # )
    # profile_geometry_dict[97] = WingCrossSectionGeometryDefinition(
    #     load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
    #     l_chandra_np,
    #     material_regions=[
    #         ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
    #         ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_pn),
    #         ((Vector([-0.0121, -0.0068]), Vector([0.0121 - position_blurring, -0.0068])), l_chandra_p),
    #     ],
    #     element_size=0.001,
    # )
    profile_geometry_dict[98] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
        l_chandra_np,
        material_regions=[
            ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
            ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_pn),
            ((Vector([-0.0121, -0.0068]), Vector([0.0121 - position_blurring, -0.0068])), l_chandra_n),
        ],
        element_size=0.001,
    )
    profile_geometry_dict[99] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
        l_chandra4_n,
        material_regions=[
            ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra4_np),
            ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra4_p),
            ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra4_pn),
        ],
        element_size=0.001,
    )
    # profile_geometry_dict[992] = WingCrossSectionGeometryDefinition(
    #     load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
    #     l_chandra4_p,
    #     material_regions=[
    #         ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra4_np),
    #         ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra4_n),
    #         ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra4_pn),
    #     ],
    #     element_size=0.005,
    # )
    # profile_geometry_dict[993] = WingCrossSectionGeometryDefinition(
    #     load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
    #     l_chandra4_p,
    #     material_regions=[
    #         ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra4_np),
    #         ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra4_n),
    #         ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra4_pn),
    #     ],
    #     element_size=0.01,
    # )
    profile_geometry_dict[994] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
        l_chandra_p,
        material_regions=[
            ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra_np),
            ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
            ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_pn),
        ],
        element_size=0.0068,
    )
    profile_geometry_dict[995] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),
        l_chandra_p,
        material_regions=[
            ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra_np),
            ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
            ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_pn),
        ],
        element_size=0.1,
    )

    sc_997 = 15.17e-3#0#14.16e-3#0#15.17e-3
    profile_geometry_dict[997] = WingCrossSectionGeometryDefinition(
        # Shear center to origin
        [Vector([p.x, p.y - sc_997]) for p in load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4_gap.txt'), False)],
        l_chandra_p,
        material_regions=[
            ((Vector([0.0121, -0.0068 - sc_997]), Vector([0.0121, 0.0068 - sc_997])), l_chandra_pn),
            ((Vector([-0.0121, 0.0068 - sc_997]), Vector([0.0121, 0.0068 - sc_997])), l_chandra_n),
            ((Vector([-0.0121, 0.0068 - sc_997]), Vector([-0.0121, -0.0068 - sc_997])), l_chandra_np),
        ],
        element_size=0.001,#np.sqrt(2)*6*0.127*1e-3,#0.001,
        profile_thickness_direction='outside',
        close_open_ends=False,
    )
    # profile_geometry_dict[97] = WingCrossSectionGeometryDefinition(
    #     load_profile_points(os.path.join(profiles_path, 'chandra_symmetric4.txt'), False),#chandra_symmetric4_inside
    #     l_chandra_p,
    #     material_regions=[
    #         ((Vector([0.0121, -0.0068]), Vector([0.0121, 0.0068])), l_chandra_pn),
    #         ((Vector([-0.0121, 0.0068]), Vector([0.0121, 0.0068])), l_chandra_n),
    #         ((Vector([-0.0121, 0.0068]), Vector([-0.0121, -0.0068])), l_chandra_np),
    #         # ((Vector([0.011338, -0.006038]), Vector([0.011338, 0.006038])), l_chandra_pn),
    #         # ((Vector([-0.011338, 0.006038]), Vector([0.011338, 0.006038])), l_chandra_n),
    #         # ((Vector([-0.011338, 0.006038]), Vector([-0.011338, -0.006038])), l_chandra_np),
    #     ],
    #     element_size=0.001,
    #     profile_thickness_direction='outside',
    # )
    # Profiles with isotropic material
    profile_geometry_dict[100] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), alu)
    profile_geometry_dict[101] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), alu,
        webs=[(web_line_1, alu)])
    profile_geometry_dict[102] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), alu,
        webs=[(web_line_2, alu)])
    profile_geometry_dict[103] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), alu,
        webs=[(web_line_2, alu), (web_line_3, alu)])
    profile_geometry_dict[104] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-0012-cos-50.txt'), True), alu,
        webs=[(web_line_4, alu)])
    profile_geometry_dict[105] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu,
        webs=[(web_line_4, alu)])
    profile_geometry_dict[106] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu,
        webs=[(web_line_2, alu), (web_line_1, alu)])
    profile_geometry_dict[107] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu,
        webs=[((Vector([0, -1]), Vector([0, 1])), alu)])
    profile_geometry_dict[108] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu)
    profile_geometry_dict[109] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu,
        webs=[((Vector([-0.2, -1]), Vector([-0.2, 1])), alu)])
    profile_geometry_dict[110] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu,
        webs=[((Vector([0, -1]), Vector([0, 1])), alu)])
    profile_geometry_dict[111] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu,
        webs=[((Vector([-0.2, -1]), Vector([-0.2, 1])), alu),
              ((Vector([0.2, -1]), Vector([0.2, 1])), alu)])

    # Profiles with composite material
    profile_geometry_dict[200] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l1)
    profile_geometry_dict[201] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l1,
        webs=[(web_line_1, l1)])
    profile_geometry_dict[202] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l1,
        webs=[(web_line_2, l1)])
    profile_geometry_dict[203] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l1,
        webs=[(web_line_2, l1), (web_line_3, l1)])
    profile_geometry_dict[204] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-0012-cos-50.txt'), True), l1,
        webs=[(web_line_4, l1)])
    profile_geometry_dict[205] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l1,
        webs=[(web_line_4, l1)])
    profile_geometry_dict[206] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l1,
        webs=[(web_line_2, l1), (web_line_1, l1)])
    # CAS
    profile_geometry_dict[210] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l1_pos_angle)
    # CUS
    profile_geometry_dict[211] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l1_pos_angle,
        material_regions=[((Vector([1, 0.5]), Vector([0, 0.0])), l1_neg_angle)])
    # First web thicker
    profile_geometry_dict[220] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l1,
        webs=[(web_line_2, l2), (web_line_1, l1)])
    # Second web thicker
    profile_geometry_dict[221] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l1,
        webs=[(web_line_2, l2), (web_line_1, l2)])
    # D-nose
    profile_geometry_dict[222] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l1,
        webs=[(web_line_2, l2), (web_line_1, l1)],
        material_region_lines=[(web_line_2, l2)])  # bug in shellexpander

    # Variation of the fiber orientation (composite laminate)
    profile_geometry_dict.update(
        get_fiber_angle_variation_geometry_dict(300, 73, 5, os.path.join(profiles_path, 'rectangle_center.txt'),
                                               lambda angle: get_laminate_1_layup(p1, p1_thickness, angle)))

    # Variation of the element size
    for i in range(40):
        profile_geometry_dict[400 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'rectangle_center.txt'), False), l1,
            material_regions=[
                ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l1),
                ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l1),
                ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l1),
                ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l1),
            ],
            element_size=1 / (i + 1)
        )

    # Variation of the coordinate system
    profile_geometry_dict[500] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l3)
    profile_geometry_dict[501] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3)

    # Variation of the fiber orientation (UD-layer)
    profile_geometry_dict.update(
        get_fiber_angle_variation_geometry_dict(600, 73, 5, os.path.join(profiles_path, 'rectangle_center.txt'),
                                               lambda angle: get_laminate_3_layup(p3, p3_thickness, angle)))

    # Profiles with composite material made form only one UD-layer
    profile_geometry_dict[700] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3)
    profile_geometry_dict[701] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3,
        webs=[(web_line_1, l3)])
    profile_geometry_dict[702] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3,
        webs=[(web_line_2, l3)])
    profile_geometry_dict[703] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3,
        webs=[(web_line_2, l3), (web_line_3, l3)])
    profile_geometry_dict[704] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-0012-cos-50.txt'), True), l3,
        webs=[(web_line_4, l3)])
    profile_geometry_dict[705] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l3,
        webs=[(web_line_4, l3)])
    profile_geometry_dict[706] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l3,
        webs=[(web_line_2, l3), (web_line_1, l3)])
    profile_geometry_dict[707] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l3)
    profile_geometry_dict[708] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l3,
        material_regions=[((Vector([0.2, 0.07]), Vector([0.8, 0.04])), l3_thick),
                          ((Vector([0.2, -0.04]), Vector([0.8, -0.01])), l3_thick)])
    # CAS
    profile_geometry_dict[710] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3_pos_angle)
    # CUS
    profile_geometry_dict[711] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3_pos_angle,
        material_regions=[((Vector([1, 0.5]), Vector([0, 0.0])), l3_neg_angle)])

    # CAS
    profile_geometry_dict[712] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l3_pos_angle_45)
    #     profile_geometry_dict[800] = WingCrossSectionGeometryDefinition(load_profile_points(
    #                                     os.path.join(profiles_path, 'rectangle.txt'), False), l3)
    #
    #     # BECAS T2
    #     profile_geometry_dict[801] = WingCrossSectionGeometryDefinition(load_profile_points(
    #                                     os.path.join(profiles_path, 'T2.txt'), False), [ortho1_neg, iso1, ortho1_pos, iso1],
    #                                     profile_keypoints=[0, 1, 1.25, 2.25],
    #                                     webs=[(LineString([[-0.25,-1],[-0.25,1]]), iso1), (LineString([[0,-1],[0,1]]), iso1)])
    #     # D-nose
    #     web_lines = [LineString([[0.2,-1],[0.2,2]]), LineString([[0.4,-1],[0.4,2]])]
    #     profile_geometry_dict[810] = WingCrossSectionGeometryDefinition(load_profile_points(
    #                                     os.path.join(profiles_path, 'DU 08-W-210-6.5.txt'), True), [i2, i1, i2, i1],
    #                                     webs=[(web_lines[0], i3), (web_lines[1], i3)],
    #                                     maintain_existing_nodes=False, profile_keypoints=[], profile_keypoint_lines=web_lines)
    #
    #     # Very thick profile
    #     profile_geometry_dict[802] = WingCrossSectionGeometryDefinition(load_profile_points(
    #                                     os.path.join(profiles_path, 'rectangle.txt'), False), [alu4])
    #     # Very very thick profile
    #     profile_geometry_dict[803] = WingCrossSectionGeometryDefinition(load_profile_points(
    #                                     os.path.join(profiles_path, 'rectangle.txt'), False), [alu5])
    #     # Very very very thick profile
    #     profile_geometry_dict[804] = WingCrossSectionGeometryDefinition(load_profile_points(
    #                                     os.path.join(profiles_path, 'rectangle.txt'), False), [alu6])

    # For the paper
    profile_geometry_dict[900] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu)
    profile_geometry_dict[901] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell)
    # CAS
    profile_geometry_dict[902] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle)
    # CUS
    profile_geometry_dict[903] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle,
        material_regions=[((Vector([0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_neg_angle)])

    profile_geometry_dict[910] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu,
        webs=[(web_line_2, alu), (web_line_1, alu)])
    profile_geometry_dict[911] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_shell,
        webs=[(web_line_2, l_web), (web_line_1, l_web)])

    # Variation of the fiber orientation (composite laminate, CAS)
    profile_geometry_dict.update(
        get_fiber_angle_variation_geometry_dict(1000, 73, 5, os.path.join(profiles_path, 'rectangle_center.txt'),
                                               lambda angle: get_shell_layup(p1, p1_thickness, angle)))

    orientation = 0
    l_test = CompositeShell(name='Laminat Test', layup=[(p1, p1_thickness, orientation + 0.0),
                                                (p1, p1_thickness, orientation - 90.0),
                                                (p1, p1_thickness, orientation - 45.0)])
    profile_geometry_dict[1100] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_test)

    profile_geometry_dict[1200] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu)
    profile_geometry_dict[1201] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l3)
    # CAS
    profile_geometry_dict[1202] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l3_pos_angle)
    # CUS
    profile_geometry_dict[1203] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l3_pos_angle,
        material_regions=[((Vector([0.5, 0.25]), Vector([-0.5, -0.25])), l3_neg_angle)])

    profile_geometry_dict[1210] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu,
        webs=[(web_line_2, alu), (web_line_1, alu)])
    profile_geometry_dict[1211] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l3,
        webs=[(web_line_2, l3), (web_line_1, l3)])

    # Variation of the fiber orientation (composite laminate, CAS)
    profile_geometry_dict.update(
        get_fiber_angle_variation_geometry_dict(1300, 37, 10, os.path.join(profiles_path, 'rectangle_center.txt'),
                                               lambda angle: get_laminate_3_layup(p3, p3_thickness, angle)))

    # CAS
    profile_geometry_dict[1400] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_paper_center.txt'), False), l7_15, element_size=1e-3)
    profile_geometry_dict[1401] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_paper_center.txt'), False), l7, element_size=1e-3)
    profile_geometry_dict[1402] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_paper_center_midsurface.txt'), False), l7_15, element_size=1e-3,
        profile_thickness_direction='center')
    profile_geometry_dict[1403] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_paper_center_midsurface.txt'), False), l7, element_size=1e-3,
        profile_thickness_direction='center')

    #     # Variation of the fiber orientation ((-30/30) laminate)
    #     profile_geometry_dict.update(get_fiber_angle_variation_geometry_dict(900, 37, 5, os.path.join(profiles_path, 'rectangle_center.txt'), lambda angle: [(p1, p1_thickness, angle+30.0)), (p1, p1_thickness, angle-30.0))]))
    #
    #     # Variation of the fiber orientation ((-45/45) laminate)
    #     profile_geometry_dict.update(get_fiber_angle_variation_geometry_dict(1000, 37, 5, os.path.join(profiles_path, 'rectangle_center.txt'), lambda angle: [(p1, p1_thickness, angle+45.0)), (p1, p1_thickness, angle-45.0))]))
    #
    #     # Variation of the fiber orientation ((-60/60) laminate)
    #     profile_geometry_dict.update(get_fiber_angle_variation_geometry_dict(1100, 37, 5, os.path.join(profiles_path, 'rectangle_center.txt'), lambda angle: [(p1, p1_thickness, angle+60.0)), (p1, p1_thickness, angle-60.0))]))
    #
    #     # Variation of the element size
    #     for i in range(40):
    #         profile_geometry_dict[1200+i] = WingCrossSectionGeometryDefinition(get_circle_points(30), (2*np.pi/30)/(i+1), [l1])

    profile_geometry_dict[2000] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle.txt'), False), l1,
        material_regions=[
            ((Vector([1, 0]), Vector([1, 0.5])), l1),
            ((Vector([1, 0.5]), Vector([0, 0.5])), l1),
            ((Vector([0, 0.5]), Vector([0, 0])), l1),
            ((Vector([0, 0]), Vector([1 - position_blurring, 0])), l1),
        ])

    # Variation of the element size
    for i in range(20):
        profile_geometry_dict[2100 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_shell,
            webs=[(web_line_2, l_web), (web_line_1, l_web)],
            element_size=1 / (i + 1),
            te_cutoff_x=0.98,
            profile_spline=airfoil_spline,
            base_material_as_material_region=True,
        )

    # Variation of the geometry discretization
    for i, num_points in enumerate([20, 50, 100, 150, 200]):
        profile_geometry_dict[2200 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, f'NACA-2412-cos-{num_points}.txt'), True), l_shell,
            webs=[(web_line_2, l_web), (web_line_1, l_web)],
            element_size=0.01,
            te_cutoff_x=0.98,
            profile_spline=airfoil_spline,
            base_material_as_material_region=True,
        )

    # Variation of the element size
    for i in range(10):
        profile_geometry_dict[2300 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu_shell,
            webs=[(web_line_2, alu_shell), (web_line_1, alu_shell)],
            element_size=0.1 / (i + 1),
            te_cutoff_x=0.98,
            profile_spline=airfoil_spline,
            base_material_as_material_region=True,
        )

    # Variation of the element size
    for i in range(40):
        profile_geometry_dict[2400 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'rectangle_center.txt'), False), l1,
            material_regions=[
                ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l1),
                ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l1),
                ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l1),
                ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l1),
            ],
            webs=[(web_line_4, l1)],
            element_size=1 / (i + 1)
        )

    # Variation of the element size
    for i in range(40):
        profile_geometry_dict[2500 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
            material_regions=[
                ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
                ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
                ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
                ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell),
            ],
            element_size=1 / (i + 1)
        )


    # Variation of the element size
    for i in range(40):
        profile_geometry_dict[10000 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'rectangle_center.txt'), False), alu_shell,
            material_regions=[
                ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), alu_shell),
                ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), alu_shell),
                ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), alu_shell),
                ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), alu_shell),
            ],
            element_size=1 / (i + 1),
        )

    # Variation of the element size
    for i in range(40):
        profile_geometry_dict[10100 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
            material_regions=[
                ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
                ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
                ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
                ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell),
            ],
            element_size=1 / (i + 1),
        )

    # Variation of the element size
    for i in range(40):
        # CAS
        profile_geometry_dict[10200 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle,
            material_regions=[
                ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_pos_angle),
                ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_pos_angle),
                ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_pos_angle),
                ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_pos_angle),
            ],
            element_size=1 / (i + 1),
        )

    # Variation of the element size
    for i in range(40):
        # CUS
        profile_geometry_dict[10300 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell_pos_angle,
            material_regions=[
                ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell_neg_angle),
                ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell_neg_angle),
                ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell_pos_angle),
                ((Vector([-0.5, -0.25]), Vector([0.5 - position_blurring, -0.25])), l_shell_neg_angle),
            ],
            element_size=1 / (i + 1),
        )

    # Variation of the element size
    for i in range(40):
        profile_geometry_dict[11000 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), alu_shell,
            webs=[(web_line_2, alu_shell), (web_line_1, alu_shell)],
            element_size=0.1 / (i + 1),
            te_cutoff_x=0.98,
            profile_spline=airfoil_spline,
            base_material_as_material_region=True,
        )

    # Variation of the element size
    for i in range(40):
        profile_geometry_dict[11100 + i] = WingCrossSectionGeometryDefinition(load_profile_points(
            os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_shell,
            webs=[(web_line_2, l_web), (web_line_1, l_web)],
            element_size=0.1 / (i + 1),
            te_cutoff_x=0.98,
            profile_spline=airfoil_spline,
            base_material_as_material_region=True,
        )

    # Open cross-sections
    element_size_open_cs = 0.05
    profile_geometry_dict[50] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), alu_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), alu_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), alu_shell),
        ],
        element_size=element_size_open_cs,
        close_open_ends=False,
    )

    profile_geometry_dict[51] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), alu_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), alu_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), alu_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), alu_shell),
        ],
        webs=[(web_line_6, alu_shell),],
        element_size=element_size_open_cs,
        close_open_ends=False,
    )

    profile_geometry_dict[52] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
        ],
        element_size=element_size_open_cs,
        close_open_ends=False,
    )

    profile_geometry_dict[53] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
        ],
        webs=[(web_line_6, l_shell),],
        element_size=element_size_open_cs,
        close_open_ends=False,
    )

    profile_geometry_dict[54] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
        ],
        webs=[(web_line_6, l_web),],
        element_size=element_size_open_cs,
        close_open_ends=False,
    )
    profile_geometry_dict[55] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'rectangle_center.txt'), False), l_shell,
        material_regions=[
            ((Vector([0.5, -0.25]), Vector([0.5, 0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([-0.5, 0.25])), l_shell),
            ((Vector([-0.5, 0.25]), Vector([-0.5, -0.25])), l_shell),
        ],
        webs=[(web_line_6, l_web), (web_line_4, l_web),],
        element_size=element_size_open_cs,
        close_open_ends=False,
    )

    element_size_open_cs2 = 0.1
    profile_geometry_dict[60] = WingCrossSectionGeometryDefinition(
        [Vector([0, -1]), Vector([0, 1])],
        l_shell,
        webs=[((Vector([-1, 1]), Vector([1, 1])), l_shell),],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[61] = WingCrossSectionGeometryDefinition(
        [Vector([0, -1]), Vector([0, 1])],
        l_shell,
        webs=[((Vector([-1, 1]), Vector([1, 1])), l_shell),((Vector([-1, -1]), Vector([1, -1])), l_shell),],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[62] = WingCrossSectionGeometryDefinition(
        [Vector([-1, -0.5]), Vector([-1, -1]), Vector([0, -1]), Vector([0, 1]), Vector([1, 1]), Vector([1, 0.5])],
        l_shell,
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[63] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center_closed.txt'), False),
        l_shell,
        webs=[((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_shell),((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell)],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[64] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center_closed.txt'), False),
        l_shell,
        webs=[
            ((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_shell),
            ((Vector([-0.5, -0.25]), Vector([-1, -0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([1, 0.25])), l_shell),
            ((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell),
        ],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[65] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center.txt'), False),
        l_shell,
        webs=[((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_shell),((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell)],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[66] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center.txt'), False),
        l_shell,
        webs=[
            ((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_shell),
            ((Vector([-0.5, -0.25]), Vector([-1, -0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([1, 0.25])), l_shell),
            ((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell),
        ],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[70] = WingCrossSectionGeometryDefinition(
        [Vector([0, -1]), Vector([0, 1])],
        l_web,
        webs=[((Vector([-1, 1]), Vector([1, 1])), l_shell),],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[71] = WingCrossSectionGeometryDefinition(
        [Vector([0, -1]), Vector([0, 1])],
        l_web,
        webs=[((Vector([-1, 1]), Vector([1, 1])), l_shell), ((Vector([-1, -1]), Vector([1, -1])), l_shell),],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[72] = WingCrossSectionGeometryDefinition(
        [Vector([-1, -0.5]), Vector([-1, -1]), Vector([0, -1]), Vector([0, 1]), Vector([1, 1]), Vector([1, 0.5])],
        l_shell,
        material_regions=[((Vector([0, -1]), Vector([0, 1])), l_web),],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[73] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center_closed.txt'), False),
        l_shell,
        webs=[
            ((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_web),
            ((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell),
        ],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[74] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center_closed.txt'), False),
        l_shell,
        webs=[
            ((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_shell),
            ((Vector([-0.5, -0.25]), Vector([-1, -0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([1, 0.25])), l_web),
            ((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell),
        ],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[75] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center.txt'), False),
        l_shell,
        webs=[
            ((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_web),
            ((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell),
        ],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    profile_geometry_dict[76] = WingCrossSectionGeometryDefinition(
        load_profile_points(os.path.join(profiles_path, 'rectangle_center.txt'), False),
        l_shell,
        webs=[
            ((Vector([-0.5, 0.25]), Vector([-1, 0.25])), l_shell),
            ((Vector([-0.5, -0.25]), Vector([-1, -0.25])), l_shell),
            ((Vector([0.5, 0.25]), Vector([1, 0.25])), l_web),
            ((Vector([0.5, -0.25]), Vector([1, -0.25])), l_shell),
        ],
        element_size=element_size_open_cs2,
        close_open_ends=False,
        web_parts=True,
        profile_thickness_direction='center',
    )

    element_size_debug = 0.01  # 0.01

    profile_geometry_dict[81] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_shell,
        webs=[(web_line_2, l_web), (web_line_1, l_web)],
        element_size=element_size_debug,
        te_cutoff_x=0.8,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
        close_open_ends=False,
    )

    profile_geometry_dict[82] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_real_shell,
        webs=[(web_line_2, l_real_web), (web_line_1, l_real_web)],
        element_size=element_size_debug,
        te_cutoff_x=0.8,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
        close_open_ends=False,
    )

    profile_geometry_dict[83] = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), l_real_shell,
        webs=[(web_line_2, l_real_web), (web_line_1, l_real_web)],
        material_regions=[
            ((Vector([0.285418,  0.078363]), Vector([0.344680,  0.079198])), l_real_cap),
            ((Vector([0.469023,  0.074547]), Vector([0.532138,  0.069890])), l_real_cap),
            ((Vector([0.288802, -0.041549]), Vector([0.346303, -0.039941])), l_real_cap),
            ((Vector([0.468187, -0.035070]), Vector([0.530653, -0.031808])), l_real_cap),
        ],
        element_size=element_size_debug,
        te_cutoff_x=0.8,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
        close_open_ends=False,
    )

    return profile_geometry_dict
