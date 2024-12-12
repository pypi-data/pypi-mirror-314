"""A module for interfacing with the mqt-debugger library."""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_debugger.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

from . import dap
from ._version import version as __version__
from .pydebugger import (
    Complex,
    Diagnostics,
    ErrorCause,
    ErrorCauseType,
    SimulationState,
    Statevector,
    Variable,
    VariableType,
    VariableValue,
    create_ddsim_simulation_state,
    destroy_ddsim_simulation_state,
)

__all__ = [
    "Complex",
    "Diagnostics",
    "ErrorCause",
    "ErrorCauseType",
    "SimulationState",
    "Statevector",
    "Variable",
    "VariableType",
    "VariableValue",
    "__version__",
    "create_ddsim_simulation_state",
    "dap",
    "destroy_ddsim_simulation_state",
]
