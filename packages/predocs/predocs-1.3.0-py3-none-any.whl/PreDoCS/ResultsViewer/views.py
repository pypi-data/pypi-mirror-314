#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import traceback
from abc import abstractmethod
from typing import Union

from PySide6.QtCore import Signal, Qt, QObject
from PySide6.QtWidgets import QComboBox, QCheckBox, QDoubleSpinBox, QFormLayout, QLabel, QVBoxLayout, QWidget, \
    QMessageBox

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from PreDoCS.CrossSectionAnalysis.Display import plot_cross_section
from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverBase


class Setting(QObject):

    value_changed = Signal()

    def __init__(self, widget_type, label, **kwargs):
        super(Setting, self).__init__()

        #self.name = name
        self.widget_type = widget_type
        self.label = label

        self._widget = widget_type()

        # Connect value changed
        if self.widget_type in [QComboBox]:
            self._widget.currentIndexChanged.connect(self._value_changed)
        elif self.widget_type in [QCheckBox]:
            self._widget.stateChanged.connect(self._value_changed)
        elif self.widget_type in [QDoubleSpinBox]:
            self._widget.valueChanged.connect(self._value_changed)
            self._widget.setMinimum(kwargs.get('min_value', 0))
            self._widget.setMaximum(kwargs.get('max_value', 1))
            self._widget.setSingleStep(kwargs.get('step', 0.1))
        else:
            raise ValueError(f'Unknown widget type {widget_type}')

        #self._value = None

    def clear(self):
        self._value = None
        self._widget.clear()

    def set_options(self, options: Union[list[str], dict[str, object]]):
        assert self.widget_type in [QComboBox]
        if isinstance(options, list):
            self._widget.addItems(options)
        elif isinstance(options, dict):
            for l, o in options.items():
                self._widget.addItem(l, o)
        else:
            raise RuntimeError()

    def set_value(self, value):
        if self.widget_type in [QComboBox]:
            raise RuntimeError()#self._widget.currentIndexChanged.connect(self._value_changed)
        elif self.widget_type in [QCheckBox]:
            assert isinstance(value, bool)
            self._widget.setCheckState(Qt.Checked if value else Qt.Unchecked)
        elif self.widget_type in [QDoubleSpinBox]:
            assert isinstance(value, float) or isinstance(value, int)
            self._widget.setValue(value)
        else:
            raise ValueError(f'Unknown widget type {self.widget_type}')

    def _value_changed(self):
        self.value_changed.emit()

    @property
    def widget(self):
        return self._widget

    @property
    def value(self):
        if self.widget_type in [QComboBox]:
            data = self._widget.currentData()
            if data is not None:
                return data
            else:
                return self._widget.currentText()
        elif self.widget_type in [QCheckBox]:
            return self._widget.checkState() == Qt.Checked
        elif self.widget_type in [QDoubleSpinBox]:
            return self._widget.value()
        else:
            raise ValueError(f'Unknown widget type {self.widget_type}')


class IView:
    def __init__(self, parent):
        self._valid_settings = False

        self.parent = parent
        self._settings = self._get_settings()

        # Settings
        self._settings_widget = QWidget()
        form_layout = QFormLayout(self._settings_widget)
        for i, (name, s) in enumerate(self._settings.items()):
            s.value_changed.connect(self.setting_changed)
            label = QLabel(self._settings_widget)
            label.setText(s.label)
            form_layout.setWidget(i, QFormLayout.LabelRole, label)
            form_layout.setWidget(i, QFormLayout.FieldRole, s.widget)

        # Plot
        self._plot_widget = QWidget()
        self.fig = Figure()
        self.view = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar2QT(self.view, self.parent)
        plot_layout = QVBoxLayout(self._plot_widget)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.view)

    def clear_view(self):
        _valid_settings = False

        # Controls
        for name, setting in self._settings.items():
            setting.clear()

        # View
        self.fig.clear()

    def init_view(self, solver: PreDoCS_SolverBase):
        self._valid_settings = False
        self.solver = solver

        self._init_view(solver)

        self._valid_settings = True
        self.update_plot()

    @property
    def settings_widget(self):
        return self._settings_widget

    @property
    def plot_widget(self):
        return self._plot_widget

    def setting_changed(self):
        if self._valid_settings:
            self.update_plot()

    def update_plot(self):
        try:
            self.fig.clf()  # Clear the canvas.

            self._update_plot()

            # Trigger the canvas to update and redraw.
            self.view.draw()
        except:
            QMessageBox.warning(self.plot_widget, 'Plotting Error', traceback.format_exc())

    @property
    @abstractmethod
    def title(self):
        pass

    @abstractmethod
    def _get_settings(self):
        pass

    @abstractmethod
    def _init_view(self, solver: PreDoCS_SolverBase):
        pass

    @abstractmethod
    def _update_plot(self):
        pass


