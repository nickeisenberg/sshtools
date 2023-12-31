from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ..transfer import SecureCopyProtocol
import subprocess
from typing import Optional
import os

p = subprocess.run(
    "pip show pip | awk '/Location/ {print $2}'", 
    shell=True,
    capture_output=True,
    text=True
)
PATH_TO_SSHTOOLS = os.path.join(
    p.stdout.strip(),
    "sshtools"
)
PLOTTING_SCRIPT_PATH = os.path.join(PATH_TO_SSHTOOLS, 'plotting', 'scripts')

def start_trigger(
        path_to_image_folder: str, 
        path_to_bash: Optional[str]=None
        ):

    """
    Initiates a trigger using a Bash script.

    Parameters
    ----------
    - path_to_image_folder: str 
        Path to the folder containing images.
    - path_to_bash: str, optional
        Path to the Bash script to be triggered. Needs to be set if `pyaws` 
        is not in `site-packages`

    Note
    ----
    The function will run indefinitely until stopped by the user with <C-c>.
    Upon execution, a message will be displayed indicating the script's running status.

    Example
    -----
    >>> start_trigger('/path/to/my/images')
    Creating the trigger. This will run indefinitely. Use <C-c> to stop
    """

    if path_to_bash is None:
        path_to_bash = os.path.join(
            PLOTTING_SCRIPT_PATH, 'trigger.sh'
        )

    command = [
        path_to_bash,
        "--folder",
        path_to_image_folder
    ]
    
    print("Creating the trigger. This will run indefinatly. Use <C-c> to stop")
    subprocess.run(
        command
    )


class Plotter:

    """
    Parameters
    ----------
        user: str,
        ip: str,
        save_path: str,
        port: str="22", 
        pem: Optional[str]=None,
        path_to_bash: Optional[str]=None
    """

    def __init__(
            self,
            user: str,
            ip: str,
            save_path: str,
            port: str="22", 
            pem: Optional[str]=None,
            path_to_bash: Optional[str]=None
        ):

        self.user = user
        self.ip = ip
        self.save_path = save_path
        self.port = port
        self.pem = pem
        self.path_to_bash = path_to_bash
    

    def show(
        self, 
        name: str, 
        figure: Figure
        ):

        """
        Parameters
        ----------
        name: str 
        figure: matplotlib.figure.Figure
        """
        
        if os.path.isfile(f"./{name}.png"):
            try:
                figure.savefig(f"./___{name}.png")
            except:
                print("file name already exists")
                return None
        else:
            figure.savefig(f"./{name}.png")
        

        scp = SecureCopyProtocol(
            self.user, self.ip, self.port, self.pem, self.path_to_bash
        )

        scp.scp(
            source_path=f"./{name}.png",
            save_path=self.save_path
        )

        os.remove(f"./{name}.png")

        return None
