from .baxh import baxh
from .bazh import bazh
from .powershell import powershell

def _bajh(command,arguments,shell):
    if shell == "batch":
        return baxh(command,arguments)
    if shell == "bash":
        return bazh(command,arguments)
    if shell == "powershell":
        return powershell(command,arguments)