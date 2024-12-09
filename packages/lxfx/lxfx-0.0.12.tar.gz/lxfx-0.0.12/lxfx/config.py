import json
import os
import logging

from lxfx.utils import createLogger

class XFXConfig:
    """
    This class generates the configuration data for the XFX model.
    Configure the model that is going to be instantiated by the XFX class. This can be either of the following:
    1. FxFCModel
    2. FxFCEncoder
    3. FxFCDecoder
    4. FxFCAutoEncoder
    Specify the model type by the model_type parameter in the XFX class and the class shall
    automatically load the appropriate configuration data and model for that type.
    If the project directory specified is already an XFX project then it is loaded as a project with
    existing configurations, models and all information saved during the previous runs.
    """
    def __init__(self, dump_dir = None, config_file_path = None, config_file_name = None):
        self.console_logger = createLogger(is_consoleLogger=True, log_level=logging.ERROR)
        self.dump_dir = dump_dir
        self.config_file_path = config_file_path
        self.config_file_name = config_file_name
        self.supported_model_types = ["FCBlock", "FxFCModel", "FxFCEncoder", "FxFCDecoder", "FxFCAutoEncoder", "FxFCWavenet"]
        self.FCBlock_model_config = {
                "in_features": None,
                "hidden_size": None,
                "out_size": None,
                "nature": "lstm",
                "dropout": 0.2,
                "num_layers": 1,
                "bidirectional": False,
                "activation": "tanh",
                "use_batch_norm": False,
                "pass_block_hidden_state": False
        }
        self.FXFCAutoEncoder_model_config = {
                "future_pred_length": 1,
                "block_types": ["lstm", "lstm"],
                "comment0": "The current configuration requires that the hidden size of the last layer of the encoder and the first layer of the decoder are the same.",
                "units": [[], []],
                "comment1": "Once the out_units is set then pass_block_hidden_states must be false beucase the first layer shall have a hidden state whose shape is different from the next layer's hidden state shape",
                "out_units": [[], []],
                "num_layers": [1, 1],
                "activations": ["tanh", "tanh"],
                "latent_dim": 32,
                "dropout": [0.2, 0.2],
                "bidirectional": [False, False],
                "use_batch_norm": [False, False],
                "pass_states": [True, True],
                "pass_block_hidden_state": [False, False],
                "is_attentive": False
        }
        self.FXFCModel_model_config = {
                "block_type": "lstm",
                "units": None,
                "comment0": "The length of the units array is equal to the number or fxfc blocks",
                "num_layers": 1,
                "comment1": "The number of out_units MUST be equal to the number of units",
                "out_units": None,
                "comment2": "Once the out_units is set then pass_block_hidden_states must be false beucase the first layer shall have a hidden state whose shape is different from the next layer's hidden state shape",
                "activation": "tanh",
                "bidirectional": False,
                "pass_states": False,
                "comment": "use_batch_norm is a MUST if the data is forex data",
                "use_batch_norm": False,
                "pass_block_hidden_state": False
        }
        self.FXFCEncoder_model_config = {
                "block_type": None,
                "units": None,
                "out_units": None,
                "num_layers": 1,
                "activation": "tanh",
                "latent_dim": None,
                "use_batch_norm": False,
                "bidirectional": False
        }
        self.FXFCDecoder_model_config = {
                "latent_dim": None,
                "block_type": None,
                "units": None,
                "out_units": None,
                "num_layers": 1,
                "activation": "tanh",
                "use_batch_norm": False,
                "initialize_weights": False,
                "initializer_method": None
        }

        self.FXFCWavenet_model_config = {
            "kernel_size":2,
            "dense_in_units": [],
            "dense_out_units": [],
            "skip_size":None,
            "blocks_per_layer":3,
            "wall_num_layers":1,
            "num_walls":1,
            "map_skip_connections":False,
            "concat_skip_connections":False,
            "apply_res":True,
            "apply_skip":True,
            "activation_func":"tanh"
        }

        self.models_config = {
            "FCBlock": self.FCBlock_model_config,
            "FxFCModel": self.FXFCModel_model_config,
            "FxFCEncoder": self.FXFCEncoder_model_config,
            "FxFCDecoder": self.FXFCDecoder_model_config,
            "FxFCAutoEncoder": self.FXFCAutoEncoder_model_config,
            "FxFCWavenet":self.FXFCWavenet_model_config
        }

        self.config_dict = {
            "TimeSeriesDatasetManager": {
                "file_path": None,
                "future_pred_length": 1,
                "targetIndices": None,
                "target_names": [],
                "drop_names": [],
                "date_col": None,
                "sequence_length": 5,
                "test_sequence_length": 2,
                "is_autoregressive": False,
                "stride": 1,
                "scaler_feature_range": [0, 1],
                "transform": None,
                "use_default_scaler": True,
                "split_criterion": [0.7, 0.15, 0.15],
                "batchsize": None,
                "to_log_returns": False,
                "transform_targets": True,
                "index_col": None,
                "manual_seed": 42
            },
            "ModelTrainer": {
                "loss_fn": "mse",
                "optmizer": "adam",
                "epochs": 3,
                "accuracy_fn": None,
                "lr": 0.001,
                "project_path": None,
                "is_logging": True,
                "resume": False,
                "targets_transformed": False, 
                "clip_grads": True
            },
            "TensorInitializer": {
                "method": None
            }
        }

    def get_config_dict(self):
        return self.config_dict

    def dump_config(self, model_type = None): # Write the dictionary to a JSON file
        if model_type in self.supported_model_types:
            filepath = None
            if self.dump_dir:
                filepath = os.path.join(self.dump_dir, "config.json")
            elif self.config_file_path:
                filepath = self.config_file_path
            elif self.config_file_name:
                filepath = os.path.join(os.getcwd(), self.config_file_name)

            dump_config_dict= self.config_dict

            dump_config_dict[model_type] = self.models_config[model_type]
            if filepath is not None:
                with open(filepath, 'w') as json_file:
                    json.dump(dump_config_dict, json_file, indent=4)
            else:
                return dump_config_dict
        else:
            self.console_logger.error(f"Model type '{model_type}' not in supported model types")