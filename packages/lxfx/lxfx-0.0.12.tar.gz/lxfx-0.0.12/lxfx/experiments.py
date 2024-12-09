"""
This module contains classes and functions for running automated experiments and also for 
optimizing hyperparameters using custom methods and other methods like the optuna module for 
optimizing hyperparameters.
"""

import logging
import optuna
from lxfx.utils import createLogger, handleExit
from lxfx.xfx import XFX

import json
import os

class XFXExperiment():
    def __init__(self):
        pass
    
    def run(self):
        pass

class XFXOptunaExperiment():
    """
    This class uses Optuna to tune hyperparameters such as learning rate, number of layers, layer hidden sizes, optimizer, etc.
    To flag a parameter as tunable by Optuna, replace its value in the config file or config dict with a dict:
    {
        "tune": true,
        "data_type": data_type,
        "value_range": [val_1, val_2]
    }
    If a parameter is not flagged as tunable, its default value will be used.
    """
    def __init__(self, n_trials = 10,
                 n_epochs = 10,
                 config_file_path = None, 
                 config_dict = None, 
                 model_type = None):
        
        self.console_logger = createLogger(is_consoleLogger=True, log_level=logging.INFO)

        self.study = optuna.create_study(direction = "minimize")
        self.n_trials = n_trials
        self.n_epochs = n_epochs

        self.config_file_path = config_file_path 
        self.config_dict = config_dict
        self.load_config_dict()

        self.model_type = model_type 
        if self.model_type is None:
            self.console_logger("Model type not set. Cannot continue ...")
            handleExit()


        self.tunable_parameters = {}
        self.get_tunable_parameters()

        self.xfx_project = None

    def load_config_dict(self):
        try:
            if not self.config_dict:
                if self.config_file_path and os.path.exists(self.config_file_path):
                    with open(self.config_file_path, 'r') as file:
                        self.config_dict = json.load(file)
                else:
                    self.console_logger.error(f"File: {self.config_file_path} not found")
                    handleExit()
        except json.JSONDecodeError as e:
            self.console_logger.error(f"JSON decode error: {str(e)}")
            handleExit()
        except FileNotFoundError as e:
            self.console_logger.error(f"File not found: {str(e)}")
            handleExit()
        except Exception as e:
            self.console_logger.error(f"An unexpected error occurred while loading the config dict: {str(e)}")
            handleExit()
        if self.config_dict is None:
            self.console_logger.error("Config dict is empty. Cannot continue ...")
            handleExit()

    def get_param_dict(self, value, section, param):
        try:
            param_dict = {
                "section": section,
                "data_type": value.get("data_type"),
                "value_range": value.get("value_range"),
                "idx": None,  # Default value for idx
                "nested":False
            }
            if param_dict["data_type"] is None or param_dict["value_range"] is None:
                raise ValueError(f"Parameter {param} in section {section} is missing 'data_type' or 'value_range'.")
            return param_dict
        except Exception as e:
            self.console_logger.error(f"Error in get_param_dict for parameter {param}: {str(e)}")
            handleExit()

    def get_tunable_parameters(self):
        try:
            for section, section_dict in self.config_dict.items():
                if not isinstance(section_dict, dict):
                    self.console_logger.error(f"Section {section} is not a dictionary.")
                    continue
                for param, value in section_dict.items():
                    if isinstance(value, dict) and value.get("tune"):
                        self.tunable_parameters[param] = self.get_param_dict(value, section, param)
                    elif isinstance(value, list):
                        for idx, val in enumerate(value):
                            if isinstance(val, dict) and val.get("tune"):
                                param_dict = self.get_param_dict(val, section, param)
                                param_dict["idx"] = idx
                                self.tunable_parameters[param] = param_dict
                            # this is the maximum number of nested lists the config can have
                            elif isinstance(val, list):
                                for nested_idx, nested_val in enumerate(val):
                                    if isinstance(nested_val, dict) and nested_val.get("tune"):
                                        param_dict = self.get_param_dict(nested_val, section, param)
                                        param_dict["idx"] = nested_idx
                                        param_dict["nested"] = True
                                        param_dict["parent_idx"] = idx  # Index of the nested list in the first list
                                        self.tunable_parameters[param] = param_dict

        except Exception as e:
            self.console_logger.error(f"An error occurred while getting tunable parameters: {str(e)}")
            handleExit()

    def objective(self, trial: optuna.Trial):
        try:
            for param, param_dict in self.tunable_parameters.items():
                if param_dict["data_type"] == "float":
                    param_dict["value"] = trial.suggest_float(param, param_dict["value_range"][0], param_dict["value_range"][1])
                elif param_dict["data_type"] == "int":
                    param_dict["value"] = trial.suggest_int(param, param_dict["value_range"][0], param_dict["value_range"][1])
                elif param_dict["data_type"] == "categorical":
                    param_dict["value"] = trial.suggest_categorical(param, param_dict["value_range"])
                
                # change the value in the config dict
                if param_dict["idx"] is None:
                    self.config_dict[param_dict["section"]][param] = param_dict["value"]
                elif param_dict["nested"] is True:
                    self.config_dict[param_dict["section"]][param][param_dict["parent_idx"]][param_dict["idx"]] = param_dict["value"]
                else:
                    self.config_dict[param_dict["section"]][param][param_dict["idx"]] = param_dict["value"]

            # Open an XFX project for each trial
            self.xfx_project = XFX(_config_dict=self.config_dict, model_type=self.model_type)
            return self.xfx_project.train(epochs=self.n_epochs, tuna_exp=True)
        except Exception as e:
            self.console_logger.error(f"An error occurred in the objective function: {str(e)}")
            handleExit()

    def run(self):
        try:
            self.get_tunable_parameters()
            self.study.optimize(self.objective, n_trials=self.n_trials)
        except Exception as e:
            self.console_logger.error(f"An error occurred during the optimization run: {str(e)}")
            handleExit()