# cython: profile=True
"""
Helping functions for PreDoCS.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import numpy as np

from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.data import interp1d
from PreDoCS.util.geometry import transform_direction_m, transform_location_m
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)

try:
    from cpacs_interface.loads import create_moved_load_vector

except ImportError:
    log.info('Modul cpacs_interface.loads not found. Use PreDoCS function.')

    def create_moved_load_vector(va, vn, fa, ma):
        """
        Loads are moved within the cross section plane from the load reference points to the load application points.

        Parameters
        ----------
        va: Vector
            positioning of the old force and moment vector fa, ma
        vn: Vector
            positioning of the new force and moment vector fn, m,
        fa: Vector
            old force vector
        ma: Vector
            old moment vector
        Returns
        -------
        fn: Vector
            new force vector
        mn: Vector
            new Moment vector
        """
        vna = va - vn

        fn = fa
        mn = ma + np.cross(vna, fa)

        return fn, mn


def intersect(a, b):
    """
    Returns the intersection of two lists.
        
    Parameters
    ----------
    a: list(object)
        First list.
    b: list(object)
        Second list.
        
    Returns
    -------
    list
        Intersection.
    """
    return list(set(a) & set(b))


def get_EI_eta(phi, EI_x, EI_y, EI_xy):
    """
    Calculates the elastic second moment of area around the eta-axis, if the coordinate system is rotated about phi.
    Eta is the rotated x-axis, xi the rotated y-axis.

    Parameters
    ----------
    phi: float
        Rotation angle in RAD.
    EI_x: float
        Elastic second moment of area around the x-axis.
    EI_y: float
        Elastic second moment of area around the y-axis.
    EI_x: float
        Elastic moment of deviation around the x- and y-axis.
        
    Returns
    -------
    float
        Elastic second moment of area around the eta-axis.
    """
    return (EI_x+EI_y)/2. + (EI_x - EI_y)/2. * np.cos(2.*phi) + EI_xy * np.sin(2.*phi)


def get_EI_xi(phi, EI_x, EI_y, EI_xy):
    """
    Calculates the elastic second moment of area around the xi-axis, if the coordinate system is rotated about phi.
    Eta is the rotated x-axis, xi the rotated y-axis.
    
    Parameters
    ----------
    phi: float
        Rotation angle in RAD.
    EI_x: float
        Elastic second moment of area around the x-axis.
    EI_y: float
        Elastic second moment of area around the y-axis.
    EI_x: float
        Elastic moment of deviation around the x- and y-axis.
        
    Returns
    -------
    float
        Elastic second moment of area around the xi-axis.
    """
    return (EI_x+EI_y)/2. - (EI_x - EI_y)/2. * np.cos(2.*phi) - EI_xy * np.sin(2.*phi)


def get_EI_eta_xi(phi, EI_x, EI_y, EI_xy):
    """
    Calculates the elastic moment of deviation around the eta- and xi-axis, if the coordinate system is rotated about phi.
    Eta is the rotated x-axis, xi the rotated y-axis.

    Parameters
    ----------
    phi: float
        Rotation angle in RAD.
    EI_x: float
        Elastic second moment of area around the x-axis.
    EI_y: float
        Elastic second moment of area around the y-axis.
    EI_x: float
        Elastic moment of deviation around the x- and y-axis.
        
    Returns
    -------
    float
        Elastic moment of deviation around the eta- and xi-axis.
    """
    return - (EI_x - EI_y)/2. * np.sin(2.*phi) + EI_xy * np.cos(2.*phi)


def get_polygon_area(x, y):
    """
    Returns the area of a polygon. [https://en.wikipedia.org/wiki/Shoelace_formula]
         
    Parameters
    ----------
    x: list(float)
        List of x-coordinates of the polygon edges.
    y: list(float)
        List of y-coordinates of the polygon edges.
        
    Returns
    -------
    float
        Area of the polygon.
    """
    # https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates

    # coordinate shift
    x_ = x - np.mean(x)
    y_ = y - np.mean(y)

    # everything else is the same as maxb's code
    correction = x_[-1] * y_[0] - y_[-1] * x_[0]
    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])

    return 0.5 * np.abs(main_area + correction)

def enclosed_area_vector(cells):
    """
    Parameters
    ----------
    cells: list(Cell)
        List of cells.
        
    Returns
    -------
    np.array
        Vector of the enclosed area of the cells.
    """
    return np.array([c.area for c in cells])


def idx(a):
    """
    Returns a numpy matrix index from a readable two-digit number. 22 -> (1,1); 52 -> (4,1)
    
    Parameters
    ----------
    a: int
        Two-digit integer.
        
    Returns
    -------
    (int, int)
        Numpy matrix index.
    """
    s = str(a)
    return (int(s[0])-1, int(s[1])-1)


def check_symmetric(m, tol=1e-8):
    """
    Checks, if a matrix is symmetric.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
    tol: float (default: 1e-8)
        The absolute tolerance of two identical elements.
        
    Returns
    -------
    bool
        True, if the matrix is symmetric.
    """
    return np.allclose(m, m.T, atol=tol)


def symmetrize(m):
    """
    Returns a symmetric matrix from a matrix where only the upper or lower triangular matrix are set.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
        
    Returns
    -------
    numpy.ndarray
        The symmetric matrix.
    """
    return m + m.T - np.diag(np.diag(m))


def get_matrix_string(m):
    """
    Returns the matrix as string.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
    
    Returns
    -------
    str
        The matrix string.
    """
    s = ''
    for row in range(m.shape[0]):
        for col in range(m.shape[1]):
            s = '{} {:5e}\t'.format(s, m[row, col])
        s += '\n'
    return s


def print_matrix(m):
    """
    Prints a matrix.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
    """
    print(get_matrix_string(m))


def get_shear_principal_axis_stiffness_and_angle(stiffness_matrix):
    """
    Returns the shear principal axis angle and stiffness.

    Parameters
    ----------
    numpy.ndarray
        3x3 cross section stiffness matrix. 1: shear x, 2: shear y, 3: torsion.

    Returns
    -------
    Vector
        Shear principal stiffness.
    float
        Shear principal axis angle in RAD.
    """
    K_1 = stiffness_matrix[0:2, 0:2]
    K_2 = stiffness_matrix[2:3, 2:3]
    K_3 = stiffness_matrix[0:2, 2:3]

    # Pure bending matrix (with the assumption that the normal force is zero)
    K_shear = K_1 - K_3 @ np.linalg.inv(K_2) @ K_3.T
    shear_paa, shear_pas = get_principal_axis_angle(K_shear)

    return shear_pas, shear_paa


def get_elatic_center_and_bending_principal_axis_angle(stiffness_matrix):
    """
    Returns the elastic center and the principal axis angle. [Giavotto1983]_, p. 7 and [BECAS2012]_, pp. 8,9

    Parameters
    ----------
    numpy.ndarray
        3x3 cross section stiffness matrix. 1: extension, 2: bending x, 3: bending y.

    Returns
    -------
    Vector
        Elastic center of the cross section.
    Vector
        Elastic principal second moments of area.
    float
        Principal axis angle in RAD.
    """
    ec = Vector([-stiffness_matrix[0, 2] / stiffness_matrix[0, 0], stiffness_matrix[0, 1] / stiffness_matrix[0, 0]])

    K_1 = stiffness_matrix[0:1, 0:1]
    K_2 = stiffness_matrix[1:3, 1:3]
    K_3 = stiffness_matrix[0:1, 1:3]

    # Pure bending matrix (with the assumption that the normal force is zero)
    K_bending = K_2 - K_3.T @ np.linalg.inv(K_1) @ K_3
    #log.debug(f'K_bending: {K_bending}')
    paa, pas = get_principal_axis_angle(K_bending)

    return ec, pas, paa


def get_principal_axis_angle(stiffness_matrix):
    """
    Returns principal axis angle from a 2x2 matrix. [BECAS2012]_, pp. 8,9
    The first axis is the one with the bigger stiffness (pas[0] > pas[1]).
    
    Parameters
    ----------
    numpy.ndarray
        2x2 stiffness matrix.
    
    Returns
    -------
    float
        Principal axis angle in RAD.
    Vector
        Principal axis stiffness.
    """
    w, v = np.linalg.eigh(stiffness_matrix)
    if w[0] > w[1]: # X-axis has the bigger stiffness
        X = Vector(v[:,0].flatten())
        pas = Vector([w[0], w[1]])
    else:
        X = Vector(v[:,1].flatten())
        pas = Vector([w[1], w[0]])
    return X.angle_in_plane, pas


# TODO: diese Berechnung NICHT im HA-Koos machen!
def calc_shear_center(
        discreet_geometry: 'DiscreetCrossSectionGeometry',
        load_states, pa_atm, pa_atm_inv, transverse_shear=False
):
    """
    Returns the shear center of the cross section in the cross section coordinate system.

    Parameters
    ----------
    discreet_geometry:
        The discreet geometry for the cross section analysis.
    load_states: dict(IElement, list(float)):
        Load states for an element:
            0: N_zs caused by a unit transverse force in x beanding principle direction.
            1: N_zs  caused by a unit transverse force in y beanding principle direction.
            2: N_zn caused by a unit transverse force in x beanding principle direction.
            3: N_zn caused by a unit transverse force in y beanding principle direction.
    pa_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the bending principal axis
        coordinate system.
    pa_atm_inv: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the bending principal axis to the cross section
        coordinate system.
    transverse_shear: bool (default: False)
        True, if transverse shear is included in the shear center calculation.

    Returns
    -------
    Vector
        Shear center of the cross section in the cross section coordinate system.
    """
    # TODO: hin- und rücktransformation überhaupt nötig?
    X_sc = 0.
    Y_sc = 0.
    for element in load_states.keys():
        # Element position in the  principal axis coordinate system
        position_element_principal_axis = transform_location_m(
            pa_atm, discreet_geometry.element_reference_position_dict[element]
        )
        position_element_principal_axis_3d = Vector([position_element_principal_axis.x, position_element_principal_axis.y, 0.])
        
        # Element length-vector in the principal axis coordinate system
        element_length_vector = discreet_geometry.node_midsurface_positions[element.node2] - discreet_geometry.node_midsurface_positions[element.node1]
        del_s = transform_direction_m(pa_atm, element_length_vector)
        del_s_3d = Vector([del_s.x, del_s.y, 0.])
        
        lever_membrane = np.cross(position_element_principal_axis_3d, del_s_3d)[2]
        
        if transverse_shear:
            # Element thickness-vector in the principal axis coordinate system
            del_n = element_length_vector.length * transform_direction_m(pa_atm, element.thickness_vector).normalised
            del_n_3d = Vector([del_n.x, del_n.y, 0.])
            lever_transverse = np.cross(position_element_principal_axis_3d, del_n_3d)[2]
        
        X_sc += load_states[element][1] * lever_membrane +\
                ((load_states[element][3] * lever_transverse) if transverse_shear else 0.)
        Y_sc -= load_states[element][0] * lever_membrane +\
                ((load_states[element][2] * lever_transverse) if transverse_shear else 0.)
        
    # Transform SC from principal axis coordinate system in the cross section coordinate system
    return transform_location_m(pa_atm_inv, Vector([X_sc, Y_sc]))


def one(iterable):
    """
    https://stackoverflow.com/a/16801605/10417332
    :param iterable:
    :return:
    """
    i = iter(iterable)
    return any(i) and not any(i)


def make_linear_function(l, f1, f2):
    def func_linear(s):
        return (f2 - f1) / l * s + f1
    return func_linear


def make_quadratic_function(l, f1, f2, f3):
    def func_quadratic(s):
        a = 2 * (f1 + f2 - 2 * f3) / l ** 2
        b = -(3 * f1 + f2 - 4 * f3) / l
        c = f1
        return a * s * s + b * s + c
    return func_quadratic


def is_number(value):
    """
    Checks, if the object is a number.

    Parameters
    ----------
    value: ?
        The object.

    Returns
    -------
    bool
        True, if value is a number, otherwise False
    """
    try:
        float(value)
        return True
    except:
        return False


def get_matrix_interpolation_function(x_matrices, matrices, **kwargs):
    """
    Creates a matrix of interpolation functions from a list of matrices at given positions
    using spline interpolation for default.

    Parameters
    ----------
    x_matrices: list(float)
        List of coordinates of the matrices.
    matrices: list(numpy.ndarray)
        The matrices to interpolate.
    kwargs:
        kwargs from scipy.interpolate.interp1d. Default values:
            - kind='linear'
            - fill_value='extrapolate'

    Returns
    -------
    function(float) -> numpy.ndarray
        Matrix interpolation function.
    """
    matrices = np.array(matrices)
    #assert matrices.ndim == 3
    assert len(x_matrices) == matrices.shape[0]

    return interp1d(
        x_matrices, matrices,
        axis=0,
        kind=kwargs.get('kind', 'linear'),
        fill_value=kwargs.get('fill_value', 'extrapolate'),
    )


def get_interpolated_stiffness_and_inertia_matrices(
        cross_section_data: list[tuple['ICrossSectionStiffness', 'ICrossSectionInertia']],
        z_cross_sections: list[float],
        z_interpolate: list[float]
):
    """
    Interpolate the cross section stiffness and inertia data from `cross_section_data` and `z_cross_sections`
    to the positions given in `z_interpolate` using spline interpolation.

    Parameters
    ----------
    cross_section_data
        List of the cross section data.
    z_cross_sections
        List of z-coordinates of the cross sections.
    z_interpolate
        List of z-coordinates for the interpolated matrices.

    Returns
    -------
    list(numpy.ndarray)
        List of the cross section stiffness matrices.
    list(numpy.ndarray)
        List of the cross section inertia matrices.
    """
    interpolated_stiffness_matrices = get_matrix_interpolation_function(
        z_cross_sections,
        [d[0].stiffness_matrix for d in cross_section_data]
    )(z_interpolate)
    interpolated_inertia_matrices = get_matrix_interpolation_function(
        z_cross_sections,
        [d[1].inertia_matrix for d in cross_section_data]
    )(z_interpolate)
    return interpolated_stiffness_matrices, interpolated_inertia_matrices


def pt_is_in_plane_dir(p0, p_normal, pt):
    """
    Checks if the point pt lies in positive normal direction of the plane defined by the point p0 and normal direction
    p_normal

    Parameters
    ----------
    p0: Vector
        reference point of the plane
    p_normal: Vector
        normal direction of the plane
    pt: Vector
        Point to check

    Returns
    -------
    boolean
        True if the point lies in positive normal direction of the plane or in the plane itself
    """
    # get the intersection point of the point to the plane
    intersection = line_plane_intersection(pt, p_normal, p0, p_normal)

    dir_plane_to_pt = pt - intersection
    if np.allclose(dir_plane_to_pt, [0, 0, 0]):
        return True
    dir_plane_to_pt_norm = dir_plane_to_pt.normalised
    if np.allclose(dir_plane_to_pt_norm, p_normal) or all(np.isnan(dir_plane_to_pt_norm)):
        return True
    else:
        # negative direction
        return False


def line_line_intersection(l0, l0_dir, l1, l1_dir, eps=1e-6):
    """
    Finds the intersection point of two given lines g0 and g1, if it exists. Else None is returned.
    The lines are defined as g0 = l0 + x0 * l0_dir and g1 = l1 + x1 * l1_dir

    Parameters
    ----------
    l0, l1 : Vector
        Reference point for line 0 and line 1
    l0_dir, l1_dir : Vector
        Reference direction of line 0 and line 1
    eps : float
        tolerance

    Returns
    -------
    Vector
        Intersection point
    """

    intersection_point = None

    A = np.array([[l1_dir_i, -l0_dir_i] for l0_dir_i, l1_dir_i in zip(l0_dir, l1_dir)])
    b = l0 - l1
    intersections, _, _, _ = np.linalg.lstsq(A, b)  # Errors are not handeled. Might not happen for this type of problem

    x0 = intersections[1]
    x1 = intersections[0]
    intersection_point0 = l0 + l0_dir * x0
    intersection_point1 = l1 + l1_dir * x1

    if np.linalg.norm(intersection_point0 - intersection_point1) < eps:
        intersection_point = Vector(intersection_point0)

    return intersection_point


def line_plane_intersection(l0, l_dir, p0, p_normal, eps=1e-6):
    """
    Finds the intersection point of the line "l0 + x * l_dir" and the plane, defined by a point and normal direction

    Parameters
    ----------
    l0: Vector
        reference point for line
    l_dir: Vector
        reference direction of the line
    p0: Vector
        reference point of the plane
    p_normal: Vector
        normal direction of the plane

    Returns
    -------
    Vector
        Point of intersection. If no intersection is found, "None" is returned
    """

    l_dot_p = l_dir.dot(p_normal)

    if abs(l_dot_p) > eps:
        w = l0 - p0
        si = -p_normal.dot(w) / l_dot_p
        pt_int = w + si * l_dir + p0

        return pt_int
    else:
        return None


def get_mean_position(positions: list[Vector]) -> Vector:
    return Vector(np.mean(positions, axis=0))


def get_function_with_bounds(function_without_bounds, s: float, bounds: tuple[float, float]) -> float:
    """
    Checks for the given function, if the parameter is in the given bounds.
    Returns the value of the function at the given parameter value.

    Parameters
    ----------
    function_without_bounds: function(float)
        The function.
    s
        The parameter value.
    bounds
        Lower and upper bound.

    Returns
    -------
    float
        Value of the function at the given parameter value.
    """
    assert s >= bounds[0]
    assert s <= bounds[1] + 1e-8  # TODO: remove  + 1e-8 (tolerance)
    return function_without_bounds(s)


def CoG_from_inertia_matrix(inertia_matrix: np.ndarray) -> Vector:
    """
    Calcs the center of gravity from a 6x6 inertia matrix.
    """
    mu = inertia_matrix[0, 0]
    s_x = inertia_matrix[1, 5]
    s_y = -inertia_matrix[0, 5]
    return Vector([s_x/mu, s_y/mu])


def rotating_inertia_matrix_around_CoG(inertia_matrix: np.ndarray) -> np.ndarray:
    """
    Calcs the 3x3 rotating inertia matrix around the center of gravity from a 6x6 inertia matrix.

    See https://de.wikipedia.org/wiki/Steinerscher_Satz
    """
    I = inertia_matrix[3:6, 3:6]
    r = CoG_from_inertia_matrix(inertia_matrix)
    m = inertia_matrix[0, 0]
    a = np.array([
        [0, 0, r.y],
        [0, 0, -r.x],
        [-r.y, r.x, 0],
    ])
    I_cog = I - m * a.T @ a
    return I_cog


def principal_rotating_inertia_around_CoG(inertia_matrix: np.ndarray) -> tuple[Vector, list[Vector]]:
    """
    Calculates the principal rotating inertia around the center of gravity in the cross-section coordinate system.

    Returns
    -------
    Vector
        Principal rotating inertia around the center of gravity.
    Vector
        Rotational vectors of the principal rotating inertia around the center of gravity.
    """
    I_cog = rotating_inertia_matrix_around_CoG(inertia_matrix)

    pa_inertia, pa_vectors = np.linalg.eigh(I_cog)
    pa_vectors = [Vector(pa_vectors[:, i]) for i in range(3)]

    return Vector(pa_inertia), pa_vectors
