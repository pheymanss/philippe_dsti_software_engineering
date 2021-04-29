import importlib.util
import subprocess
import sys

def precheck_single_import(pkg):
    """Checks if the provided package is present in the given environment, and
    if not, attempts to perform an installation.

    Args:
        pkg (str): Name of the python package.
    """
    spec = importlib.util.find_spec(pkg)
    if spec is None:
        print(f"Package '{pkg}' is required but not present in current environment. Attempting installation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print('Package installation succesful.')
        
def precheck_imports(pkgs):
    """Reviews that a list of packages are all installed in the given 
    environment, and if not, attempts to perform an installation of the missing 
    ones.  

    Args:
        pkgs ([str]): A list of package names to check.
    """
    for pk in pkgs:
        precheck_single_import(pk)