"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import math
import os
from distutils.util import strtobool

import matplotlib.pyplot as plt
import numpy as np
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Quaternion, gp_EulerSequence
from OCC.Display.OCCViewer import rgb_color, Viewer3d

from PreDoCS.CrossSectionAnalysis.Display import _save_and_show
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.geometry import transform_displacements_vectors
from PreDoCS.util.occ import transform_shape, vector_to_point, vector_to_occ_vector, transformation_matrix_2_occ
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


def element2edge(element):
    """
    Creates an edge from an element.
    
    Parameters
    ----------
    element: IElement
        The element.
    
    Returns
    -------
    OCC.TopoDS.TopoDS_Edge
        The edge.
    """
    pos1 = element.node1.position
    pos2 = element.node2.position
    return BRepBuilderAPI_MakeEdge(gp_Pnt(pos1.x, pos1.y, 0), gp_Pnt(pos2.x, pos2.y, 0)).Edge()


def display_discreet_cross_section_geometry(
        viewer3d,
        discreet_geometry,
        transformation,
        color,
        transparency: float = 0.0,
):
    """
    Displays a cross section in a viewer.
    
    Parameters
    ----------
    viewer3d: OCC.Display.OCCViewer.Viewer3d
        The viewer.
    z2_coord: Vector
        At the z2-coordinate of the undeformed cross section.
    normal_dir: Vector
        Normal direction of the undeformed cross section
    discreet_geometry: DiscreetCrossSectionGeometry
        The discreet cross section geometry object.
    color: OCC.Quantity.Quantity_Color
        The color of the cross section.
    transparency: float (default: 0)
        Transparency of the cross section. 0 to 1. 0 is opaque, 1 is full transparent.
    displacements: list(float) (default: None)
        The displacements of the cross section (three translations, three rotations) for the deformed beam.
        None for the undeformed state.
    """
    edges = [element2edge(element) for element in discreet_geometry.elements]
    for edge in edges:
        viewer3d.DisplayShape(transform_shape(edge, transformation), color=color, transparency=transparency)


def display_wing_geometries(
        viewer3d,
        cpacs2predocs,
        transformation: gp_Trsf = None,
        plot_spars=False,
        **kwargs,
):
    """
    Displays the wing cross sections in a viewer. 
    
    Parameters
    ----------
    viewer3d: OCC.Display.OCCViewer.Viewer3d
        The viewer.
    cpacs2predocs: CPACS2PreDoCS
        The CPACS2PreDoCS object to display.
    predocs_coord: PreDoCSCoord
        THe PreDoCS coordinate system definition.
    plot_spars: bool (default: False)
        True, if the spar cut geometries should be plotted.
    shell_transparency: float (default: 0.5)
        Transparency of the wing shell. 0 to 1. 0 is opaque, 1 is full transparent.
    upper_shell_color: OCC.Quantity.Quantity_Color (default: color(1,0,0))
        The color of the upper wing shell.
    lower_shell_color: OCC.Quantity.Quantity_Color (default: color(0,1,0))
        The color of the lower wing shell.
    spar_transparency: float (default: 0.5)
        Transparency of the wing spar. 0 to 1. 0 is opaque, 1 is full transparent.
    spar_color: OCC.Quantity.Quantity_Color (default: color(0,0,1))
        The color of the wing spar.
    """
    # Arguments
    shell_transparency = kwargs.get('shell_transparency', 0.5)
    upper_shell_color = kwargs.get('upper_shell_color', rgb_color(1, 0, 0))
    lower_shell_color = kwargs.get('lower_shell_color', rgb_color(0, 1, 0))
    spar_transparency = kwargs.get('spar_transparency', 0.5)
    spar_color = kwargs.get('spar_color', rgb_color(0, 0, 1))

    if transformation is None:
        transformation = gp_Trsf()
    component_segment = cpacs2predocs.component_segment

    # Shell
    viewer3d.DisplayShape(transform_shape(component_segment.upper_shell.shape, transformation),
                          color=upper_shell_color, transparency=shell_transparency)
    viewer3d.DisplayShape(transform_shape(component_segment.lower_shell.shape, transformation),
                          color=lower_shell_color, transparency=shell_transparency)

    # Spars
    if plot_spars:
        for spar in component_segment.spars:
            viewer3d.DisplayShape(transform_shape(spar.tigl_shape.shape(), transformation), color=spar_color,
                                  transparency=spar_transparency)


