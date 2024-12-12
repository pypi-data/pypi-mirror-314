from ..bin._validate import _validateArguments,_validateCommand
from subprocess import run
from ..bin.exceptions import UnknownCommand

def baxh(command,arguments):
    _runCommand = run([command],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
    _runCommandArgument = run([command,arguments],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
    print(_validateArguments(arguments))
    if _validateCommand(command):
        raise UnknownCommand(command)
    # if _validateArguments(arguments):
    #     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #     return _runCommandArgument
    # return _runCommand