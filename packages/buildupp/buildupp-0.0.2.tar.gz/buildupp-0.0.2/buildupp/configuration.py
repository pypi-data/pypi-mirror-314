import configparser
import os
import sys
import importlib
import pandas as pd

import buildupp


class UserNotFoundError(AttributeError):
    pass


class Config:

    def __init__(self, config_dir: str = os.path.join(buildupp.PROJECT_ROOT, "config")):

        self.config_dir = config_dir
        self.paths_file = os.path.join(self.config_dir, "paths.py")

        # Dynamically load paths.py file
        self.data_root_directory, self.desktop_directory = self.load_paths()

        # Dynamically load .py files
        self.user_functions = self.load_user_functions()
        self.systems_measured = self.load_systems_measured()
        self.colors = self.load_colors()

        # load chemistry data
        self.chemistry_database = config_dir + "/chemistry_database.ini"
        self.chemdat_dict = self.load_chemistry_database()

        # load powder properties
        self.powder_properties = self.load_powder_properties()

    def load_paths(self):
        """Dynamically loads paths.py and retrieves the data root and desktop directories for the current user."""

        if not os.path.isfile(self.paths_file):
            raise FileNotFoundError(f"File {self.paths_file} not found.")

        # Dynamically load the paths.py file
        spec = importlib.util.spec_from_file_location("paths", self.paths_file)
        paths_module = importlib.util.module_from_spec(spec)
        sys.modules["paths"] = paths_module
        spec.loader.exec_module(paths_module)

        data_root = paths_module.data_root_directory
        desktop = paths_module.desktop_directory

        return data_root, desktop

    def load_colors(self):
        """Dynamically loads the colors.py file from the config directory."""
        colors_file = os.path.join(self.config_dir, "colors.py")

        if not os.path.isfile(colors_file):
            raise FileNotFoundError(f"File {colors_file} not found.")

        # Dynamically load the colors.py file
        spec = importlib.util.spec_from_file_location("colors", colors_file)
        colors_module = importlib.util.module_from_spec(spec)
        sys.modules["systems_measured"] = colors_module
        spec.loader.exec_module(colors_module)

        return colors_module

    def load_systems_measured(self):
        """Dynamically loads the systems_measured.py file from the config directory."""
        systems_measured_file = os.path.join(self.config_dir, "systems_measured.py")

        if not os.path.isfile(systems_measured_file):
            raise FileNotFoundError(f"File {systems_measured_file} not found.")

        # Dynamically load the systems_measured.py file
        spec = importlib.util.spec_from_file_location(
            "systems_measured", systems_measured_file
        )
        systems_measured_module = importlib.util.module_from_spec(spec)
        sys.modules["systems_measured"] = systems_measured_module
        spec.loader.exec_module(systems_measured_module)

        return systems_measured_module

    def load_chemistry_database(self):
        """Loads the INI database into a dictionary."""
        config = configparser.ConfigParser()
        config.read(self.chemistry_database)

        chemdat_dict = {}
        for section in config.sections():
            compound_data = {}
            for key in config[section]:
                try:
                    # Try to convert values to float if possible
                    compound_data[key] = (
                        float(config[section][key])
                        if "." in config[section][key]
                        else int(config[section][key])
                    )
                except ValueError:
                    # If it's not a number, store as a string (e.g., reference)
                    compound_data[key] = config[section][key]
            chemdat_dict[section] = compound_data

        return chemdat_dict  # This returns the dictionary so it can be assigned to self.chemdat_dict

    def load_powder_properties(self):
        """
        Load powder properties from a Python file (physical_properties.py) in the config directory.
        Returns a dictionary of powder properties, where each powder is a key.
        """

        properties_file = os.path.join(self.config_dir, "physical_properties.py")

        if not os.path.isfile(properties_file):
            raise FileNotFoundError(
                f"{properties_file} not found in the config directory."
            )

        # Dynamically load the Python file as a module
        spec = importlib.util.spec_from_file_location(
            "physical_properties", properties_file
        )
        physicalties_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(physicalties_module)

        physical_properties = getattr(physicalties_module, "physical_properties", {})

        # Check if the dictionary exists in the file
        if not physical_properties:
            raise ValueError(
                "No properties dictionary found in the physical_properties.py file."
            )

        return physical_properties

    def load_user_functions(self):
        """Dynamically loads user-defined functions for reading PSD data."""
        user_functions_file = os.path.join(self.config_dir, "user_functions.py")

        if not os.path.isfile(user_functions_file):
            raise FileNotFoundError(f"File {user_functions_file} not found.")

        # Dynamically load the user functions file (user_functions.py)
        spec = importlib.util.spec_from_file_location(
            "user_functions", user_functions_file
        )
        user_functions_module = importlib.util.module_from_spec(spec)
        sys.modules["user_functions"] = user_functions_module
        spec.loader.exec_module(user_functions_module)

        return user_functions_module

    def get_psd_data(self, material: str):
        """Retrieve the PSD data as a pandas DataFrame for a given material."""
        if material not in self.powder_properties:
            raise ValueError(f"Material {material} not found in powder properties.")

        # Fetch the PSD file path and reader function name from powder_properties
        psd_path = self.powder_properties[material].get("psd_file")
        reader_function_name = self.powder_properties[material].get(
            "psd_reader_function"
        )

        if not psd_path or not reader_function_name:
            raise ValueError(
                f"Missing PSD path or reader function for material {material}."
            )

        # Get the reader function dynamically from the user_functions module
        reader_function = getattr(self.user_functions, reader_function_name, None)

        if not reader_function:
            raise AttributeError(
                f"Reader function {reader_function_name} not found in user_functions.py."
            )

        psd_df = reader_function(psd_path)

        if not isinstance(psd_df, pd.DataFrame):
            raise TypeError(
                f"Reader function {reader_function_name} did not return a pandas DataFrame."
            )

        return psd_df