def display_beam_cross_sections(
        viewer3d,
        predocs_coord,
        discreet_cross_section_geometries,
        color=rgb_color(0, 0, 0),
        beam_displacements=None,
        **kwargs,
):
    """
    Displays the wing geometry in the undeformed and deformed state.
    
    Parameters
    ----------
    viewer3d: OCC.Display.OCCViewer.Viewer3d
        The viewer.
    z2_cross_sections: list(float)
        The z2-coordinates of the undeformed cross sections.
    z2_2_predocs_coord: method
        Returns the PreDoCS coordinates for a given z2 coordinate.
    discreet_cross_section_geometries: list(DiscreetCrossSectionGeometry)
        List of discreet cross section geometry objects.
    beam_displacements: list(float) <- function(float)
        The displacements of the cross section (three translations, three rotations) as function the beam axis.
    undeformed_color: OCC.Quantity.Quantity_Color (default: color(0,0,0))
        The color of the undeformed cross sections.
    deformed_color: OCC.Quantity.Quantity_Color (default: color(1,1,1))
        The color of the deformed cross sections.
    """
    for z2, discreet_geometry in zip(predocs_coord.z2_cs, discreet_cross_section_geometries):
        if beam_displacements is None:
            display_discreet_cross_section_geometry(
                viewer3d,
                discreet_geometry,
                transformation_matrix_2_occ(predocs_coord.transformation_predocs_2_wing(z2)),
                color,
            )
        else:
            displacements_wing = beam_displacements(z2)
            translation_wing, rotation_wing = Vector(displacements_wing[0:3]), Vector(displacements_wing[3:6])
            translation_cs, rotation_cs = transform_displacements_vectors(
                translation_wing, rotation_wing, predocs_coord.transformation_wing_2_predocs(z2),
            )

            translation_wing_trsf = gp_Trsf()
            translation_wing_trsf.SetTranslation(vector_to_occ_vector(translation_cs))

            rotation_cs_q = gp_Quaternion()
            rotation_cs_q.SetEulerAngles(
                gp_EulerSequence.gp_Extrinsic_XYZ, rotation_cs.x, rotation_cs.y, rotation_cs.z,
            )
            rotation_cs_trsf = gp_Trsf()
            rotation_cs_trsf.SetRotation(rotation_cs_q)
            # rotation_cs_trsf.SetRotation(gp_Ax1(gp_Pnt(), gp_Dir(1, 0, 0)), translation_cs.x)
            # rotation_cs_trsf.SetRotation(gp_Ax1(gp_Pnt(), gp_Dir(0, 1, 0)), translation_cs.y)
            # rotation_cs_trsf.SetRotation(gp_Ax1(gp_Pnt(), gp_Dir(0, 0, 1)), translation_cs.z)

            trsf = (
                    translation_wing_trsf
                    * transformation_matrix_2_occ(predocs_coord.transformation_predocs_2_wing(z2))
                    * rotation_cs_trsf
            )
            display_discreet_cross_section_geometry(
                viewer3d,
                discreet_geometry,
                trsf,
                color,
            )


