import os

# Default to None for PROJECT_ROOT
PROJECT_ROOT = None

def find_git_repo_with_config(start_dir=None):
    """
    Searches upwards from the specified directory to find the first Git repository
    containing a 'config' directory. Raises FileNotFoundError if no such repository is found.
    """
    if start_dir is None:
        start_dir = os.getcwd()  # Default to the current working directory

    current_dir = start_dir
    while current_dir != os.path.dirname(current_dir):  # Stop when reaching the root directory
        git_dir = os.path.join(current_dir, '.git')
        config_dir = os.path.join(current_dir, 'config')
        
        # Check if both .git and 'config' directories exist
        if os.path.isdir(git_dir) and os.path.isdir(config_dir):
            return current_dir
        
        current_dir = os.path.dirname(current_dir)  # Move up one level

    # Raise error if no matching repository is found
    raise FileNotFoundError("No project root found (git repository containing the 'config' directory).")

# Try to set PROJECT_ROOT automatically
try:
    PROJECT_ROOT = find_git_repo_with_config()
    print(f"PROJECT_ROOT is {PROJECT_ROOT}")

except FileNotFoundError as e:
    # Handle the case when automatic discovery fails
    print(e)

    # Prompt the user to manually enter the project root directory
    PROJECT_ROOT = input("Enter the path to the project root (where .git and config directories are located): ").strip()

    # Check if the user entered a valid path
    if os.path.isdir(PROJECT_ROOT) and os.path.isdir(os.path.join(PROJECT_ROOT, '.git')) and os.path.isdir(os.path.join(PROJECT_ROOT, 'config')):
        print(f"PROJECT_ROOT is set to: {PROJECT_ROOT}")
    else:
        print(f"The directory you entered is not valid. Please ensure it contains a .git directory and a 'config' directory.")
        # You could raise an error or re-prompt the user here
        raise ValueError(f"Invalid project root: {PROJECT_ROOT}")

# Import package components after PROJECT_ROOT is set
from .experiment import Experiment
from .blend import Blend
from .configuration import Config
from .hydration import Hydration

# Now you can safely create your config
config = Config()