class MaterialDistributionStateView(IView):
    def __init__(self, *args, **kwargs):
        super(MaterialDistributionStateView, self).__init__(*args, **kwargs)

    @property
    def title(self):
        return 'Material Distribution'

    def _get_settings(self):
        return {
            'cross_section': Setting(QComboBox, 'Cross Section'),
            'plot_layup': Setting(QCheckBox, 'Plot Layup?'),
            'display_element_numbers_directly': Setting(QCheckBox, 'Display Material Numbers directly?'),
            'element_colors': Setting(QComboBox, 'Colors'),
            'plot_nodes': Setting(QCheckBox, 'Plot Nodes?'),
            'plot_node_ids': Setting(QCheckBox, 'Plot Node IDs?'),
            'plot_element_ids': Setting(QCheckBox, 'Plot Element IDs?'),
            'coordinate_axis_length': Setting(QDoubleSpinBox, 'Coord. Sys. Axis Length', min_value=0, max_value=10, step=0.1),
            'y_axis_mirrored': Setting(QCheckBox, 'Y-axis mirrored?'),
        }

    def _init_view(self, solver: PreDoCS_SolverBase):
        self._settings['cross_section'].set_options(
            {f'{cs_processor.z_beam:.2f} m': i for i, cs_processor in enumerate(solver.cs_processors)}
        )
        self._settings['plot_layup'].set_value(True)
        self._settings['plot_nodes'].set_value(False)
        self._settings['plot_node_ids'].set_value(False)
        self._settings['plot_element_ids'].set_value(False)
        self._settings['display_element_numbers_directly'].set_value(True)
        self._settings['element_colors'].set_options(['tab20', 'tab10'])
        self._settings['coordinate_axis_length'].set_value(0.5)
        self._settings['y_axis_mirrored'].set_value(True)

    def _update_plot(self):
        settings = self._settings
        cs_idx = settings['cross_section'].value
        cs_processor = self.solver.cs_processors[cs_idx]
        axes = self.fig.subplots(1, 2 if settings['plot_layup'].value else 1)
        plot_cross_section(
            cs_processor,
            highlight_material_distribution=True,
            plot_layup=settings['plot_layup'].value,
            plot_nodes=settings['plot_nodes'].value,
            plot_node_ids=settings['plot_node_ids'].value,
            plot_element_ids=settings['plot_element_ids'].value,
            elements_scale_factor=1,
            element_colors=settings['element_colors'].value,#'tab20',
            coordinate_axis_length=settings['coordinate_axis_length'].value,
            display_element_numbers_directly=settings['display_element_numbers_directly'].value,
            y_axis_mirrored=settings['y_axis_mirrored'].value,
            fig=self.fig,
            ax=axes,
        )


class ElementLoadStateView(IView):
    def __init__(self, *args, **kwargs):
        super(ElementLoadStateView, self).__init__(*args, **kwargs)

    @property
    def title(self):
        return 'Element Load States'

    def _get_settings(self):
        return {
            'cross_section': Setting(QComboBox, 'Cross Section'),
            'load_case': Setting(QComboBox, 'Load Case'),
            'load_state_source': Setting(QComboBox, 'Load State Source'),
            'load_state_component': Setting(QComboBox, 'Load State Component'),
            'use_arrow': Setting(QCheckBox, 'Arrow?'),
            'arrow_scale_factor': Setting(QDoubleSpinBox, 'Arrow scale factor', min_value=0, max_value=10, step=0.1),
            'max_display_value': Setting(QDoubleSpinBox, 'Max Display Value', min_value=0, max_value=100, step=0.1),
            'plot_value_numbers': Setting(QCheckBox, 'Plot value numbers?'),
            'x_axis_mirrored': Setting(QCheckBox, 'X-axis mirrored?'),
            'y_axis_mirrored': Setting(QCheckBox, 'Y-axis mirrored?'),
            'plot_value_scale': Setting(QCheckBox, 'Plot value scale?'),
            'coordinate_axis_length': Setting(QDoubleSpinBox, 'CS-axis length', min_value=0, max_value=100, step=0.1),
        }

    def _init_view(self, solver: PreDoCS_SolverBase):
        self._settings['cross_section'].set_options(
            {f'{cs_processor.z_beam:.2f} m': i for i, cs_processor in enumerate(solver.cs_processors)}
        )
        self._settings['load_case'].set_options(solver.load_case_names)
        self._settings['load_state_source'].set_options(
            (['functions'] if solver.ctrl.calc_element_load_state_functions else []) +
            (['min', 'max'] if solver.ctrl.calc_element_load_state_min_max else [])
        )
        self._settings['load_state_component'].set_options(['N_zz', 'N_zs', 'sigma_zz', 'sigma_zs'])
        self._settings['use_arrow'].set_value(False)
        self._settings['max_display_value'].set_value(0.5)
        self._settings['plot_value_numbers'].set_value(False)
        self._settings['x_axis_mirrored'].set_value(False)
        self._settings['y_axis_mirrored'].set_value(True)
        self._settings['plot_value_scale'].set_value(True)
        self._settings['arrow_scale_factor'].set_value(0.5)
        self._settings['coordinate_axis_length'].set_value(0.5)

    def _update_plot(self):
        settings = self._settings
        cs_idx = settings['cross_section'].value
        cs_processor = self.solver.cs_processors[cs_idx]
        axes = self.fig.subplots()
        self.solver.plot_load_states(
            cross_section_idx=cs_idx,
            selected_load_case=settings['load_case'].value,
            selected_stress_state=settings['load_state_component'].value,
            stress_source=settings['load_state_source'].value,
            plot_value_numbers=settings['plot_value_numbers'].value,
            x_axis_mirrored=settings['x_axis_mirrored'].value,
            y_axis_mirrored=settings['y_axis_mirrored'].value,
            coordinate_axis_length=settings['coordinate_axis_length'].value,
            title=f'Section {cs_processor.z_beam} m',
            # cross_section_size=(20, 15),
            plot_value_scale=settings['plot_value_scale'].value,
            max_display_value=settings['max_display_value'].value,
            plot_direction_as_arrow=settings['use_arrow'].value,
            arrow_scale_factor=settings['arrow_scale_factor'].value,
            fig=self.fig,
            ax=axes,
        )