def display_beam_axis(
        viewer3d,
        predocs_coord,
        beam_displacements=None,
        color=rgb_color(0, 0, 0),
        number_interpolation_points: int = 30,
):
    """
    Displays the wing geometry in the undeformed a deformed state.

    Parameters
    ----------
    viewer3d: OCC.Display.OCCViewer.Viewer3d
        The viewer.
    z2_nodes: list(float)
        The z-coordinates of the beam nodes.
    beam_displacements: list(float) <- function(float)
        The displacements of the cross section (three translations, three rotations) as function the beam axis.
    color: OCC.Quantity.Quantity_Color (default: color(0,0,0))
        The color of the beam.
    """
    z2_nodes = predocs_coord.z2_bn

    # For all beam elements
    elements = []
    for i in range(len(z2_nodes)-1):
        z2_1 = z2_nodes[i]
        z2_2 = z2_nodes[i+1]
        if beam_displacements is None:
            element_points = [
                vector_to_point(predocs_coord.z2_2_point_wing(z2_1)),
                vector_to_point(predocs_coord.z2_2_point_wing(z2_2)),
            ]
        else:
            z2_interpolate = np.linspace(z2_1, z2_2, number_interpolation_points)
            element_points = []
            for z2 in z2_interpolate:
                point = predocs_coord.z2_2_point_wing(z2)
                displacements = beam_displacements(z2)
                element_points.append(vector_to_point(
                    point + Vector(displacements[0:3])
                ))
        elements.append(element_points)

    # Draw points and elements
    for element_points in elements:
        viewer3d.DisplayShape(element_points[0], color=color)
        for i in range(len(element_points) - 1):
            edge = BRepBuilderAPI_MakeEdge(element_points[i], element_points[i+1]).Edge()
            viewer3d.DisplayShape(edge, color=color)
    viewer3d.DisplayShape(elements[-1][-1], color=color)


def plot_beam_3d(
        c2p,
        predocs_coord,
        cs_processors,
        beam_displacements_function,
        display_wing_geometry: bool = True,
        display_axis: bool = True,
        display_cross_sections: bool = True,
        display_deformed_state: bool = True,
        **kwargs,
):
    DISABLE_OCC_VIEWER = bool(strtobool(os.getenv('DISABLE_OCC_VIEWER', '0')))
    if DISABLE_OCC_VIEWER:
        log.warning('OCC Viewer is disabled via environment variable "DISABLE_OCC_VIEWER". Exit plot_beam_3d.')
        return

    bg_color = rgb_color(1.0, 1.0, 1.0)
    undeformed_color = rgb_color(0.0, 0.0, 0.0)
    deformed_color = rgb_color(160 / 255, 64 / 255, 0.0)

    open_viewer = 'file' not in kwargs
    if open_viewer:
        # 3D Result Viewer with undeformed and deformed state
        from OCC.Display.SimpleGui import init_display
        viewer3d, start_display, add_menu, add_function_to_menu = init_display()
    else:
        viewer3d = Viewer3d()
        viewer3d.Create()
        viewer3d.SetModeShaded()

    if display_wing_geometry:
        # Display the shells and spars
        display_wing_geometries(
            viewer3d,
            c2p,
            transformation=transformation_matrix_2_occ(predocs_coord.transformation_aircraft_2_wing),
            **kwargs,
        )

    if display_axis:
        # Display the undeformed beam FEM elements
        display_beam_axis(
            viewer3d,
            predocs_coord,
            color=undeformed_color,
        )

        # Display the deformed beam FEM elements
        if display_deformed_state:
            display_beam_axis(
                viewer3d,
                predocs_coord,
                beam_displacements=beam_displacements_function,
                color=deformed_color,
            )

    if display_cross_sections:
        # Display the cross sections for the undeformed beam
        display_beam_cross_sections(
            viewer3d=viewer3d,
            predocs_coord=predocs_coord,
            discreet_cross_section_geometries=[p.discreet_geometry for p in cs_processors],
            beam_displacements=None,
            color=undeformed_color,
        )

        if display_deformed_state:
            # Display the cross sections for the deformed beam
            display_beam_cross_sections(
                viewer3d=viewer3d,
                predocs_coord=predocs_coord,
                discreet_cross_section_geometries=[p.discreet_geometry for p in cs_processors],
                beam_displacements=beam_displacements_function,
                color=deformed_color,
            )

    viewer3d.View_Iso()
    viewer3d.set_bg_gradient_color(bg_color, bg_color)
    viewer3d.FitAll()

    if open_viewer:
        start_display()
    else:
        filename = kwargs['file']
        viewer3d.ExportToImage(filename)
        log.info(f'3D export to "{filename}" successfully finished')



