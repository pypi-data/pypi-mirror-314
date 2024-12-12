from ._validate import _validateArguments
from subprocess import run

def bazh(command,arguments):
    _runCommand = run([command],
                    capture_output=True,
                    text=True
                    )
    _runCommandArgument = run([command,arguments],
                    capture_output=True,
                    text=True
                    )
    if _validateArguments(arguments):
        return _runCommandArgument
    return _runCommand