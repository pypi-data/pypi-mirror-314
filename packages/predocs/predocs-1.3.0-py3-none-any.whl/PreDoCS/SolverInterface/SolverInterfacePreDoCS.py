from typing import Callable

from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverBase
from PreDoCS.WingAnalysis.cpacs_interface_predocs import CPACSInterfacePreDoCS
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)


class PreDoCS_SolverPreDoCS(PreDoCS_SolverBase):
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

    @property
    def _cpacs_interface_class(self) -> type:
        return CPACSInterfacePreDoCS

    @property
    def _get_element_stiffness_func(self) -> Callable:
        return get_stiffness_for_shell