def display_vector(viewer3d, point, axis, **kwargs):
    """
    Displays the wing geometry in the undeformed an deformed state.

    Parameters
    ----------
    viewer3d: OCC.Display.OCCViewer.Viewer3d
        The viewer.
    point: Vector
        Where the vector origin is positioned
    axis: Vector
        The vector itself
    """
    pnt0 = vector_to_point(point)

    viewer3d.DisplayColoredShape(pnt0, color='RED')

    # TODO: Method broken?
    point = vector_to_point(point)
    vector = vector_to_occ_vector(axis)
    viewer3d.DisplayVector(vector, point)


def plot_beam_displacements(processor_dict, num_plots, rad2deg: bool = True, **kwargs):
    """
    Plots the beam displacements over the beam length.

    Parameters
    ----------
    processor_dict: dict(ICrossSectionProcessor, numpy.ndarray)
        The beam displacement data for each cross section processor as a matrix. First column is the z-position
        and the following num_plots columns are the displacement data.
    num_plots: int
        Number of displacements to plot.
    file: str
        File, where to save the plot. No for no saving.
    title: str (default: 'Beam displacements')
        Title of the plot.
    plot_size: (float, float) (default: (5, 3))
        Size of on plot in inches.
    """
    # Arguments
    plot_size = kwargs['plot_size'] if 'plot_size' in kwargs else (5, 3)
    title = kwargs['title'] if 'title' in kwargs else 'Beam displacements'
    x_label = kwargs['x_label'] if 'x_label' in kwargs else 'z [m]'
    y_labels = kwargs['y_labels'] if 'y_labels' in kwargs else None
    hide_legend = kwargs.get('hide_legend', False)

    legend = list(processor_dict.keys())

    cols = math.ceil(math.sqrt(num_plots))
    rows = math.ceil(num_plots / cols)
    if 'fig' in kwargs and 'axes' in kwargs:
        fig = kwargs.pop('fig')
        axarr = kwargs.pop('axes')
    else:
        fig, axarr = plt.subplots(rows, cols, sharex=True, sharey='row', squeeze=False,
                              figsize=(plot_size[0] * cols, plot_size[1] * rows))
    if title is not None:
        fig.suptitle(title)
    if y_labels is None:
        y_labels = [
            'ux [m]',
            'uy [m]',
            'uz [m]',
        ]
        if rad2deg:
            y_labels.extend([
                'rotx [DEG]',
                'roty [DEG]',
                'rotz [DEG]',
            ])
        else:
            y_labels.extend([
                'rotx [RAD]',
                'roty [RAD]',
                'rotz [RAD]',
            ])
    for i in range(num_plots):
        if rad2deg and i > 2:
            factor = np.rad2deg(1)
        else:
            factor = 1
        ax = axarr[i // cols, i % cols]
        for processor, load_case_data in processor_dict.items():
            ax.plot(load_case_data[:, 0].flatten(), factor * load_case_data[:, i + 1].flatten())
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_labels[i])
        ax.grid()
        if not hide_legend:
            ax.legend(legend)

    # Save and show figure
    _save_and_show(fig, **kwargs)


