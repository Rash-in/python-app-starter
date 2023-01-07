#!/usr/bin/env python3

import os, sys, argparse
from pathlib import Path
from typing import Union

################################################################################
# ----------------------------- Global Variables ----------------------------- #
################################################################################

file_name = "install_script.py"
script_description = """Script used to create baseline Python application runtime environment for development. 
Creates files/folders inside the specified path, virtual environment creation, and dotenv creation.
Additionally, it creates a file that can be used to run the application in python. Script can be run by
running python against the file directly or further scripts can import the install_app function."""
delimeter = "---"
# ---------------------------------------------------------------------------- #
USER = os.getlogin()
USER_HOME_PATH = os.path.expanduser('~')
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
SCRIPT_PARENT_PATH = os.path.dirname(SCRIPT_PATH)
# ---------------------------------------------------------------------------- #
#runtime_folder = ".env/runtime"
#certs_folder = runtime_folder + "/certs"
#logs_folder = runtime_folder + "/logs"
#pids_folder = runtime_folder + "/pids"
#dotenv_folder = runtime_folder + "/envs"
#app_folders = "src/bin"
# ---------------------------------------------------------------------------- #

################################################################################
# ----------------------------- Helper Functions ----------------------------- #
################################################################################
def validate_path(path: Path) -> bool:
    """Validate if the path exists"""
    if os.path.exists(path):
        return True
    return False
# ---------------------------------------------------------------------------- #
def validate_path_list(path_list: list) -> bool:
    """Validate if paths supplied exist. If any fail, returns False, else return True."""
    for path in path_list:
        if not os.path.exists(path):
            return False
    return True


################################################################################
# ---------------------- Application Directory Functions --------------------- #
################################################################################
def validate_app_dirs(app_path:Path) -> Union[bool, str]:
    """"""
# ---------------------------------------------------------------------------- #
def create_app_dirs(app_path:Path) -> Union[bool, str]:
    """"""
# ---------------------------------------------------------------------------- #


################################################################################
# ------------------------ Runtime Directory Functions ----------------------- #
################################################################################
def create_runtime_dirs(app_path:Path) -> Union[bool, str]:
    """"""
# ---------------------------------------------------------------------------- #


################################################################################
# ----------------------- Virtual Environment Functions ---------------------- #
################################################################################
def validate_venv(app_path: Path) -> Union[bool, str]:
    '''Validate that the .env path exists and that the venv activates'''
    venv_path = os.path.join(app_path, ".env")
    bin_path = os.path.join(venv_path, "bin")
    activate_file_path = os.path.join(bin_path, "activate")
    python_file_path = os.path.join(bin_path, "python3")
    
    # Venv Path Check
    isVenvPathValid = validate_path(path=venv_path)
    if not isVenvPathValid:
        return isVenvPathValid, f"Path Not Found: {venv_path}"
    
    # Bin Path Check
    isBinPathValid = validate_path(path=bin_path)
    if not isBinPathValid:
        return isBinPathValid, f"Path Not Found: {bin_path}"
    
    # Activate File Check
    isActivateFile = os.path.isfile(activate_file_path)
    if not isActivateFile:
        return isActivateFile, f"File Not Found: {activate_file_path}"
    
    # Python File Check
    isPythonFile = os.path.isfile(python_file_path)
    if not isPythonFile:
        return isPythonFile, f"File Not Found: {python_file_path}"
    
    # Activation Check
    try:
        python_verified_path = os.popen(cmd=f"cd {app_path} && . .env/bin/activate && which python3").read()
        if python_file_path == python_verified_path.strip():
            return True, "Virtual Environment activated and executable found"
        else:
            return False, f"Venv paths are not equal\n{python_verified_path}\n{python_file_path}"
    except RuntimeError as ActErr:
        return False, f"Error validating venv activation: {ActErr}"
# ---------------------------------------------------------------------------- #
def create_venv(app_path: Path) -> Union[bool, str]:
    """Creates Python Virtual Environment if it doesn't already exist, then validate it returning the validation results."""
    try:
        os.popen(cmd=f"cd {app_path} && python3 -m venv .env").read()
        isVenvValid, venv_msg = validate_venv(app_path=app_path)
        return isVenvValid, venv_msg
    except RuntimeError as Err:
        return False, f"Error installing venv: {Err}"
