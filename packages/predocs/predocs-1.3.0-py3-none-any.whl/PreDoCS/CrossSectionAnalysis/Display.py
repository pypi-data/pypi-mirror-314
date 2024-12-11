"""
This file contains functions for displaying cross sections and values depending of the cross section elements (element strain, element stress).

Global kwargs:
    file
        If not None, the file where to save the figure.
    show
        If True, the figure will be shown.
    x_label: str (default: 'x [m]')
        Label of the x-axis.
    y_label: str (default: 'y [m]')
        Label of the y-axis.
    coordinate_axis_length: float (default: 0.1)
        Length of the coordinate system axis.
    plot_element_ids: bool (default: False)
        True for plotting the id's of the elements.
    element_color: str (default: 'b')
        Color of the elements.
    plot_node_ids: bool (default: True)
        True for plotting the id's of the nodes.
    node_color: str (default: 'k')
        Color of the nodes.
    node_marker_size: float (default: 3)
        Maker size of the nodes.
    plot_direction_as_arrow: bool (default: False)
        True, if value direction is plotted as an arrow.
    scale_factor: float (default: 1.0)
        Scale factor for the element values.
    plot_value_numbers: bool (default: True)
        Plot the numbers of the values if True.
    arrow_color: str (default: 'b')
        Color of the arrows.
    hitch_distance: float (default: 0.02)
        Distance for the hitch.
    arrow_scale_factor: float (default: 2.0)
        Scale factor for the arrow to the element thickness.
    plot_mass_center: bool (default: True)
        True, if the mass center should be plotted.
    plot_elastic_center: bool (default: True)
        True, if the elastic center should be plotted.
    plot_principal_axis: bool (default: True)
        True, if the principal should be plotted.
    plot_shear_center: bool (default: True)
        True, if the shear center should be plotted.
    plot_shear_principal_axis: bool (default: True)
        True, if the shear principal should be plotted.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import math
from copy import copy
from typing import Optional, Tuple, Union

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

from PreDoCS.CrossSectionAnalysis.Interfaces import ICrossSectionProcessor
from PreDoCS.MaterialAnalysis.Shells import IsotropicShell, CompositeShell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.filters import modified_kwargs
from PreDoCS.util.geometry import transform_location_m
from PreDoCS.util.vector import Vector
from PreDoCS.util.data import make_hash

log = get_module_logger(__name__)

try:
    from lightworks.mechana.skins.metal import Sheet as Sheet_lw
    from lightworks.mechana.skins.composite import Laminate as Laminate_lw
    from lightworks.mechana.skins.composite import LaminationParameter as LaminationParameter_lw
except ImportError:
    log.info('Modul lightworks.mechana not found. Material world VCP can not be used.')
    Sheet_lw = None
    Laminate_lw = None
    LaminationParameter_lw = None

# Allowed savefig args
savefig_args = [
    'transparent', 'dpi', 'format', 'metadata', 'bbox_inches', 'pad_inches', 'facecolor', 'edgecolor', 'backend',
]


def _save_and_show(fig, file: Optional[str] = None, show: bool = False, **kwargs):
    """
    Saves and/or shows figure.

    Parameters
    ----------
    fig
        The matplotlib figure.
    file
        If not None, the file where to save the figure.
    show
        If True, the figure will be shown.
    """
    if file:
        fig.tight_layout()
        plt.savefig(file, **{k: v for k, v in kwargs.items() if k in savefig_args})
        plt.close()

    if show:
        fig.show()


def plot_discreet_geometry(discreet_geometry, **kwargs):
    """
    Plots a cross section with elastic and shear center and the principal axis.
    
    Parameters
    ----------
    discreet_geometry: DiscreetCrossSectionGeometry
        The cross section to plot.
    file: str
        File, where to save the plot, otherwise no saving.
    title: str (default: 'Cross section')
        Title of the plot.
    cross_section_size: (float, float) (default: (5, 3))
        Size of the cross section in inches.
    """
    # Arguments
    cross_section_size = kwargs['cross_section_size'] if 'cross_section_size' in kwargs else (5, 3)
    title = kwargs['title'] if 'title' in kwargs else 'Cross section'
    
    fig, ax = plt.subplots(figsize=cross_section_size)
    if title is not None:
        fig.suptitle(title)
    _setup_axes(ax, **modified_kwargs(kwargs, title=None))
    _plot_discreet_geometry(ax, discreet_geometry, **kwargs)

    # Save and show figure
    _save_and_show(fig, **kwargs)


def plot_cross_section(cross_section, highlight_material_distribution=False, plot_layup=False,
                       node_texts=None, node_texts_color='k', element_texts=None, element_texts_color='k', **kwargs):
    """
    Plots a cross section with elastic and shear center and the principal axis.
    
    Parameters
    ----------
    cross_section: ICrossSectionProcessor
        The cross section to plot.
    highlight_material_distribution: bool (default: False)
        True for highlighting the material distribution.
    plot_layup: bool (default: False)
        If True, the layup of the segments is plotted in an additional plot.
        highlight_material_distribution must be True for this.
    file: str
        File, where to save the plot. No for no saving.
    title: str (default: 'Cross section')
        Title of the plot.
    cross_section_size: (float, float) (default: (5, 3))
        Size of the cross section in inches.
    element_colors: list(str)
        List of colors for the different element materials.
    material_colors: list(str)
        List of colors for the different base materials.
    node_texts: dict(INode, str) (default: None)
        Node texts.
    node_texts_color: str (default: 'k')
        Color of the node texts.
    element_texts: dict(IElement, str) (default: None)
        Element texts.
    element_texts_color: str (default: 'k')
        Color of the element texts.
    """
    # Arguments
    cross_section_size = kwargs['cross_section_size'] if 'cross_section_size' in kwargs else (5, 3)
    title = kwargs.get('title', None)

    ax2 = None
    if 'fig' in kwargs and 'ax' in kwargs:
        fig = kwargs.pop('fig')
        ax1 = kwargs.pop('ax')
        if highlight_material_distribution and plot_layup:
            ax1, ax2 = ax1
    else:
        if highlight_material_distribution and plot_layup:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=cross_section_size)
        else:
            fig, ax1 = plt.subplots(figsize=cross_section_size)

    if title is not None:
        fig.suptitle(title)

    _setup_axes(ax1, **modified_kwargs(kwargs, title=None))
    _plot_cross_section_coordinate_systems(ax1, cross_section, **kwargs)

    if highlight_material_distribution:
        _plot_materials(ax1, cross_section.discreet_geometry, ax2=ax2, **kwargs)
    else:
        _plot_discreet_geometry(ax1, cross_section.discreet_geometry, **kwargs)

    if node_texts is not None:
        for n, t in node_texts.items():
            ax1.text(n.position.x, n.position.y, t, color=node_texts_color)

    if element_texts is not None:
        for e, t in element_texts.items():
            ax1.text(e.position.x, e.position.y, t, color=element_texts_color)

    ax1.autoscale()

    # Save and show figure
    _save_and_show(fig, **kwargs)


def plot_cross_section_cells(cross_section, **kwargs):
    """
    Plots the cells of a cross section.
    
    Parameters
    ----------
    cross_section: ICrossSectionProcessor
        The cross section to plot.
    plot_cut_nodes: bool (default: True)
        True for plotting nodes.
    file: str
        File, where to save the plot. No for no saving.
    title: str (default: 'Cells')
        Title of the plot.
    cross_section_size: (float, float) (default: (5, 3))
        Size of the cross section in inches.
    """
    # Arguments
    cross_section_size = kwargs['cross_section_size'] if 'cross_section_size' in kwargs else (5, 3)
    title = kwargs['title'] if 'title' in kwargs else 'Cells'
    
    num_cells = len(cross_section.discreet_geometry.cells)
    cols = math.ceil(math.sqrt(num_cells))
    rows = math.ceil(num_cells / cols)
    fig, axarr = plt.subplots(rows, cols, sharex=True, sharey=True, squeeze=False,
                              figsize=(cross_section_size[0]*cols, cross_section_size[1]*rows))
    if title is not None:
        fig.suptitle(title)
    for i in range(num_cells):
        cell = cross_section.discreet_geometry.cells[i]
        ax = axarr[i // cols, i % cols]
        _setup_axes(ax, **modified_kwargs(kwargs, shared_axes=True, title='Cell ' + str(i)))
        _plot_cross_section_coordinate_systems(ax, cross_section, **kwargs)
        _plot_discreet_geometry(ax, cross_section.discreet_geometry, **kwargs)
        _plot_cell(ax, cell, **kwargs)

    # Save and show figure
    _save_and_show(fig, **kwargs)


def plot_materials(discreet_geometry, plot_layup=True, **kwargs):
    """
    Plots the material distribution of a cross section.
    
    Parameters
    ----------
    discreet_geometry: DiscreetCrossSectionGeometry
        The cross section to plot.
    plot_layup: bool (default: True)
        If True, the layup of the segments is plotted in an additional plot.
    file: str
        File, where to save the plot. No for no saving.
    title: str (default: 'Material distribution')
        Title of the plot.
    cross_section_size: (float, float) (default: (5, 3))
        Size of the cross section in inches.
    element_colors: list(str)
        List of colors for the different element materials.
    material_colors: list(str)
        List of colors for the different base materials.
    """
    # Arguments
    cross_section_size = kwargs['cross_section_size'] if 'cross_section_size' in kwargs else (5, 3)
    title = kwargs.get('title', None)

    ax2 = None
    if plot_layup:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=cross_section_size)
    else:
        fig, ax1 = plt.subplots(figsize=cross_section_size)

    if title is not None:
        fig.suptitle(title)

    _setup_axes(ax1, **modified_kwargs(kwargs, title=None))
    _plot_materials(ax1, discreet_geometry, ax2=ax2, **kwargs)

    ax1.autoscale()

    # Save and show figure
    _save_and_show(fig, **kwargs)


unit_conversion_dict = {
    'Pa': ('MPa', 1e-6),
    'N/m': ('N/mm', 1e-3),
    'm': ('mm', 1e3),
}


def get_unit_conversion(scale_unit: str) -> tuple[str, float]:
    # Convert units
    scale_unit_new = scale_unit
    value_scale_unit_factor = 1
    if scale_unit in unit_conversion_dict.keys():
        scale_unit_new, value_scale_unit_factor = unit_conversion_dict[scale_unit]
    return scale_unit_new, value_scale_unit_factor


def plot_cross_section_element_values(cross_section, value_dict, values_are_functions=False, plot_value_scale=False,
                                      scale_unit='-', scale_length=None, scale_color='k',
                                      scale_position: Optional[Tuple[float, float]] = None, cog: Vector = None,
                                      scale_factor: Optional[float] = None, **kwargs):
    """
    Plots a cross section with values for each element.
    
    Parameters
    ----------
    cross_section: ICrossSectionProcessor or DiscreetCrossSectionGeometry
        The cross section or discreet geometry to plot.
    value_dict: dict(IElement, dtpye)
        The values of the elements.
    values_are_functions: bool (default: False)
        True, if the element values are functions of the element contur coordinate.
    plot_value_scale: bool (default: False)
        Plot a scale for the element values if True.process_comparison_sets
    scale_unit: str (default: '-')
        String of the scale unit.
    scale_length: float (default: None)
        The max length of the scale. If None, the max value is the max scale length.
    scale_color: str (default: 'k')
        Color of the scale.
    scale_position
        The position of the scale.
    cog: Vector (default: None)
        If cross_section is a DiscreetCrossSectionGeometry, the CoG of the cross section must be given additionally.
    scale_factor
        The scale factor of the value bars (value bar height per value).
        If None, it is calculated that the maximum height of the value bars is max_display_value.
    max_display_value: float (default: 1)
        Max height of the value bar.
    file: str
        File, where to save the plot. No for no saving.
    title: str (default: 'Element values')
        Title of the plot.
    cross_section_size: (float, float) (default: (5, 3))
        Size of the cross section in inches.
    """
    # Arguments
    cross_section_size = kwargs['cross_section_size'] if 'cross_section_size' in kwargs else (5, 3)
    title = kwargs['title'] if 'title' in kwargs else 'Element values'
    max_display_value = kwargs['max_display_value'] if 'max_display_value' in kwargs else 1.

    # Convert units
    scale_unit, value_scale_unit_factor = get_unit_conversion(scale_unit)

    if isinstance(cross_section, ICrossSectionProcessor):
        discreet_geometry = cross_section.discreet_geometry
        cog = cross_section.CoG
    else:
        discreet_geometry = cross_section
        cross_section = None
        assert cog is not None

    if 'fig' in kwargs and 'ax' in kwargs:
        fig = kwargs.pop('fig')
        ax = kwargs.pop('ax')
    else:
        fig, ax = plt.subplots(figsize=cross_section_size)
    if title is not None:
        fig.suptitle(title)
    _setup_axes(ax, **modified_kwargs(kwargs, title=None))
    if cross_section:
        _plot_cross_section_coordinate_systems(ax, cross_section, **kwargs)
    _plot_discreet_geometry(ax, discreet_geometry, **kwargs)

    if values_are_functions:
        element_reference_length_dict = discreet_geometry.element_reference_length_dict
        sample_values = [fun(0) for e, fun in value_dict.items()] + \
                        [fun(element_reference_length_dict[e]) for e, fun in value_dict.items()]
    else:
        sample_values = list(value_dict.values())

    max_value = np.max(np.abs(sample_values))
    if scale_factor is None:
        if max_value == 0:
            # Empty plot
            scale_factor = 1
        else:
            scale_factor = max_display_value / max_value

    # Element value directions
    swap_element_value_direction_list = [e for e in discreet_geometry.elements
                                         if np.dot(e.thickness_vector, (e.position - cog)) < 0]

    _plot_element_values(discreet_geometry, ax, value_dict, values_are_functions, swap_element_value_direction_list,
                         **modified_kwargs(kwargs, scale_factor=scale_factor, value_scale_unit_factor=value_scale_unit_factor))

    if plot_value_scale:
        scale_max_value = max_value if scale_length is None else scale_length / scale_factor / value_scale_unit_factor
        if scale_max_value == 0:
            # Empty plot
            scale_max_value = 0.1
        line_value = 10**round(np.log10(scale_max_value)-0.5)
        line_length = line_value * scale_factor
        end_line_length = 0.2 * line_length

        if scale_position is None:
            x0, xm = ax.get_xbound()
            y0, ym = ax.get_ybound()
            x_0 = x0
            y_0 = y0
        else:
            x_0 = scale_position[0]
            y_0 = scale_position[1]

        y_factor = -1 if kwargs.get('y_axis_mirrored', False) else 1
        ax.hlines(y_0, x_0, x_0 + line_length, colors=scale_color)
        ax.vlines(x_0, y_0 - end_line_length, y_0 + end_line_length, colors=scale_color)
        ax.vlines(x_0 + 0.25 * line_length, y_0 - 0.25 * end_line_length, y_0 + 0.25 * end_line_length, colors=scale_color)
        ax.vlines(x_0 + 0.5 * line_length, y_0 - 0.5 * end_line_length, y_0 + 0.5 * end_line_length, colors=scale_color)
        ax.vlines(x_0 + 0.75 * line_length, y_0 - 0.25 * end_line_length, y_0 + 0.25 * end_line_length, colors=scale_color)
        ax.vlines(x_0 + line_length, y_0 - end_line_length, y_0 + end_line_length, colors=scale_color)
        ax.text(x_0 + line_length / 2, y_0 + 1.1 * end_line_length * y_factor, '{:.0E} [{}]'.format(line_value * value_scale_unit_factor, scale_unit),
                ha='center', va='bottom')

    # Save and show figure
    _save_and_show(fig, **kwargs)


def _plot_materials(
        ax1,
        discreet_geometry,
        element_colors: Union[list, str] = 'tab10',
        material_colors: Union[list, str] = 'tab10',
        ax2=None,
        plot_nodes: bool = True,
        display_element_numbers_directly: bool = False,
        ignore_shell_attrs: list[str] = None,
        ignore_ply_attrs: list[str] = None,
        **kwargs
):
    """
    Plots the material distribution of a cross section.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    discreet_geometry: DiscreetCrossSectionGeometry
        The cross section to plot.
    element_colors: list(str) or str
        List of colors for the different element materials or matplotlib colormap name.
    material_colors: list(str) or str
        List of colors for the different base materials or matplotlib colormap name.
    plot_nodes
        True, if the nodes of the cross section geometry should be plotted.
    display_element_numbers_directly
        If True, the element numbers ar displayed at the elements, if False color coded with a legend.
    ignore_shell_attrs
        Ignore the given attributes of the shell objects.
    ignore_ply_attrs
        Ignore the given attributes of the ply objects.
    """
    legend_kwargs = dict(loc='lower center', bbox_to_anchor=(-0.05, 1.02, 1.1, 0))

    if ignore_shell_attrs is None:
        ignore_shell_attrs = []
    if ignore_ply_attrs is None:
        ignore_ply_attrs = []

    use_material_hashes = len(ignore_shell_attrs) != 0 and len(ignore_ply_attrs) != 0

    # Collect materials
    if use_material_hashes:
        element_shell_hash_dict = {}
        shell_hash_material_dict = {}
        material_shell_hash_dict = {}
        for e in discreet_geometry.elements:
            shell_dict = copy(e.shell.__dict__)
            for attr in ignore_shell_attrs:
                shell_dict.pop(attr, None)
            if hasattr(e.shell, '_layup'):
                shell_dict['_layup'] = []
                for ply in e.shell.layup:
                    ply_dict = copy(ply.__dict__)
                    ply_dict['_material'] = ply_dict['_material'].name
                    for attr in ignore_ply_attrs:
                        ply_dict.pop(attr, None)
                    shell_dict['_layup'].append(ply_dict)
            e_hash = make_hash(shell_dict)
            shell_hash_material_dict[e_hash] = e.shell
            material_shell_hash_dict[e.shell] = e_hash
            element_shell_hash_dict[e] = e_hash
        element_materials = list(shell_hash_material_dict.values())
    else:
        element_materials = list({e.shell for e in discreet_geometry.elements})

    base_materials = []
    for element_material in element_materials:
        # element_materials.append(element_material)
        if isinstance(element_material, IsotropicShell) or \
                (Sheet_lw is not None and isinstance(element_material, Sheet_lw)):
            # Sheet
            base_materials.append(element_material)
        elif isinstance(element_material, CompositeShell):
            # Composite
            base_materials.extend([m.material for m in element_material.layup])
        elif Laminate_lw is not None and isinstance(element_material, Laminate_lw):
            # Composite
            base_materials.extend([m.material for m in element_material.layers])
        elif LaminationParameter_lw is not None and isinstance(element_material, LaminationParameter_lw):
            # Composite
            base_materials.append(element_material.material)
        else:
            raise RuntimeError('Material type "{}" not defined'.format(str(type(element_material))))
    base_materials = list({m.name for m in base_materials})
    # Sort
    element_materials = sorted(element_materials, key=lambda m: m.name)
    base_materials = sorted(base_materials)
    # Set names
    element_materials = [(i + 1, m) for i, m in enumerate(element_materials)]  # (name, material)

    # print(element_materials)
    # print(base_materials)

    # Colors
    element_colors = get_colors(element_colors, len(element_materials))
    material_colors = get_colors(material_colors, len(base_materials))

    # Plot elements with material color
    legend_handles = []
    if plot_nodes:
        _plot_nodes(ax1, discreet_geometry.nodes, **kwargs)
    for i, (materials_name, material) in enumerate(element_materials):
        color = element_colors[i]
        if use_material_hashes:
            material_hash = material_shell_hash_dict[material]
            elements = [e for e in discreet_geometry.elements if element_shell_hash_dict[e] == material_hash]
        else:
            elements = [e for e in discreet_geometry.elements if e.shell == material]
        _plot_elements(ax1, elements, **modified_kwargs(kwargs, element_color=color))
        if display_element_numbers_directly:
            mean_pos = np.mean([e.position for e in elements], axis=0)
            ax1.text(mean_pos[0], mean_pos[1], str(materials_name))
        else:
            legend_handles.append(mlines.Line2D([], [], color=color, marker='s', linestyle='None',
                                                markersize=10, label=get_valid_legend_str(materials_name)))
    if not display_element_numbers_directly:
        ax1.legend(handles=legend_handles, mode='expand', ncol=6, **legend_kwargs)

    # Plot thickness direction
    _plot_thickness_direction(ax1, discreet_geometry, **kwargs)

    # Plot layup
    if ax2 is not None:
        ax2.grid(linestyle='--', linewidth='0.5', color='silver')
        for i, (element_materials_name, element_material) in enumerate(element_materials):
            # color = element_colors[i]
            if isinstance(element_material, IsotropicShell) or \
                    (Sheet_lw is not None and isinstance(element_material, Sheet_lw)):
                # Sheet
                layup_base_materials = [element_material]
                layup_thickness = [element_material.thickness]
            elif isinstance(element_material, CompositeShell):
                # Composite
                layup_base_materials = [m.material for m in element_material.layup]
                layup_thickness = [m.thickness for m in element_material.layup]
            elif Laminate_lw is not None and isinstance(element_material, Laminate_lw):
                # Composite
                layup_base_materials = [m.material for m in element_material.layers]
                layup_thickness = [m.thickness for m in element_material.layers]
            elif LaminationParameter_lw is not None and isinstance(element_material, LaminationParameter_lw):
                # Composite
                layup_base_materials = [element_material.material]
                layup_thickness = [element_material.thickness]
            else:
                raise RuntimeError('Material type "{}" not defined'.format(str(type(element_material))))

            z = 0
            for base_material, thickness in zip(layup_base_materials, layup_thickness):
                thickness *= 1e3  # m -> mm
                ax2.bar(element_materials_name, thickness, bottom=z,
                        # label=base_material.name,
                        color=material_colors[base_materials.index(base_material.name)])  # ,
                # tick_label=element_materials_name)
                z += thickness

        legend_handles = []
        for i, base_material in enumerate(base_materials):
            color = material_colors[i]
            legend_handles.append(mlines.Line2D([], [], color=color, marker='s', linestyle='None',
                                                markersize=10, label=get_valid_legend_str(base_material)))
        ax2.legend(handles=legend_handles, mode='expand', ncol=2, **legend_kwargs)
        ax2.set_ylabel('t [mm]')


def get_valid_legend_str(s: str) -> str:
    """Legend labels are not allowed to start with an underscore."""
    s = str(s)
    return (' ' + s) if s[0] == '_' else s


def _setup_axes(
        ax,
        shared_axes: bool = False,
        x_axis_mirrored: bool = False,
        y_axis_mirrored: bool = False,
        title: Optional[str] = None,
        x_label: str = '$x$ [m]',
        y_label: str = '$y$ [m]',
        x_lim: Optional[Tuple[float, float]] = None,
        y_lim: Optional[Tuple[float, float]] = None,
        **kwargs,
):
    """
    Labels the axes of a plot and sets the axis ratio.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    shared_axes
        True, if the axes should be shared.
    x_axis_mirrored
        True, if the x-axis should be mirrored.
    y_axis_mirrored
        True, if the y-axis should be mirrored.
    title
        Title of the plot.
    x_label
        Label of the x-axis.
    y_label
        Label of the y-axis.
    x_lim
        The x-axis limits, None for autoscale.
    y_lim
        The y-axis limits, None for autoscale.
    """
    if title is not None:
        ax.set_title(title)
    ax.set_xlabel(x_label)
    if x_axis_mirrored:
        ax.invert_xaxis()
    if y_axis_mirrored:
        ax.invert_yaxis()
    ax.set_ylabel(y_label)
    ax.set_aspect('equal')
    if not shared_axes:
        ax.set_adjustable('datalim')
    ax.autoscale()
    if x_lim is not None:
        ax.set_xlim(x_lim)
    if y_lim is not None:
        ax.set_ylim(y_lim)
    ax.grid(linestyle='--', linewidth='0.5', color='silver')


def _plot_thickness_direction(
        ax,
        discreet_geometry,
        thickness_direction_arrow_length: float = None,
        thickness_direction_arrow_stride: int = 1,
        thickness_direction_arrow_color='r',
        thickness_direction_arrow_width: float = 1e-2,
        **kwargs,
):
    if thickness_direction_arrow_length is not None:
        for i, element in enumerate(discreet_geometry.elements):
            if i % thickness_direction_arrow_stride == 0:
                pos = element.position
                arrow_dir = element.thickness_vector.normalised * thickness_direction_arrow_length
                ax.arrow(
                    pos.x, pos.y,
                    arrow_dir.x, arrow_dir.y,
                    color=thickness_direction_arrow_color,
                    width=thickness_direction_arrow_width,
                    length_includes_head=True,
                )


def _plot_discreet_geometry(ax, discreet_geometry, **kwargs):
    """
    Plots a discreet geometry.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    discreet_geometry: DiscreetCrossSectionGeometry
        The discreet geometry to plot.
    thickness_direction_arrow_length
        If not None, the thickness direction of the elements is plotted.
    thickness_direction_arrow_stride
        Stride to plot arrows of the thickness direction.
    """
    plot_nodes = kwargs.get('plot_nodes', True)
    _plot_elements(ax, discreet_geometry.elements, **kwargs)
    if plot_nodes:
        _plot_nodes(ax, discreet_geometry.nodes, **kwargs)

    # Plot thickness direction
    _plot_thickness_direction(ax, discreet_geometry, **kwargs)


def _plot_coordinate_system(ax, atm, color, plot_axis=False, axis_length=1., x_label='x', y_label='y'):
    """
    Plots a coordinate system from an augmented transformation matrix.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    atm: numpy.ndarray
        Augmented transformation matrix of the coordinate system to plot.
    color: str
        Color of the coordinate system.
    plot_axis: bool (default: False)
        If True, the coordinate system axis are plotted, otherwise only the origin.
    axis_length: float (default: 1.)
        The length of the axis.
    x_label: str (default: 'x')
        Label of the x-axis.
    y_label: str (default: 'y')
        Label of the y-axis.
    """
    origin = transform_location_m(atm, Vector([0., 0.]))
    if plot_axis:
        x_axis_profile = axis_length * Vector([1., 0.])
        y_axis_profile = axis_length * Vector([0., 1.])
        x_axis = transform_location_m(atm, x_axis_profile)
        y_axis = transform_location_m(atm, y_axis_profile)
        ax.plot([origin.x, x_axis.x], [origin.y, x_axis.y], color)
        ax.text(x_axis.x, x_axis.y, x_label, color=color)
        ax.plot([origin.x, y_axis.x], [origin.y, y_axis.y], color)
        ax.text(y_axis.x, y_axis.y, y_label, color=color)


def _plot_cross_section_coordinate_systems(ax, cross_section, **kwargs):
    """
    Plots the elastic and shear center and the principal axis.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    cross_section: ICrossSectionProcessor
        The cross section to plot.
    coordinate_axis_length: float (default: 0.1)
        Length of the coordinate system axis.
    """
    # Arguments
    coordinate_axis_length = kwargs.get('coordinate_axis_length', 0.1)
    cog_color = 'k'
    ec_color = 'darkorange'
    sc_color = 'm'
    plot_mass_center = kwargs.get('plot_mass_center', True)
    plot_elastic_center = kwargs.get('plot_elastic_center', True)
    plot_principal_axis = kwargs.get('plot_principal_axis', True)
    plot_shear_center = kwargs.get('plot_shear_center', True)
    plot_shear_principal_axis = kwargs.get('plot_shear_principal_axis', True)

    # Mass center
    if plot_mass_center:
        ax.plot([cross_section.CoG.x], [cross_section.CoG.y], 'D', label='CoG', color=cog_color, fillstyle='right')

    # Elastic center / coordinate system
    if plot_elastic_center:
        ec = cross_section.elastic_center
        ax.plot([ec.x], [ec.y], 'o', label='EC', color=ec_color)
        _plot_coordinate_system(ax, cross_section.transform_principal_axis_to_cross_section_atm, ec_color,
                                plot_axis=plot_principal_axis, axis_length=coordinate_axis_length,
                                x_label='$X_b$', y_label='$Y_b$')

    # Shear center / coordinate system
    if plot_shear_center:
        sc = cross_section.shear_center
        ax.plot([sc.x], [sc.y], '+', label='SC', color=sc_color)
        if hasattr(cross_section, 'transform_shear_principal_axis_to_cross_section_atm'):
            _plot_coordinate_system(ax, cross_section._transform_shear_principal_axis_to_cross_section_atm, sc_color,
                                    plot_axis=plot_shear_principal_axis, axis_length=coordinate_axis_length,
                                    x_label='$X_s$', y_label='$Y_s$')

    ax.legend()


def _plot_cell(ax, cell, **kwargs):
    """
    Plots a cell of a discreet geometry.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    cell: Cell
        The cell to plot.
    plot_cut_nodes: bool (default: True)
        True for plotting nodes.
    """
    # Arguments
    plot_cut_nodes = kwargs['plot_cut_nodes'] if 'plot_cut_nodes' in kwargs else True
    
    _plot_elements(ax, cell.elements, **modified_kwargs(kwargs, element_color='r'))
    if plot_cut_nodes and cell.is_cutted:
        _plot_nodes(ax, [cell.cut_node], **modified_kwargs(kwargs, plot_node_ids=True, node_color='lime'))


def _plot_elements(ax, elements, elements_scale_factor: float = 1., **kwargs):
    """
    Plots a list of elements.
   
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    elements: list(IElement)
        The elements.
    plot_element_ids: bool (default: False)
        True for plotting the id's of the elements.
    plot_segment_ids: bool (default: False)
        True for plotting the id's of the segments.
    plot_component_ids: bool (default: False)
        True for plotting the id's of the components.
    element_color: str (default: 'b')
        Color of the elements.
    element_as_arrow: bool (default: False)
        True for plotting the elements as arrows in element direction, otherwise as simple rectangles.
    elements_scale_factor
        Scale factor for plotting the elements.
    """
    # Arguments
    plot_element_ids = kwargs.get('plot_element_ids', False)
    plot_segment_ids = kwargs.get('plot_segment_ids', False)
    plot_component_ids = kwargs.get('plot_component_ids', False)
    element_color = kwargs.get('element_color', 'b')
    element_as_arrow = kwargs.get('element_as_arrow', False)
    ax_margins = kwargs.get('ax_margins', 0.05)
    
    patches = []
    for element in elements:
        if element_as_arrow:
            element_position = element.node1.position + element.thickness_vector * element.component.midsurface_offset
            element_length = element.length_vector
            ax.arrow(element_position.x, element_position.y, element_length.x, element_length.y,
                     color=element_color, width=element.thickness, length_includes_head=True)
        else:
            p1 = element.node1.position + element.thickness_vector * element.component.midsurface_offset - element.thickness_vector/2
            p2 = p1 + element.thickness_vector * elements_scale_factor
            p3 = p2 + element.length_vector
            p4 = p3 - element.thickness_vector * elements_scale_factor
            patches.append(Polygon([p1, p2, p3, p4], closed=True, edgecolor=None))
        if plot_element_ids:
            ax.text(element.position.x, element.position.y, str(element.id), color='gold')

    if plot_segment_ids:
        segments_dict = {}
        for element in elements:
            if element.segment in segments_dict:
                segments_dict[element.segment].append(element)
            else:
                segments_dict[element.segment] = [element]
        segment_positions = {s: Vector(np.mean(np.array([e.position for e in e_list]), axis=0))
                             for s, e_list in segments_dict.items()}
        for segment, position in segment_positions.items():
            ax.text(position.x, position.y, str(segment.id if segment else segment), color='green')

    if plot_component_ids:
        components_dict = {}
        for element in elements:
            if element.component in components_dict:
                components_dict[element.component].append(element)
            else:
                components_dict[element.component] = [element]
        component_positions = {s: Vector(np.mean(np.array([e.position for e in e_list]), axis=0))
                             for s, e_list in components_dict.items()}
        for component, position in component_positions.items():
            ax.text(position.x, position.y, str(component.id if component else component), color='black')

    if not element_as_arrow:
        p = PatchCollection(patches)
        p.set_color(element_color)
        ax.add_collection(p)

    ax.margins(ax_margins)


def _plot_nodes(ax, nodes, **kwargs):
    """
    Plots a list of nodes.
   
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    nodes: list(INode)
        The nodes to plot.
    plot_node_ids: bool (default: True)
        True for plotting the id's of the nodes.
    node_color: str (default: 'k')
        Color of the nodes.
    node_marker_size: float (default: 3)
        Maker size of the nodes.
    """
    # Arguments
    plot_node_ids = kwargs['plot_node_ids'] if 'plot_node_ids' in kwargs else False
    node_color = kwargs['node_color'] if 'node_color' in kwargs else 'k'
    node_marker_size = kwargs['node_marker_size'] if 'node_marker_size' in kwargs else 3
    
    for node in nodes:
        ax.plot([node.position.x], [node.position.y], 'o', markersize=node_marker_size, color=node_color)
        if plot_node_ids:
            ax.text(node.position.x, node.position.y, str(node.id), color='m')


def _plot_element_values(discreet_geometry, ax, value_dict, values_are_functions=False, swap_element_value_direction_list=[], **kwargs):
    """
    Plots values for each element.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    value_dict: dict(IElement, float)
        The values of the elements.
    values_are_functions: bool (default: False)
        True, if the element values are functions of the contur coordinate.
    elements_to_plot: list(IElement) (default: None)
        List of elements, for which the values are plotted. None for all elements in value_dict.
    swap_element_value_direction_list: list(IElement) (default: [])
        List of elements, of which the value bars are plotted to the negative thickness direction
        instead of the positive thickness direction.
    """
    # Arguments
    elements_to_plot = kwargs.get('elements_to_plot', list(value_dict.keys()))
    ax_margins = kwargs.get('ax_margins', 0.05)

    for element in elements_to_plot:
        _plot_element_value(discreet_geometry, ax, element, value_dict[element], values_are_functions,
            swap_element_value_direction=(True if element in swap_element_value_direction_list else False), **kwargs)

    ax.margins(ax_margins)


def _plot_element_value(discreet_geometry, ax, element, value, value_is_function=False, swap_element_value_direction=False, **kwargs):
    """
    Plots a value bar for an element.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes, where to plot.
    element: IElement
        The element.
    value: float
        The values of the element.
    value_is_function: bool (default: False)
        True, if the element value is a function of the contur coordinate.
    swap_element_value_direction: bool (default: False)
        True if the value bars are plotted to the negative thickness direction
        instead of the positive thickness direction.
    plot_direction_as_arrow: bool (default: False)
        True, if value direction is plotted as an arrow.
    scale_factor: float (default: 1.0)
        Scale factor for the element values.
    plot_value_numbers: bool (default: True)
        Plot the numbers of the values if True.
    arrow_color: str (default: 'b')
        Color of the arrows.
    hitch_distance: float (default: 0.02)
        Distance for the hitch.
    arrow_scale_factor: float (default: 2.0)
        Scale factor for the arrow to the element thickness.
    """
    # Arguments
    plot_direction_as_arrow = kwargs['plot_direction_as_arrow'] if 'plot_direction_as_arrow' in kwargs else False
    scale_factor = kwargs['scale_factor'] if 'scale_factor' in kwargs else 1.
    plot_value_numbers = kwargs['plot_value_numbers'] if 'plot_value_numbers' in kwargs else True
    arrow_color = kwargs['arrow_color'] if 'arrow_color' in kwargs else 'b'
    hitch_distance = kwargs['hitch_distance'] if 'hitch_distance' in kwargs else 0.02
    arrow_scale_factor = kwargs['arrow_scale_factor'] if 'arrow_scale_factor' in kwargs else 2.
    value_scale_unit_factor = kwargs.get('value_scale_unit_factor', 1)

    l_ref = discreet_geometry.element_reference_length_dict[element]
    if swap_element_value_direction:
        scale_factor *= -1.

    if value_is_function:
        mean_value = value(l_ref / 2.)
        value_function = value
    else:
        mean_value = value
        value_function = lambda s: value

    if plot_direction_as_arrow and mean_value != 0:
        # Plot arrow
        if mean_value > 0:
            start_pos = element.node1.position + element.thickness_vector * element.component.midsurface_offset
            ax.arrow(start_pos.x, start_pos.y,
                     element.length_vector.x, element.length_vector.y,
                     color=arrow_color, width=element.thickness*arrow_scale_factor, length_includes_head=True)
        else:
            start_pos = element.node2.position + element.thickness_vector * element.component.midsurface_offset
            ax.arrow(start_pos.x, start_pos.y,
                     -element.length_vector.x, -element.length_vector.y,
                     color=arrow_color, width=element.thickness*arrow_scale_factor, length_includes_head=True)

    # Value hitch
    positive_value_stile = 'g'
    negative_value_stile = 'r'
    x = []
    y = []
    hitch_lines = []
    hitch_colors = []
    num_hitch_lines = max(math.ceil(l_ref / hitch_distance) + 1, 2)
    for s in np.linspace(0., l_ref, num_hitch_lines):
        plot_value = value_function(s)
        s_pos = (element.node1.position + element.thickness_vector * element.component.midsurface_offset - element.thickness_vector/2) + element.length_vector.normalised * s
        t_pos = element.thickness_vector.normalised * abs(plot_value) * scale_factor
        p = s_pos + t_pos

        x.append(p.x)
        y.append(p.y)

        hitch_lines.append(((s_pos.x, s_pos.y), (p.x, p.y)))
        hitch_colors.append(positive_value_stile
                            if (plot_value >= 0) or plot_direction_as_arrow else negative_value_stile)

    # Values
    value_lines = []
    x_prev = x[0]
    y_prev = y[0]
    for i in range(len(x)-1):
        x_cur = x[i+1]
        y_cur = y[i+1]
        value_lines.append(((x_prev, y_prev), (x_cur, y_cur)))
        x_prev = x_cur
        y_prev = y_cur
    ax.add_collection(mc.LineCollection(value_lines, colors=hitch_colors[0:-1]))

    # Hitch
    ax.add_collection(mc.LineCollection(hitch_lines, colors=hitch_colors, linewidths=0.5))

    # Display value number
    if plot_value_numbers:
        if plot_direction_as_arrow:
            disp_value = abs(mean_value)
        else:
            disp_value = mean_value
        text_position = element.node1.position + element.length_vector / 2.\
                        + element.thickness_vector.normalised * abs(value_function(l_ref / 2.)) * scale_factor
        ax.text(text_position.x, text_position.y, '{:.2e}'.format(disp_value * value_scale_unit_factor), color='k')


def get_colors(colors, min_colors):
    if isinstance(colors, str):
        # From color map
        cmap = plt.get_cmap(colors)
        colors = cmap(range(cmap.N))
    if min_colors > len(colors):
        # Random colors, if colors is too short
        colors = [np.random.rand(3, ) for _ in range(min_colors)]
    return colors