def plot_beam_cross_section_displacements(processor_dict, num_plots, **kwargs):
    """
    Plots the beam cross section displacements over the beam length.

    Parameters
    ----------
    processor_dict: dict(ICrossSectionProcessor, numpy.ndarray)
        The cross section displacements data for each cross section processor as a matrix. First column is the z-position
        and the following num_plots columns are the cross section displacements data.
    num_plots: int
        Number of cross section displacements to plot.
    file: str
        File, where to save the plot. No for no saving.
    title: str (default: 'Beam cross section displacements')
        Title of the plot.
    plot_size: (float, float) (default: (5, 3))
        Size of on plot in inches.
    """
    # Arguments
    plot_size = kwargs['plot_size'] if 'plot_size' in kwargs else (5, 3)
    title = kwargs['title'] if 'title' in kwargs else 'Beam cross section displacements'
    x_label = kwargs['x_label'] if 'x_label' in kwargs else 'z [m]'
    y_labels = kwargs['y_labels'] if 'y_labels' in kwargs else None

    legend = list(processor_dict.keys())

    cols = math.ceil(math.sqrt(num_plots))
    rows = math.ceil(num_plots / cols)
    fig, axarr = plt.subplots(rows, cols, sharex=True, sharey='row', squeeze=False,
                              figsize=(plot_size[0] * cols, plot_size[1] * rows))
    if title is not None:
        fig.suptitle(title)
    if y_labels is None:
        y_labels = [
            r"$\gamma_{xz}$",
            r"$\gamma_{yz}$",
            r"$w_0'$",
            r"$\Theta_x'$",
            r"$\Theta_y'$",
            r"$\phi'$",
            r"$\phi''$"
        ]
    for i in range(num_plots):
        ax = axarr[i // cols, i % cols]
        for processor, load_case_data in processor_dict.items():
            ax.plot(load_case_data[:, 0].flatten(), load_case_data[:, i + 1].flatten())
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_labels[i])
        ax.grid()
        ax.legend(legend)

    # Save and show figure
    _save_and_show(fig, **kwargs)


def plot_beam_internal_loads(processor_dict, num_plots, **kwargs):
    """
    Plots the beam internal loads over the beam length.

    Parameters
    ----------
    processor_dict: dict(ICrossSectionProcessor, numpy.ndarray)
        The beam internal loads data for each cross section processor as a matrix. First column is the z-position
        and the following num_plots columns are the internal loads data.
    num_plots: int
        Number of internal loads to plot.
    file: str
        File, where to save the plot. No for no saving.
    title: str (default: 'Beam internal loads')
        Title of the plot.
    plot_size: (float, float) (default: (5, 3))
        Size of on plot in inches.
    """
    # Arguments
    plot_size = kwargs['plot_size'] if 'plot_size' in kwargs else (5, 3)
    title = kwargs['title'] if 'title' in kwargs else 'Beam internal loads'
    x_label = kwargs['x_label'] if 'x_label' in kwargs else 'z [m]'
    y_labels = kwargs['y_labels'] if 'y_labels' in kwargs else None

    legend = list(processor_dict.keys())

    cols = math.ceil(math.sqrt(num_plots))
    rows = math.ceil(num_plots / cols)
    fig, axarr = plt.subplots(rows, cols, sharex=True, sharey='row', squeeze=False,
                              figsize=(plot_size[0] * cols, plot_size[1] * rows))
    if title is not None:
        fig.suptitle(title)
    if y_labels is None:
        y_labels = ['Force in x-direction [N]',
                    'Force in y-direction [N]',
                    'Force in z-direction [N]',
                    'Moment around x-axis [Nm]',
                    'Moment around y-axis [Nm]',
                    'Moment around z-axis [Nm]',
                    'Bimoment [Nm^2]']
    for i in range(num_plots):
        ax = axarr[i // cols, i % cols]
        for processor, load_case_data in processor_dict.items():
            ax.plot(load_case_data[:, 0].flatten(), load_case_data[:, i + 1].flatten())
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_labels[i])
        ax.grid()
        ax.legend(legend)

    # Save and show figure
    _save_and_show(fig, **kwargs)