# ---------------------------------------------------------------------------- #


################################################################################
# ------------------ Application and Install Path Functions ------------------ #
################################################################################
def create_install_path(install_path: Path) -> Union[bool, str]:
    """Creates install_path if it doesn't already exist and then validates it after creation."""
    try:
        os.makedirs(name=install_path, exist_ok=True)
        installPathValid = validate_path(path=install_path)
        if not installPathValid:
            return False, f"Error validating install_path after creating: {install_path}"
        else:
            return True, f"Install Path created and validated"
    except RuntimeError as Err:
        return False, f"Error creating install_path: {Err}"
# ---------------------------------------------------------------------------- #
def create_app_path(app_path: Path):
    """Creates app_path if it doesn't already exist and then validates it after creation."""
    try:
        os.makedirs(name=app_path, exist_ok=True)
        appPathValid = validate_path(path=app_path)
        if not appPathValid:
            return False, f"Error validating app_path after creating: {app_path}"
        else:
            return True, "App Path created and validated"
    except RuntimeError as Err:
        return False, f"Error creating app_path: {Err}"
# ---------------------------------------------------------------------------- #


################################################################################
# ------------------------ User Information Functions ------------------------ #
################################################################################
def verify_input(app_name: str, install_path: Path, app_path: Path) -> Union[bool, str]:
    """Verifies with the user that the parsed information is correct."""
    print(f"\nApplication Name: {app_name}")
    print(f"Install Path: {install_path}")
    print(f"Application Path: {app_path}")
    input_verification = input(f"\n\nARE YOU SURE THIS IS CORRECT???? Please verify with y/n: ")
    if input_verification.lower() == 'y':
        return True, "Verified"
    if input_verification.lower() == 'n':
        return False, "User selected Not Verified. Exiting Script..."
    return False, "Input not recognized. Exiting Script..."
# ---------------------------------------------------------------------------- #
def augment_input(app: str, path: str) -> Union[bool, str, str, Path, Path]:
    """Converts User input to use formatted syntax and paths to an official Path type"""
    done=False
    formatted_app_name = app.replace(" ", "-").lower()
    msg = "Formatted"
    if path.startswith("/"):
        formatted_app_name = app.replace(" ", "-").lower()
        formatted_install_path = Path(path)
        formatted_app_path = os.path.join(formatted_install_path, formatted_app_name)
        done=True
    elif path.startswith("./"):
        formatted_app_name = app.replace(" ", "-").lower()
        join_path = os.path.join(SCRIPT_PATH, path)
        formatted_install_path = Path(join_path)
        formatted_app_path = os.path.join(formatted_install_path, formatted_app_name)
        done=True
    elif path.startswith("../"):
        formatted_app_name = app.replace(" ", "-").lower()
        join_path = os.path.join(SCRIPT_PARENT_PATH, path)
        formatted_install_path = Path(join_path)
        formatted_app_path = os.path.join(formatted_install_path, formatted_app_name)
        done=True
    elif path.startswith("~"):
        formatted_app_name = app.replace(" ", "-").lower()
        refactor_path = path.replace("~", os.path.expanduser('~'))
        formatted_install_path = Path(refactor_path)
        formatted_app_path = os.path.join(formatted_install_path, formatted_app_name)
        done=True
    else:
        msg = f"Unable to parse Install Path provided: {path}"
        formatted_app_name = None
        formatted_install_path = None
        formatted_app_path = None
        done=False

    return done, msg, formatted_app_name, formatted_install_path, formatted_app_path
# ---------------------------------------------------------------------------- #

def intro() -> None:
    print(f"""
################################################################################
# ----------------------------- install_script.py ---------------------------- #
################################################################################

IMPORTANT: Do not run this script as Root. It will have unintended consequences.
NOTE: Windows Compatibility is coming in a future release.

Script used to create baseline Python application runtime environment for development. 
Creates files/folders inside the specified path, virtual environment creation, and dotenv creation.
Additionally, it creates a file that can be used to run the application in python. Script can be run by
running python against the file directly or further scripts can import the install_app function.

Enter the data required to proceed
- Application Name: Title of the application being worked on.
- Install Path: Existing path to a folder where the application is being installed.
    a) Example (Not Windows): '/home/{USER}/My Repos/Projects'
    b) Example (Windows): 'C:\\Users\\{USER}\\My Repos\\Projects'
    c) If the path starts with './': it will be replaced by the current script directory
    d) If the path starts with '../': it wil be replaced by the parent directory that the script is located.
    e) If the path starts with '~' it will be replaced by the users home directory + app_name
        - Example: '~' replaced with: '{USER_HOME_PATH}'""")
    return None

