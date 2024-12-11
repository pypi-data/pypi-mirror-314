"""
This module contains the implementation of the CPACS interface using PreDoCS materials.
"""

import logging
from copy import deepcopy
from typing import Union, Optional, Callable

from PreDoCS.MaterialAnalysis.CLT import Ply
from PreDoCS.MaterialAnalysis.Interfaces import IShell
from PreDoCS.MaterialAnalysis.Materials import Anisotropic, Isotropic, Orthotropic, Transverse_Isotropic, \
    MaterialFailureData
from PreDoCS.MaterialAnalysis.Shells import IsotropicShell, CompositeShell
from PreDoCS.util.data import get_equal_content_key
from cpacs_interface.cpacs_interface import CPACSInterface
from cpacs_interface.utils.tixi import double_format, tixi_create_x_path, \
    tixi_get_value_from_path, tixi_generate_uid

log = logging.getLogger(__name__)


class CPACSInterfacePreDoCS(CPACSInterface):
    """

    """
    def __init__(self, directory: str, filename: str, simplified_airfoils_epsilon: Optional[float] = None, **kwargs):
        """
        The CPACS interface is at it's current state designed to manipulate CPACS files rather than to create them.

        The interface is set up for a specified CPACS file and allows to read and material and composite data.

        For performance reasons, the airfoils can be simplified before loading the shapes of the airfoil.
        For this, the Ramer–Douglas–Peucker algorithm is used
        (https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm).
        The epsilon variable can be used to determine how strong the airfoil should be.

        Parameters
        ----------
        directory: str
            The directory of the CPACS file.
        filename: str
            The filename of the CPACS file.
        name: str
            Value of the name element in the CPACS header. Only used, if the CPACS file does not exist.
        description: str
            Value of the description element in the CPACS header. Only used, if the CPACS file does not exist.
        creator: str
            Value of the creator element in the CPACS header. Only used, if the CPACS file does not exist.
        version: str
            Value of the version element in the CPACS header (This is NOT the CPACS version).
            Only used, if the CPACS file does not exist.
        simplified_airfoils_epsilon
            The epsilon for the Ramer–Douglas–Peucker algorithm to simplify the airfoils. None for no simplification.
        """
        super().__init__(directory, filename, simplified_airfoils_epsilon=simplified_airfoils_epsilon, **kwargs)

    def _write_single_material(self, uid, material):
        if isinstance(material, CompositeShell):
            self._write_composite(uid, material)
        elif isinstance(material, Anisotropic):
            self._write_material(uid, material)
        else:
            raise RuntimeError(f'Unknown material type "{type(material)}".')

    def create_composite(self, name: str, layers: list[dict], **kwargs):
        return CompositeShell(
            name=name,
            layup=[
                Ply(
                    name=layer['name'],
                    material=layer['material'],
                    thickness=layer['thickness'],
                    orientation=layer['angle'],
                    ply_index_global=layer['ply_index_global'] if 'ply_index_global' in layer else None,
                    labels=layer['labels'] if 'labels' in layer else None,
                )
                for i, layer in enumerate(layers)],
            **kwargs,
        )

    def get_composite_dict(self, uid: str, composite: CompositeShell) -> dict:
        return {
            'name': composite.name,
            'layers': [
                {
                    'name': ply.name,
                    'material': ply.material,
                    'thickness': ply.thickness,
                    'angle': ply.orientation,
                    'ply_index_global': ply.ply_index_global,
                    'labels': ply.labels,
                }
                for ply in composite.layup
            ],
        }

    def read_skin(self, xpath) -> IShell:
        """
        Returns the skin from a given XPath.

        Parameters
        ----------
        xpath: str
            XPath of the material.

        Returns
        -------
        IShell
            The skin.
        """
        self._read_if_required()

        tixi = self._tixi_handle
        if tixi.checkElement(xpath + '/materialUID'):
            material_uid = str(tixi_get_value_from_path(tixi, xpath + '/materialUID'))
            material = self._uid2material[material_uid]
            if tixi.checkElement(xpath + '/thickness'):
                thickness = tixi_get_value_from_path(tixi, xpath + '/thickness')
            else:
                raise RuntimeError('For a materialUID, thickness must exist')
        elif tixi.checkElement(xpath + '/compositeUID'):
            material_uid = str(tixi_get_value_from_path(tixi, xpath + '/compositeUID'))
            material = self._uid2material[material_uid]
            thickness = None
            if tixi.checkElement(xpath + '/compositeUID/orthotropyDirection'):
                log.warning(f'orthotropyDirection element of material "{material_uid}" is ignored')
            if tixi.checkElement(xpath + '/compositeUID/thicknessScaling'):
                log.warning(f'thicknessScaling element of material "{material_uid}" is ignored')
        else:
            raise RuntimeError('Material element must contain materialUID or compositeUID element')

        name = material.name  # TODO: use different names for sheets of same material?
        # Each component needs its own material instance in order to use it as an optimisation region later
        # Return a copy of the material and add a thickness depending on the material type
        if isinstance(material, Isotropic):
            # return sheet with isotropic material
            return IsotropicShell(material=material, thickness=thickness, name=name, uid=material_uid)
        elif isinstance(material, CompositeShell):
            # return a copy of a Laminate
            material_copy = deepcopy(material)
            material_copy.uid = material_uid
            material_copy.name = name
            return material_copy
        elif isinstance(material, Anisotropic) or isinstance(material, Orthotropic) or isinstance(material, Transverse_Isotropic):
            # TODO: only workaround
            # If an orthotropic, anisotripic or transversal isotropic material is assigned to a cell or shell,
            # a laminate with one layer of this material is created.
            # This is just a workaround, because for PreDoCS only isotropic materials or laminates should be assigned to cells and shells.
            log.warning(
                'Wrong CPACS material assignment: '
                'For PreDoCS, only isotropic materials or laminates should be assigned to cells and shells.'
            )
            return CompositeShell(
                layup=[Ply(material=deepcopy(material), thickness=thickness, orientation=0)],
                name=name + '_laminate',
                uid=material_uid,
            )
        else:
            raise ImportError(f'Unknown skin type "{type(material)}".')

    def write_skin(self, xpath: str, skin: 'Union[IsotropicShell, CompositeShell]'):
        """
        handle the writing of a skin, including updating material/laminates

        Parameters
        ----------
        xpath
            The XPath of the material element.
        skin
            The skin to write.
        """
        tixi = self.tixi_handle

        # Remove existing data
        if tixi.checkElement(xpath):
            tixi.removeElement(xpath)
        tixi_create_x_path(tixi, xpath)

        # Single material
        if isinstance(skin, IsotropicShell):
            # Search for existing material
            material = skin.material
            material_uid = material.uid
            if material_uid in self.uid2material:
                if material_uid not in self._written_material_uids:
                    material_uid = get_equal_content_key(self.uid2material, material)
                else:
                    material_uid = tixi_generate_uid(tixi, material.uid if material.uid is not None else material.name)
            else:
                material_uid = tixi_generate_uid(tixi, material.uid if material.uid is not None else material.name)

            self._write_material(material_uid, material)

            tixi.addTextElement(xpath, 'materialUID', material_uid)
            tixi.addDoubleElement(xpath, 'thickness', skin.thickness, double_format)

        # Laminate
        elif isinstance(skin, CompositeShell):
            material_uid = skin.uid
            if material_uid in self.uid2material:
                material_uid = get_equal_content_key(self.uid2material, self.uid2material[skin.uid])
            else:
                material_uid = get_equal_content_key(self.uid2material, skin)
            if material_uid is None:
                material_uid = tixi_generate_uid(tixi, skin.uid if skin.uid is not None else skin.name)

            self._write_composite(material_uid, skin)

            tixi.addTextElement(xpath, 'compositeUID', material_uid)
            tixi.addDoubleElement(xpath, 'orthotropyDirection', 0, double_format)

        else:
            raise NotImplementedError(f'Writing of skin {type(skin)} is currently not implemented')

    @staticmethod
    def _orthotropic_from_cpacs_old(mp: dict[str, Union[float, str]]) -> 'Orthotropic':
        """
        This method initiates an instance of class Orthotropic from the old CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Orthotropic
            Instance of Orthotropic material.
        """
        material = Orthotropic.init_from_stiffness(
            C11=mp['k11'],
            C12=mp['k12'],
            C13=mp['k13'],
            C22=mp['k22'],
            C23=mp['k23'],
            C33=mp['k33'],
            C44=mp['k44'],
            C55=mp['k55'],
            C66=mp['k66'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        if 'sig11t' in mp.keys():
            failure_data.set_failure_stresses(
                sigma_1t=mp['sig11t'],
                sigma_2t=mp['sig22t'],
                sigma_3t=mp['sig33t'],
                sigma_1c=mp['sig11c'],
                sigma_2c=mp['sig22c'],
                sigma_3c=mp['sig33c'],
                sigma_12=mp['tau12'],
                sigma_13=mp['tau13'],
                sigma_23=mp['tau23'],
            )
        if 'maxStrain' in mp.keys():
            failure_data.set_failure_strains(
                epsilon_1t=mp['maxStrain'],
                epsilon_2t=mp['maxStrain'],
                epsilon_3t=mp['maxStrain'],
                epsilon_1c=mp['maxStrain'],
                epsilon_2c=mp['maxStrain'],
                epsilon_3c=mp['maxStrain'],
                epsilon_12=mp['maxStrain'],
            )
        material.failure_data = failure_data

        return material

    @staticmethod
    def _orthotropic_from_cpacs_new_shell(mp: dict[str, Union[float, str]]) -> 'Orthotropic':
        """
        This method initiates an instance of class Orthotropic from the new CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Orthotropic
            Instance of Orthotropic material.
        """
        material = Orthotropic(
            E_11=mp['E1'],
            E_22=mp['E2'],
            E_33=mp['E2'],
            nu_12=mp['nu'],
            nu_23=mp['nu'],
            nu_13=mp['nu'],
            G_12=mp['G12'],
            G_23=mp['G23'],
            G_13=mp['G31'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        failure_data.set_failure_stresses(
            sigma_1t=mp.get('sig1t'),
            sigma_2t=mp.get('sig2t'),
            sigma_3t=mp.get('sig2t'),
            sigma_1c=mp.get('sig1c'),
            sigma_2c=mp.get('sig2c'),
            sigma_3c=mp.get('sig2c'),
            sigma_12=mp.get('tau12'),
            sigma_13=mp.get('tau12'),
            sigma_23=mp.get('tau12'),
        )
        failure_data.set_failure_strains(
            epsilon_1t=mp.get('eps1t'),
            epsilon_2t=mp.get('eps2t'),
            epsilon_3t=mp.get('eps2t'),
            epsilon_1c=mp.get('eps1c'),
            epsilon_2c=mp.get('eps2c'),
            epsilon_3c=mp.get('eps2c'),
            epsilon_12=mp.get('gamma12'),
        )
        material.failure_data = failure_data

        return material

    @staticmethod
    def _orthotropic_from_cpacs_new_solid(mp: dict[str, Union[float, str]]) -> 'Orthotropic':
        """
        This method initiates an instance of class Orthotropic from the new CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Orthotropic
            Instance of Orthotropic material.
        """
        material = Orthotropic(
            E_11=mp['E1'],
            E_22=mp['E2'],
            E_33=mp['E2'],
            nu_12=mp['nu12'],
            nu_23=mp['nu23'],
            nu_13=mp['nu31'] * mp['E1'] / mp['E3'],
            G_12=mp['G12'],
            G_23=mp['G23'],
            G_13=mp['G31'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        failure_data.set_failure_stresses(
            sigma_1t=mp.get('sig1t'),
            sigma_2t=mp.get('sig2t'),
            sigma_3t=mp.get('sig3t'),
            sigma_1c=mp.get('sig1c'),
            sigma_2c=mp.get('sig2c'),
            sigma_3c=mp.get('sig3c'),
            sigma_23=mp.get('tau23'),
            sigma_13=mp.get('tau31'),
            sigma_12=mp.get('tau12'),
        )
        failure_data.set_failure_strains(
            epsilon_1t=mp.get('eps1t'),
            epsilon_2t=mp.get('eps2t'),
            epsilon_3t=mp.get('eps3t'),
            epsilon_1c=mp.get('eps1c'),
            epsilon_2c=mp.get('eps2c'),
            epsilon_3c=mp.get('eps3c'),
            epsilon_12=mp.get('gamma12'),
        )
        material.failure_data = failure_data

        return material

    @staticmethod
    def _transverse_isotropic_from_cpacs_old(mp: dict[str, Union[float, str]]) -> 'Transverse_Isotropic':
        """
        This method initiates an instance of class Transverse_Isotropic from the old CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Transverse_Isotropic
            Instance of Transverse_Isotropic material.
        """
        material = Transverse_Isotropic.init_from_stiffness(
            C11=mp['k11'],
            C12=mp['k12'],
            C22=mp['k22'],
            C23=mp['k23'],
            C66=mp['k66'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        if 'sig11t' in mp.keys():
            failure_data.set_failure_stresses(
                sigma_1t=mp['sig11t'],
                sigma_1c=mp['sig11c'],
                sigma_2t=mp['sig22t'],
                sigma_2c=mp['sig22c'],
                sigma_12=mp['tau12'],
                sigma_23=mp['tau23'],
            )
        if 'maxStrain' in mp.keys():
            failure_data.set_failure_strains(
                epsilon_1t=mp['maxStrain'],
                epsilon_2t=mp['maxStrain'],
                epsilon_3t=mp['maxStrain'],
                epsilon_1c=mp['maxStrain'],
                epsilon_2c=mp['maxStrain'],
                epsilon_3c=mp['maxStrain'],
                epsilon_12=mp['maxStrain'],
            )
        material.failure_data = failure_data

        return material

    @staticmethod
    def _transverse_isotropic_from_cpacs_new_shell(mp: dict[str, Union[float, str]]) -> 'Transverse_Isotropic':
        """
        This method initiates an instance of class Transverse_Isotropic from the new CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Transverse_Isotropic
            Instance of Transverse_Isotropic material.
        """
        log.warning('Open TODOs for anisotropicShell CPACS material')
        # TODO: Why not import as Anisotropic material?
        # TODO: Are the parameters of init_from_stiffness solid (C) or shell (Q) stiffnesses

        material = Transverse_Isotropic.init_from_stiffness(
            C11=mp['Q11'],
            C12=mp['Q12'],
            C22=mp['Q22'],
            C23=mp['Q23'],
            C66=mp['Q33'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        failure_data.set_failure_stresses(
            sigma_1t=mp['sig1t'],
            sigma_1c=mp['sig1c'],
            sigma_2t=mp['sig2t'],
            sigma_2c=mp['sig2c'],
            sigma_12=mp['tau12'],
            sigma_23=mp['tau12'],
        )
        failure_data.set_failure_strains(
            epsilon_1t=mp.get('eps1t'),
            epsilon_2t=mp.get('eps2t'),
            epsilon_3t=mp.get('eps2t'),
            epsilon_1c=mp.get('eps1c'),
            epsilon_2c=mp.get('eps2c'),
            epsilon_3c=mp.get('eps2c'),
            epsilon_12=mp.get('gamma12'),
        )
        material.failure_data = failure_data

        return material

    @staticmethod
    def _transverse_isotropic_from_cpacs_new_solid(mp: dict[str, Union[float, str]]) -> 'Transverse_Isotropic':
        """
        This method initiates an instance of class Transverse_Isotropic from the new CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Transverse_Isotropic
            Instance of Transverse_Isotropic material.
        """
        log.warning('Open TODOs for anisotropicSolid CPACS material')
        # TODO: Why not import as Anisotropic material?

        material = Transverse_Isotropic.init_from_stiffness(
            C11=mp['C11'],
            C12=mp['C12'],
            C22=mp['C22'],
            C23=mp['C23'],
            C66=mp['C33'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        failure_data.set_failure_stresses(
            sigma_1t=mp['sig1t'],
            sigma_1c=mp['sig1c'],
            sigma_2t=mp['sig2t'],
            sigma_2c=mp['sig2c'],
            sigma_12=mp['tau12'],
            sigma_23=mp['tau12'],
        )
        failure_data.set_failure_strains(
            epsilon_1t=mp.get('eps1t'),
            epsilon_2t=mp.get('eps2t'),
            epsilon_3t=mp.get('eps2t'),
            epsilon_1c=mp.get('eps1c'),
            epsilon_2c=mp.get('eps2c'),
            epsilon_3c=mp.get('eps2c'),
            epsilon_12=mp.get('gamma12'),
        )
        material.failure_data = failure_data

        return material

    @staticmethod
    def _isotropic_from_cpacs_old(mp: dict[str, Union[float, str]]) -> 'Isotropic':
        """
        This method initiates an instance of class Isotropic from the old CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Isotropic
            Instance of Isotropic material
        """
        material = Isotropic.init_from_stiffness(
            C11=mp['k11'],
            C12=mp['k12'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        if 'sig11' in mp.keys():
            failure_data.set_failure_stresses(
                sigma_1t=mp['sig11'],
                sigma_12=mp['tau12'],
            )
        if 'maxStrain' in mp.keys():
            failure_data.set_failure_strains(
                epsilon_1t=mp['maxStrain'],
            )
        material.failure_data = failure_data

        return material

    @staticmethod
    def _isotropic_from_cpacs_new(mp: dict[str, Union[float, str]]) -> 'Isotropic':
        """
        This method initiates an instance of class Isotropic from the new CPACS material definition.

        Parameters
        ----------
        mp
            dict of the material properties.

        Returns
        -------
        Isotropic
            Instance of Isotropic material
        """
        material = Isotropic(
            E=mp['E'],
            nu=mp['nu'],
            name=mp['name'],
            density=mp['rho'],
        )
        failure_data = MaterialFailureData()
        failure_data.set_failure_stresses(
            sigma_1t=mp.get('sigt'),
            sigma_12=mp.get('tau12'),
        )
        failure_data.set_failure_strains(
            epsilon_1c=mp.get('epsc'),
            epsilon_1t=mp.get('epst'),
            epsilon_12=mp.get('gamma12'),
        )
        material.failure_data = failure_data

        return material

    @property
    def read_material_functions_dict(self) -> dict[str, Union[Callable, str]]:
        return {
            'orthotropic': self._orthotropic_from_cpacs_old,
            'transverse_isotropic': self._transverse_isotropic_from_cpacs_old,
            'isotropic': self._isotropic_from_cpacs_old,
            'orthotropic-new-shell': self._orthotropic_from_cpacs_new_shell,
            'orthotropic-new-solid': self._orthotropic_from_cpacs_new_solid,
            'anisotropic-shell': self._transverse_isotropic_from_cpacs_new_shell,
            'anisotropic-solid': self._transverse_isotropic_from_cpacs_new_solid,
            'isotropic-new': self._isotropic_from_cpacs_new,
        }

    def get_write_material_data(self, material, new_definition: bool, **kwargs) -> 'Union[dict[str, float], (dict[str, float], str)]':
        failure_data = material.failure_data
        if new_definition:
            E11, E22, E33, nu23, nu13, nu12, G23, G13, G12 = material.engineering_constants
            if isinstance(material, Isotropic):
                return (
                    'isotropicProperties', {
                        'name': material.name,
                        'density': material.density,
                        "E": E11,
                        "G": G12,
                        "nu": nu12,
                        "epsc": failure_data.max_strain.get('epsilon_1c', None),
                        "epst": failure_data.max_strain.get('epsilon_1t', None),
                        "gamma12": failure_data.max_strain.get('epsilon_12', None),
                        "sigc": failure_data.max_stress.get('sigma_1c', None),
                        "sigt": failure_data.max_stress.get('sigma_1t', None),
                        "tau12": failure_data.max_stress.get('sigma_12', None),
                    }
                )
            elif isinstance(material, Transverse_Isotropic):
                return (
                    'anisotropicShellProperties', {
                        'name': material.name,
                        'density': material.density,
                        "Q11": material.stiffness_matrix[0, 0],
                        "Q12": material.stiffness_matrix[0, 1],
                        "Q22": material.stiffness_matrix[1, 1],
                        "Q13": material.stiffness_matrix[0, 2],
                        "Q23": material.stiffness_matrix[1, 2],
                        "Q33": material.stiffness_matrix[5, 5],
                        "sig1c": failure_data.max_stress.get('sigma_1c', None),
                        "sig1t": failure_data.max_stress.get('sigma_1t', None),
                        "sig2c": failure_data.max_stress.get('sigma_2c', None),
                        "sig2t": failure_data.max_stress.get('sigma_2t', None),
                        "tau12": failure_data.max_stress.get('sigma_12', None),
                        "eps1c": failure_data.max_strain.get('epsilon_1c', None),
                        "eps1t": failure_data.max_strain.get('epsilon_1t', None),
                        "eps2c": failure_data.max_strain.get('epsilon_2c', None),
                        "eps2t": failure_data.max_strain.get('epsilon_2t', None),
                        "gamma12": failure_data.max_strain.get('epsilon_12', None),
                    }
                )
            elif isinstance(material, Orthotropic):
                return (
                    'orthotropicShellProperties', {
                        'name': material.name,
                        'density': material.density,
                        "E1": E11,
                        "E2": E22,
                        "G12": G12,
                        "G23": G23,
                        "G31": G13,
                        "nu": nu23,
                        "sig1c": failure_data.max_stress.get('sigma_1c', None),
                        "sig1t": failure_data.max_stress.get('sigma_1t', None),
                        "sig2c": failure_data.max_stress.get('sigma_2c', None),
                        "sig2t": failure_data.max_stress.get('sigma_2t', None),
                        "tau12": failure_data.max_stress.get('sigma_12', None),
                        "eps1c": failure_data.max_strain.get('epsilon_1c', None),
                        "eps1t": failure_data.max_strain.get('epsilon_1t', None),
                        "eps2c": failure_data.max_strain.get('epsilon_2c', None),
                        "eps2t": failure_data.max_strain.get('epsilon_2t', None),
                        "gamma12": failure_data.max_strain.get('epsilon_12', None),
                    }
                )
            else:
                # TODO: implement for anisotropicSolidProperties and orthotropicSolidProperties? Or Anisotripoc class?
                raise RuntimeError(f'No write method found for material type "{type(material)}".')
        else:
            if isinstance(material, Isotropic):
                return {
                    'name': material.name,
                    'density': material.density,
                    "k11": material.stiffness_matrix[0, 0],
                    "k12": material.stiffness_matrix[0, 1],
                    "sig11": failure_data.max_stress.get('sigma_1t', None),
                    "tau12": failure_data.max_stress.get('sigma_12', None),
                    "maxStrain": failure_data.max_strain.get('epsilon_1t', None),
                }
            elif isinstance(material, Transverse_Isotropic):
                return {
                    'name': material.name,
                    'density': material.density,
                    "k11": material.stiffness_matrix[0, 0],
                    "k12": material.stiffness_matrix[0, 1],
                    "k22": material.stiffness_matrix[1, 1],
                    "k23": material.stiffness_matrix[1, 2],
                    "k66": material.stiffness_matrix[5, 5],
                    "sig11t": failure_data.max_stress.get('sigma_1t', None),
                    "sig11c": failure_data.max_stress.get('sigma_1c', None),
                    "sig22t": failure_data.max_stress.get('sigma_2t', None),
                    "sig22c": failure_data.max_stress.get('sigma_2c', None),
                    "tau12": failure_data.max_stress.get('sigma_12', None),
                    "tau23": failure_data.max_stress.get('sigma_23', None),
                    "maxStrain": failure_data.max_strain.get('epsilon_1t', None),
                }
            elif isinstance(material, Orthotropic):
                return {
                    'name': material.name,
                    'density': material.density,
                    "k11": material.stiffness_matrix[0, 0],
                    "k12": material.stiffness_matrix[0, 1],
                    "k13": material.stiffness_matrix[0, 2],
                    "k22": material.stiffness_matrix[1, 1],
                    "k23": material.stiffness_matrix[1, 2],
                    "k33": material.stiffness_matrix[2, 2],
                    "k44": material.stiffness_matrix[3, 3],
                    "k55": material.stiffness_matrix[4, 4],
                    "k66": material.stiffness_matrix[5, 5],
                    "sig11t": failure_data.max_stress.get('sigma_1t', None),
                    "sig11c": failure_data.max_stress.get('sigma_1c', None),
                    "sig22t": failure_data.max_stress.get('sigma_2t', None),
                    "sig22c": failure_data.max_stress.get('sigma_2c', None),
                    "sig33t": failure_data.max_stress.get('sigma_3t', None),
                    "sig33c": failure_data.max_stress.get('sigma_3c', None),
                    "tau12": failure_data.max_stress.get('sigma_12', None),
                    "tau23": failure_data.max_stress.get('sigma_23', None),
                    "tau13": failure_data.max_stress.get('sigma_13', None),
                    "maxStrain": failure_data.max_strain.get('epsilon_1t', None),
                }
            else:
                raise RuntimeError(f'No write method found for material type "{type(material)}".')
