#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from typing import Callable

import numpy as np
import pandas as pd

from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell_VCP
from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverBase
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.util import Vector
from PreDoCS.util.geometry import transform_location_m
from cpacs_interface.cpacs_interface import CPACSInterface

log = get_module_logger(__name__)

try:
    from lightworks.mechana.assemlies.assembly import Assembly, update_structural_model_with_mesh
    from lightworks.mechana.parts.panel import BasePanel
    from lightworks.mechana.loads.loadstate import LoadState
    from lightworks.cpacs_interface.cpacs_interface_lightworks import CPACSInterfaceLightworks
    from lightworks.opti.solver.interface import ISolver
    from lightworks.structural_model_generator.structural_model_generator_from_cpacs import StructuralModelCPACSInterface
    from lightworks.opti.config import OptimisationControl
except ImportError as ex:
    log.error('Modul lightworks.mechana not found. Material world VCP can not be used.')
    raise ex


class PreDoCS_SolverLightworks(PreDoCS_SolverBase, ISolver):
    """

    """

    def __init__(self, ctrl):
        """
        The PreDoCS calculation model is initialised only with an instance of Class control.

        The initialisation does not import any CPACS model. This is done by build model.

        Parameters
        ----------
        ctrl: Control
            Instance of class Control.
        """
        super().__init__(ctrl)

        if ctrl.dtype is None:
            self._dtype = np.dtype(OptimisationControl().get_solver_dtype_str())
        else:
            self._dtype = np.dtype(ctrl.dtype)

        self._panel2components = None
        self._component2panel = None
        self._nodes = None

    @property
    def _cpacs_interface_class(self) -> type:
        return CPACSInterfaceLightworks

    @property
    def _get_element_stiffness_func(self) -> Callable:
        return get_stiffness_for_shell_VCP

    def build_model(self, cpacs_interface: CPACSInterface = None, skip_solve: bool = False, **kwargs):
        """
        The method build_model imports a CPACS model and builds up the entire PreDoCS model
        and create references to the structural model.

        A PreDoCS model includes:
            - Cross section processors
            - A load processor containing the load cases for calculation
            - Boundary conditions, for now a clamped end is hard coded at the wing root.
            - The beam model based on the cross section stiffness.
        """
        super().build_model(cpacs_interface=cpacs_interface, skip_solve=True, **kwargs)

        # Link to lightworks structural model
        self._create_and_link_structural_model()

        # Set solver mesh in lightworks structural model
        self._set_solver_mesh_in_structural_model()

        # Initial Solve
        self._solve()

    def _create_and_link_structural_model(self):
        """
        Creates the lightworks structural model and the connection between it and the PreDoCS model.
        """
        # TODO: ATTENTION: Component and Element Classes using hash only unique for one cross section

        # Create structural model
        self._structural_model_interface = StructuralModelCPACSInterface(self.cpacs_interface, [self.c2p.wing.uid])
        self._structural_model = self._structural_model_interface.get_structural_model(with_ribs=False)

        # CPACS uid to PreDoCS component dict
        uid2component = {}
        for cross_section in self._cs_processors:
            for component in cross_section.discreet_geometry.components:
                uid = None
                if component.material_region:
                    # Cell
                    uid = component.material_region.uid
                elif 'spar_cell_uid' in component.extra_data:
                    # Spar cell
                    uid = component.extra_data['spar_cell_uid']
                if uid:
                    if uid in uid2component.keys():
                        raise RuntimeError(f'uID "{uid}" used in multiple cross section components.')
                    uid2component[uid] = (cross_section, component)
                else:
                    log.warning(
                        f'No uID found for component "{component.id}" in cross section at "{cross_section.z_beam}" m.')

        # PreDoCS component to PreDoCS segment dict
        component2segments = {}
        for cross_section in self._cs_processors:
            for segment in cross_section.discreet_geometry.segments:
                component = (cross_section, segment.component)
                if component in component2segments:
                    component2segments[component].append(segment)
                else:
                    component2segments[component] = [segment]

        # Add connection for all base parts
        self._panel2components = {}
        self._component2panel = {}
        segment2panel = {}
        for part in self._structural_model.base_parts:
            if isinstance(part, BasePanel):
                # Only panels, no assemblies
                if part.uid is not None:
                    uid = part.uid
                else:
                    raise RuntimeError(f'Part "{part}" not supported by the PreDoCS Solver')

                if uid not in uid2component:
                    log.warning(
                        f'Part "{uid}" not found in solver. Part is deleted from structural model.')  # TODO: is this an error?
                    self._structural_model.delete_part(part)
                else:
                    cross_section, component = uid2component[uid]
                    # # Filter for material regions
                    # if component.material_region:
                    segments = component2segments[(cross_section, component)]
                    for segment in segments:
                        assert segment not in segment2panel, 'Segment can be assigned to exact one panel'
                        segment2panel[(cross_section, segment)] = part

                    self._component2panel[(cross_section, component)] = part
                    if part in self._panel2components:
                        self._panel2components[part].append((cross_section, component))
                    else:
                        self._panel2components[part] = [(cross_section, component)]

        # Check for components assigned to more than one panel
        all_components = []
        for part, cs_component_tuples in self._panel2components.items():
            all_components.extend(cs_component_tuples)
        # # DEBUG
        # components_by_cs = {cs: [] for cs in self._cs_processors}
        # for part, cs_component_tuples in self._panel2components.items():
        #     for cross_section, component in cs_component_tuples:
        #         components_by_cs[cross_section].append(component)

        assert len(all_components) == len(set(all_components)), 'Component assigned to multiple panels'

        # Create or use replacement skin if needed
        if self._ctrl.use_lp:
            for part, cs_component_tuples in self._panel2components.items():
                if len(cs_component_tuples) > 1:
                    log.info('More than one component for one panel, '
                             'the first component is used to create the lamination parameters')
                cross_section, component = cs_component_tuples[0]
                component_elements = [e for e in cross_section.discreet_geometry.elements if e.component == component]
                original_skin = component.shell
                if self._ctrl.lp_skin:
                    replacement_skin = self._ctrl.lp_skin.copy()
                elif self._ctrl.lp_material:
                    replacement_skin = component.shell.get_lamination_parameter(
                        material=self._ctrl.lp_material)
                else:
                    replacement_skin = component.shell.get_lamination_parameter()

                if hasattr(original_skin, 'uid'):
                    replacement_skin.uid = original_skin.uid
                else:
                    log.warning(f'Skin "{original_skin}" is replaced and has no uid. '
                                'The skin is not written by the structural model interface.')

                # Update material stiffness
                # TODO Think about shifting stiffness to component instead of material.
                element_type = type(component_elements[0])
                replacement_skin.stiffness = self._get_element_stiffness_func(replacement_skin, element_type, dtype=self._dtype)

                # Update structural model material
                part.skin = replacement_skin

                # Update PreDoCS material
                component.shell = replacement_skin

    def _set_solver_mesh_in_structural_model(self):
        """
        Sets the geometry of the the lightworks structural model (solver mesh).
        """
        predocs_coord = self._predocs_coord

        # Transformation matrix from local PreDoCS to global CPACS coordinates
        T_p2c = predocs_coord.transformation_wing_2_aircraft

        node_coordinates = {}
        shape_elements = {}

        def get_element_nodes(z_inner, z_outer, p1, p2, element_id: str):
            return {
                element_id + '01': Vector([p1.x, p1.y, z_inner]),
                element_id + '02': Vector([p2.x, p2.y, z_inner]),
                element_id + '03': Vector([p2.x, p2.y, z_outer]),
                element_id + '04': Vector([p1.x, p1.y, z_outer]),
            }

        for panel, cs_component_tuples in self._panel2components.items():
            panel_elements = {}
            for cross_section, component in cs_component_tuples:
                i_cs = int(np.where(np.isclose(predocs_coord.z2_cs, cross_section.z_beam))[0])
                z2_inner = predocs_coord.z2_bn[i_cs]
                z2_outer = predocs_coord.z2_bn[i_cs + 1]

                component_elements = [e for e in cross_section.discreet_geometry.elements if e.component == component]
                for element in component_elements:
                    element_id = self.get_element_id(cross_section.id, component.id, element.id)
                    nodes = get_element_nodes(
                        z2_inner, z2_outer, element.node1.position, element.node2.position, element_id)

                    # Transform node position from PreDoCS to CPACS coordinate system
                    nodes = {node_id: transform_location_m(T_p2c, node_position)
                             for node_id, node_position in nodes.items()}

                    node_coordinates.update(nodes)
                    panel_elements[element_id] = list(nodes.keys())

            shape_elements[panel.name] = panel_elements

        self._nodes = pd.DataFrame(node_coordinates).T
        self._structural_model = update_structural_model_with_mesh(
            self._structural_model, node_coordinates, shape_elements, update_buckling_lengths=False)

    def update_structural_model(self):
        """
        This method updates the structural properties used by the solver.

        The update is based on the panels in the panel2segment dictionary.

        The panels in the dictionary are the same panels as in the structural model of the optimisation process.

        The method update structural model is used to change the material property abd.

        Material thickness information is included in the abd matrix.

        After alternation the beam model is recalculated.
        """
        # # DEBUG
        # with open(f'H:/panel_materials_{random()}.txt', 'w') as f:
        #     f.write(f'PID: {os.getpid()}, datetime: {datetime.now().isoformat()}\n')
        #     for panel, cs_component_tuples in self.panel2components.items():
        #         f.write(f'Panel "{panel.name}: Thickness: {panel.skin.thickness}\n')
        #         for cross_section, component in cs_component_tuples:
        #             f.write(f'\tCS "{cross_section.id}", Component "{component.id}"\n')

        # Check for component in multiple parts
        components = {}
        for panel, cs_component_tuples in self.panel2components.items():
            components.update({id(component): component for cross_section, component in cs_component_tuples})
        c_ids = list(components.keys())
        multiple_used_components = [(c_id, c) for c_id, c in components.items() if c_ids.count(c_id) > 1]
        assert len(
            multiple_used_components) == 0, f'Components are used in multiple parts: "{multiple_used_components}".'

        # Update cross sections material information
        cs_component2material = {cs: {} for cs in self._cs_processors}
        for panel, cs_component_tuples in self.panel2components.items():
            for cross_section, component in cs_component_tuples:
                cs_component2material[cross_section][component] = panel.skin
        for processor in self._cs_processors:
            processor.update_components(cs_component2material[processor], self.ctrl.processor_type,
                                        self.c2p._get_element_stiffness_func)

        # Update internal solver
        self._internal_solver.update_structural_model()

        # Solve again with updated model
        self._solve()

    def get_panel_loads(self, panel, element_flag=False):
        """
        Return a list of Loadcases for a panel. Each LoadState is representative for the load state of one element.

        Additionally a list of elements referring to the list of Loadcases is returned.

        Parameter
        ---------
        panel: Panel
            The panel for which the Loadcases need to be calculated.
        element_flag: bool
            True: return element_list

        Return
        ------
        panel_loadcase_list:
            List of Loadcases of one Panel, each LoadState represents the load state of one element.
        element_list:
            Optional. The list of Elements referring to the list of Loadcases.
        list(float)
            Optional. The list of the element lengths.
        """
        # log.debug(f'get_panel_loads: {panel.name}')

        if panel not in self.panel2components:
            return None

        element_ids = []
        element_load_states = []
        element_lengths = []

        # Get the component connected to the panel
        cs_component_tuples = self.panel2components[panel]
        for cross_section, component in cs_component_tuples:
            # Get the Element load states for the component
            panel_loadstate_list, element_list = self._get_component_load_functions(cross_section, component)
            # log.debug(f'component: {component}')
            # log.debug(f'panel_loadcase_list: {panel_loadstate_list}')
            # log.debug(f'element_list: {element_list}')
            element_ids.extend(
                [self.get_element_id(cross_section.id, component.id, element.id) for element in element_list])
            element_load_states.extend(panel_loadstate_list)
            if element_flag:
                element_lengths.extend([element.length for element in element_list])

        # Set element ids
        for element_id, element_load_state in zip(element_ids, element_load_states):
            element_load_state.element_ids = [element_id]

        # # DEBUG
        # solver_details_path = os.environ.get('solver_details_path', '')
        # with open(os.path.join(solver_details_path, f'panel_loads_{random()}.p'), 'wb') as f:
        #     cloudpickle.dump((os.getpid(), datetime.now(), panel.name, panel.skin.thickness, panel, element_load_states, self), f)

        if element_flag:
            return element_load_states, element_ids, element_lengths
        else:
            return element_load_states

    def get_init_loads(self, panel):
        """
        Method used in the constraint processor of the optimisation interface to initialise the load cases.

        No actual load cases are needed here, only the right number has to be returned.

        For PreDoCS as a solver also the actual load cases at that stat can be returned because there is no real
        advantage in computational time returning dummy load cases.

        Parameter
        ---------
        panel: Panel
            The panel.
        """
        return self.get_panel_loads(panel, element_flag=True)

    # PreDoCS to lightworks coordinate system conversion:
    _STRESS_NAMES_PREDOCS2LIGHTWORKS = {
        'N_zz': 'n_x',
        'N_zs': 'n_xy',
        'N_zn': 'n_xz',
        'N_sn': 'n_yz',
        'M_zz': 'm_x',
        'M_ss': 'm_y',
        'M_zs': 'm_xy'
    }
    _STRAIN_NAMES_PREDOCS2LIGHTWORKS = {
        # Jung
        'epsilon_zz': 'e_x',
        'epsilon_ss': 'e_y',
        'gamma_zs': 'e_xy',
        'kappa_zz': 'k_x',
        'kappa_zs': 'k_xy',
        'kappa_ss': 'k_y',

        # Song
        'epsilon_zz_0': 'e_x'
        # 'gamma_zn': Not used
    }

    # Negative sign of gamma_zs, kappa_zs and gamma_sn (and N_zs, M_zs, N_sn and sigma_zs) due to different
    # coordinate system convention of the PreDoCS s,z,n COSY to the PreDoCS laminate u,v,w COSY
    _neg_sign_keys = ['gamma_zs', 'kappa_zs', 'gamma_sn', 'N_zs', 'M_zs', 'N_sn']

    def _get_component_load_functions(self, cross_section, component):
        """
        Return a list of Loadcases for a component. Each LoadState is representative for the load state of one element.

        Additionally a list of elements referring to the list of Loadcases is returned.

        Parameter
        ---------
        component: Component
            PreDoCS component for stress evaluation

        Return
        ------
        load_case_list: list(LoadState)
            List of Loadcases containing one load case for each element in the component.
        element_list: list(IElement)
            List of elements were each element refers to one LoadState.
        """
        load_states = []
        element_lengths = []
        loadstate_ids = []
        element_list = []

        if self.ctrl.calc_element_load_state_min_max:
            load_states_dict = self.min_max_load_states_dict
        elif self.ctrl.calc_element_load_state_functions:
            load_states_dict = self.load_states_dict
        else:
            raise RuntimeError(
                'At least on option of "calc_element_load_state_min_max" and '
                '"calc_element_load_state_functions" must be True'
            )

        assert len(load_states_dict) > 0, 'No load states in Solver, clear_results must not be called!'

        element_reference_length_dict = cross_section.discreet_geometry.element_reference_length_dict

        component_elements = [e for e in cross_section.discreet_geometry.elements if e.component == component]
        # Iterate through all design load cases
        for ls_key in load_states_dict.keys():
            # Iterate through all cross sections
            for cs_element_dict in load_states_dict[ls_key]:
                # Check element in cross section
                for element in component_elements:
                    # Attention: Don't compare representation but id/instance!
                    if id(element) in [id(e) for e in cs_element_dict.keys()]:
                        load_states.append(cs_element_dict[element])
                        element_lengths.append(element_reference_length_dict[element])
                        loadstate_ids.append(ls_key)
                        element_list.append(element)

        load_state_list = []

        # Get the load case of each element in a component
        for load_state, element_length, loadstate_id, element in zip(load_states, element_lengths, loadstate_ids,
                                                                     element_list):
            if self.ctrl.calc_element_load_state_min_max:
                strain_dict = {state_key: max([load_state[0].strain_state[state_key],
                                               load_state[1].strain_state[state_key]], key=abs)
                               for state_key in load_state[0].strain_state.keys()}
                stress_dict = {state_key: max([load_state[0].stress_state[state_key],
                                               load_state[1].stress_state[state_key]], key=abs)
                               for state_key in load_state[0].stress_state.keys()}
            elif self.ctrl.calc_element_load_state_functions:
                strain_dict, stress_dict = self._extreme_stress_states(load_state=load_state,
                                                                       element_length=element_length)
            else:
                raise RuntimeError(
                    'At least on option of "calc_element_load_state_min_max" and '
                    '"calc_element_load_state_functions" must be True'
                )

            # Create lightworks load case
            # Negative sign of gamma_zs, kappa_zs and gamma_sn (and N_zs, M_zs, N_sn and sigma_zs) due to different
            # coordinate system convention of the PreDoCS s,z,n COSY to the PreDoCS laminate u,v,w COSY
            strain_stress_dict_lightworks = {}
            strain_stress_dict_lightworks.update({
                self._STRESS_NAMES_PREDOCS2LIGHTWORKS[key]: -value if key in self._neg_sign_keys else value
                for key, value in stress_dict.items()
                if key in self._STRESS_NAMES_PREDOCS2LIGHTWORKS
            })
            strain_stress_dict_lightworks.update({
                self._STRAIN_NAMES_PREDOCS2LIGHTWORKS[key]: -value if key in self._neg_sign_keys else value
                for key, value in strain_dict.items()
                if key in self._STRAIN_NAMES_PREDOCS2LIGHTWORKS
            })
            load_state = LoadState(loadstate_id, **strain_stress_dict_lightworks)

            element_id = self.get_element_id(cross_section.id, component.id, element.id)
            load_state.label = element_id
            load_state_list.append(load_state)

        return load_state_list, element_list

    def get_nodes(self) -> pd.DataFrame:
        """
        Returns a dataframe with nodes ids as index and positions as values.

        Returns
        -------
        pd.DataFrame
        """
        return self._nodes

    def get_displacements(self, panel, coordinate_system='global'):
        """
        Returns the beam displacements of the given panel for all loadcases.

        Parameters
        ----------
        panel: lightworks.mechana.parts.panel instance
            Panel instance.

        Returns
        -------
        dict
            Dictionary of Loadcases. For each loadcases a dict for each element containing a
            dict for each node displacements.
        """
        # Transformation matrix from global CPACS to local PreDoCS coordinates
        T_c2p = self.predocs_coord.transformation_aircraft_2_wing

        # Transformation matrix from local PreDoCS to global CPACS coordinates
        T_p2c = self.predocs_coord.transformation_wing_2_aircraft

        # Displacements for each load case
        load_case_element_displacement_dict = {}
        for load_case_name, beam_displacements_function in self.beam_displacement_function_dict.items():

            # Displacements for each node of the panel
            displacements_dict = {}
            for node_id, node_pos_cpacs in panel.nodes.items():
                # Node position from CPACS to PreDoCS coordinate system
                node_pos_predocs = transform_location_m(T_c2p, node_pos_cpacs)
                z_node = node_pos_predocs[2]

                # Displaced node position at the node z-position
                T_displacement_predocs = self._get_transformation_matrix_from_beam_displacements(
                    beam_displacements_function(z_node))
                node_pos_displaced_predocs = transform_location_m(T_displacement_predocs, node_pos_predocs)

                # Displaced node position from PreDoCS to CPACS coordinate system
                node_pos_displaced_cpacs = transform_location_m(T_p2c, node_pos_displaced_predocs)

                node_displacement = node_pos_displaced_cpacs - node_pos_cpacs
                displacements_dict[node_id] = node_displacement

            load_case_element_displacement_dict[load_case_name] = displacements_dict

        return load_case_element_displacement_dict

    def read_displacements(self) -> dict[str, pd.DataFrame]:
        """
        Reads the displacements and stores them in the displacements attribute.

        Returns
        -------
        pd.DataFrame:
            displacements of all nodes. Index: node IDs, Value: [nx, ny, nz, mx, my, mz]
        """
        node_displacements_list = []
        for part in self._structural_model.base_parts:
            node_displacements = self.get_displacements(part)
            for load_case, nd in node_displacements.items():
                for node_id, displacements in nd.items():
                    node_displacements_list.append(dict(
                        load_case=load_case,
                        node_id=node_id,
                        nx=displacements.x,
                        ny=displacements.y,
                        nz=displacements.z,
                    ))
        df_node_displacements = pd.DataFrame(node_displacements_list)
        lc_dict = {}
        for lc_name in df_node_displacements.load_case.unique():
            df_lc = df_node_displacements[df_node_displacements.load_case == lc_name]

            # Check if all nodes of the part have the same displacements
            assert df_lc.groupby('node_id').nx.nunique().eq(1).all()
            assert df_lc.groupby('node_id').ny.nunique().eq(1).all()
            assert df_lc.groupby('node_id').nz.nunique().eq(1).all()

            df_res = df_lc.groupby('node_id').nth(0)
            df_res['mx'] = 0
            df_res['my'] = 0
            df_res['mz'] = 0

            lc_dict[lc_name] = df_res[['node_id', 'nx', 'ny', 'nz', 'mx', 'my', 'mz']].set_index('node_id')
        return lc_dict

    def init_optimization(self, client, optimization_model):
        """
        Needed to fulfill the optimisation interface.

        Parameters
        ----------
        client: distributed.Client
            instance of dask.distributed.Client to prepare distributed evaluation.
        optimization_model: lightworks.mechana.optimization_model.OptimisationModel
            instance of the optimization model
        """
        # Speed up pickle
        # self.clear_results()
        pass

    @staticmethod
    def get_element_id(cs_id, component_id, element_id) -> str:
        """
        Returns a unique id for an PreDoCS cross section element.

        Parameters
        ----------

        Return
        ------
        """
        return '{0:03d}{1:03d}{2:03d}'.format(cs_id, component_id, element_id)

    def __getstate__(self):
        """Make pickle possible."""
        state = super().__getstate__()
        state['_structural_model_interface'] = None

        return state

    @property
    def structural_model_interface(self):
        return self._structural_model_interface

    @property
    def panel2components(self):
        return self._panel2components

    @property
    def component2panel(self):
        return self._component2panel

    @property
    def structural_model(self) -> Assembly:
        """The structural model for the solver."""
        return self._structural_model
