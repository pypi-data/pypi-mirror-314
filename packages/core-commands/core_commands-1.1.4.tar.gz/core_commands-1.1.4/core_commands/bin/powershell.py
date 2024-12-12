from subprocess import run
from ._validate import _validateArguments

def powershell(command,arguments):
        full_command=None
        if _validateArguments(arguments):
                full_command = f"{command} {arguments}"
                return run(["powershell", "-Command", full_command],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
        full_command = command
        return run(["powershell", "-Command", full_command],
                    capture_output=True,
                    text=True,
                    shell=True
                    )