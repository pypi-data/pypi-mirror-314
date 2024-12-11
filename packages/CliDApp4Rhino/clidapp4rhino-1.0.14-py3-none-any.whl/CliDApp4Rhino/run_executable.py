"""Module to run the executable file"""
import platform
import subprocess

import pkg_resources


def main():
    """Function to run the executable file."""
    # Determine the user's operating system
    os_name = platform.system()

    # Get appropriate executable file based on the user's operating system
    if os_name == "Windows":
        executable_name = "CliDApp4Rhino.exe"
    else:
        executable_name = "CliDApp4Rhino"
    # Get the path to the executable file
    executable_path = pkg_resources.resource_filename("CliDApp4Rhino", executable_name)
    # Run the executable file
    subprocess.run([executable_path])
    # Add a print statement to indicate completion
    print(
        f"{executable_name} has been run successfully. Open Rhino to use the" " plugin."
    )
