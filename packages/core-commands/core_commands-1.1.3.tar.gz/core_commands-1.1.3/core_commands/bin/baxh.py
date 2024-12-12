from ..bin._validate import _validateArguments,_validateCommand
from subprocess import run
from ..bin.exceptions import UnknownCommand

def baxh(command,arguments):
    print(_validateArguments(arguments))
    if _validateCommand(command):
        raise UnknownCommand(command)
    if _validateArguments(arguments):
        return run([command,arguments],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
    return run([command],
                    capture_output=True,
                    text=True,
                    shell=True
                    )