################################################################################
# ----------------------- Script Procedures and Runtime ---------------------- #
################################################################################
def install_app() -> Union[bool, str]:
    """Procedures for installation. If importing scripts into an application, import this function."""

    # Step 1: Display intro text and gather user input
    intro()
    app = input("\nEnter an Application Name\n     app_name: ")
    path = input("\nEnter an Install Path\n     install_path: ")

    # Step 2 Format the variables to what is needed.
    isAugmented, augmented_msg, app_name, install_path, app_path = augment_input(app=app, path=path)
    if not isAugmented:
        return isAugmented, augmented_msg

    # Step 3: Verify with User if the input is correct
    verifyInput, verify_msg = verify_input(app_name=app_name, install_path=install_path, app_path=app_path)
    if not verifyInput:
        return verifyInput, verify_msg

    # Step 4: install_path
    isInstallPathValid = validate_path(install_path)
    if isInstallPathValid:
        print("Found install_path before creation")
        pass
    else:
        isInstallPathCreated, create_install_path_msg = create_install_path(install_path=install_path)
        if isInstallPathCreated:
            print("Found install_path after creation")
            pass
        else:
            return isInstallPathCreated, create_install_path_msg

    #Step 5: app_path
    isAppPathValid = validate_path(app_path)
    if isAppPathValid:
        print("Found app_path before creation")
        pass
    else:
        isAppPathCreated, create_app_path_msg = create_app_path(app_path=app_path)
        if isAppPathCreated:
            print("Found app_path after creation")
            pass
        else:
            return isAppPathCreated, create_app_path_msg

    # Step 6: VENV Path
    isVenvValid, venv_msg = validate_venv(app_path=app_path)
    if isVenvValid:
        print("Validated Virtual Environment before creation")
        pass
    else:
        print(venv_msg + "\n\n...Creating new venv")
        isCreateVenv, create_venv_msg = create_venv(app_path=app_path)
        if isCreateVenv:
            print("Validated Virtual Environment after creation")
            pass
        else:
            return isCreateVenv, create_venv_msg

    # Step 7: Runtime Directories
    venv_folder = os.path.join(app_path, ".env")
    runtime_folder = os.path.join(venv_folder, "runtime")
    runtime_dirs = [
        runtime_folder,
        os.path.join(runtime_folder, "certs"),
        os.path.join(runtime_folder, "logs"),
        os.path.join(runtime_folder, "pids"),
        os.path.join(runtime_folder, "envs")
    ]
#LEFT OFF HERE. NEED TO VERIFY WORKING
    isRuntimeDirs= validate_path_list(runtime_dirs)
    if isRuntimeDirs:
        print("Validated runtime directories before creation.")
        pass
    else:
        isRuntimeDirsCreated, runtime_dirs_msg = create_runtime_dirs(runtime_dirs=runtime_dirs)
        if isRuntimeDirsCreated:
            print("Validated runtime directories after creation")
            pass
        else:
            return isRuntimeDirsCreated, runtime_dirs_msg


################################################################################
# ------------------------------ Script Runtime ------------------------------ #
################################################################################
#Script when called directly through this file does not require arguments.
# These objects are needed to display the help screen and error out if any
#   arguments are input by the user aside from the help option/long option.
parser = argparse.ArgumentParser(
    prog=file_name,
    description=script_description,
    epilog=delimeter
)
args = parser.parse_args()
# ---------------------------------------------------------------------------- #
def main() -> str:
    '''Execution function. Hit when file is called directly in python.'''
    isInstalled, installation_msg = install_app()
    sys.exit(f"Install Compete?: {isInstalled}; Msg: {installation_msg}")
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    main()
# ---------------------------------------------------------------------------- #

# EOF