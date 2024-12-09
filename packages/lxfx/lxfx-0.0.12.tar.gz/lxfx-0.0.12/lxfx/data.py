import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from typing import Union
import logging
from pathlib import Path
import matplotlib.pyplot as plt
from statsmodels.tsa import seasonal
import plotly.graph_objects as graph_objects
import plotly.subplots as subplots
import ta
# from ta.trend import 

from lxfx.utils import createLogger, handleExit
from lxfx.metrics import TorchMinMaxScaler, TorchStandardScaler

class TimeSeriesDatasetManager():
    class TimeSeriesDataset(Dataset):
        def __init__(self, data:torch.Tensor,
                     targets:torch.Tensor,
                     model_type = None):
            super().__init__()
            self.data = data 
            self.targets= targets 
            self.model_type = model_type

        def __len__(self):
            return len(self.data)
        
        def __getitem__(self, index):
            seq_data = self.data[index]
            targets = self.targets[index]

            if self.model_type == "FxFCWavenet":
                seq_data = seq_data.reshape(seq_data.size(1), seq_data.size(0))
                # targets = targets.reshape(targets.size(1), targets.size(0))
                targets = targets.squeeze(0)
            return seq_data, targets
        
    def __init__(self, data: Union[torch.Tensor, np.ndarray, pd.DataFrame] = None,
                file_path = None,
                targets:torch.Tensor|np.ndarray = None,
                future_pred_length = 1,
                targetIndices:list = None,
                target_names:list = None,
                drop_names:list = None,
                date_col:str = None,
                sequence_length = 5,
                stride = 1,
                scaler_feature_range = (0,1),
                transform = None,
                use_default_scaler = True,
                split_criterion = (0.7, 0.15, 0.15),
                batchsize = None, 
                to_log_returns = False,
                transform_targets = True,
                manual_seed = None,
                is_autoregressive = False,
                test_sequence_length = 2,
                model_type = None,
                **kwargs):
        """
        Initializes the TimeSeriesDatasetManager with the provided data and parameters.

        Parameters:
            data (torch.Tensor|np.ndarray|pd.DataFrame, optional): The input data for the time series. Defaults to None.
            file_path (str, optional): The file path to load the data from. Defaults to None.
            targets (torch.Tensor|np.ndarray, optional): The target values for the time series. Defaults to None.
            future_pred_length (int, optional): The length of the future predictions. Defaults to 1.
            targetIndices (list, optional): The indices of the target columns. Defaults to None.
            target_names (list, optional): The names of the target columns. Defaults to None.
            drop_names (list, optional): The names of the columns to drop. Defaults to None.
            date_col (str, optional): The name of the date column. Defaults to None.
            sequence_length (int, optional): The length of the sequences to create. Defaults to 5.
            stride (int, optional): The stride between sequences. Defaults to 1.
            scaler_feature_range (tuple, optional): The feature range for the scaler. Defaults to (0, 1).
            transform (callable, optional): The transform to apply to the data. Defaults to None.
            use_default_scaler (bool, optional): Whether to use the default scaler. Defaults to True.
            split_criterion (tuple, optional): The split criterion for train, validation, and test sets. Defaults to (0.7, 0.15, 0.15).
            batchsize (int, optional): The batch size for training. Defaults to None.
            to_log_returns (bool, optional): if true then log returns are to be calculated with a default multiplier of 10000
            transform_targets: Whether or not to transform the targets using the transform or scaler used to transform the data
            manual_seed (int, optional): The manual seed to set for the random number generator. Defaults to None.
            is_autoregressive (bool, optional): Whether the model is autoregressive. Defaults to False.
            test_sequence_length (int, optional): The length of the test sequences to create. Defaults to 2.
            **kwargs: Additional keyword arguments.

        """
        # todo: cater for the data if available instead of just dropping it
        super().__init__()
        self.console_logger = createLogger(is_consoleLogger=True, log_level = logging.WARNING)

        self.manual_seed = manual_seed
        if manual_seed:
            self.set_seed(self.manual_seed)

        self.data = data 
        self.to_log_returns = to_log_returns
        self.targets = targets 
        self.sequenceLength = sequence_length
        self.is_autoregressive = is_autoregressive
        self.test_sequence_length = test_sequence_length
        self.future_pred_length = future_pred_length
        self.data_filepath = file_path
        self.targetIndices = targetIndices
        self.targetNames = target_names
        self.kwargs = kwargs
        self.drop_names = drop_names
        self.date_col_name = date_col
        self.data_column_names = []
        self.target_column_names = []
        self.date_series = None
        self.batchsize = batchsize
        self.stride = stride
        self.test_stride = self.test_sequence_length # This only has impact when the model is flaged autoregressive.
        self.target_dict = {}
        self.use_default_scaler = use_default_scaler
        self.is_data_transformed = False 
        self.is_targets_transformed = False 
        self.scaler_feature_range = scaler_feature_range
        self.transform = transform
        self.model_type = model_type
        if self.transform:
            if self.transform == "z-norm":
                self.transform = TorchStandardScaler()
        self.default_transform = TorchMinMaxScaler(feature_range = self.scaler_feature_range)
        self.df_column_names = []
        self.df = None

        self.getData() # get the data ready

        self.dataset_size = len(self.data)

        self.test_batchsize = 1
        self.train_split = split_criterion[0]
        self.val_split = split_criterion[1]
        self.test_split = split_criterion[2]

        self.train_data = None 
        self.test_data = None 
        self.val_data = None
        self.train_targets = None 
        self.test_targets = None
        self.val_targets = None  
        self.val_end_index = None 
        self.test_start_index = None
        self.transform_targets = transform_targets
        # split the data
        self.splitData()

        self.train_data_seqs = None 
        self.train_eq_target_seqs = None 
        self.test_data_seqs = None 
        self.test_eq_target_seqs = None 
        self.val_data_seqs = None 
        self.val_eq_target_seqs = None 
        self.train_seq_targets = None 
        self.val_seq_targets = None 
        self.test_seq_targets = None
        self.createSequences()

        self.train_dataloader = None
        self.test_dataloader = None 
        self.val_dataloader = None 

        self.generateDataloaders()

    @property
    def model_future_pred_length(self):
        return self.future_pred_length

    @property
    def model_out_features(self):
        if self.model_type == "FxFCWavenet":
            return self.model_num_features
        return self.targets.size(-1)

    @property
    def model_num_features(self):
        return self.data.size(-1)

    @property
    def targets_idx_in_tensor_data(self):
        return [self.data_column_names.index(p) for p in self.target_column_names] if self.model_type == "FxFCWavenet" else None

    @property 
    def targets_idx_in_df(self):
        return [self.df.columns.to_list().index(p) for p in self.target_column_names]

    def config_dict(self):
        """
        Returns a dictionary representation of the instance's attributes.
        """
        return {
            "file_path": self.data_filepath,
            "targetIndices": self.targetIndices,
            "target_names": self.targetNames,
            "drop_names": self.drop_names,
            "date_col": self.date_col_name,
            "sequence_length": self.sequenceLength,
            "stride": self.stride,
            "scaler_feature_range": self.scaler_feature_range,
            "transform": self.transform,
            "use_default_scaler": self.use_default_scaler,
            "split_criterion": (self.train_split, self.val_split, self.test_split),
            "batchsize": self.batchsize,
            "to_log_returns": self.to_log_returns,
            "manual_seed": self.manual_seed,
            "transform_targets": self.transform_targets,
        }
    def printSummary(self, train_only = False, val_only = False,
                     test_only = False, sample_size = 15,
                     seq_sample_size = 3):
        """
        print a summary of what has been done to the data
        """
        summary = {}
        summary["Data loaded from"] = self.data_filepath
        summary["Data columns"] = self.df_column_names
        summary["Target column's'"] = self.target_dict.keys()
        summary["Data shape"] = self.data.shape
        summary["Targets shape"] = self.targets.shape

        summary["split criterion"] = (self.train_split, self.val_split, self.test_split)
        summary["train_data_shape"] = self.train_data.shape
        summary["val_data_shape"] = self.val_data.shape
        summary["test_data_shape"] = self.test_data.shape
        summary["train_targets_shape"] = self.train_targets.shape
        summary["val_targets_shape"] = self.val_targets.shape
        summary["test_targets_shape"] = self.test_targets.shape

        summary["sequence_length"] = self.sequenceLength
        summary["future_pred_length"] = self.future_pred_length
        summary["stride"] = self.stride

        for k, v in summary.items():
            print(f"{k}: {v}")

        print(f"\nData sample_size: {sample_size}")
        print(f"Sequence length: {self.sequenceLength}")
        print(f"Sequence sample_size: {seq_sample_size}")
        
        if train_only:
            print(f"Data : {self.data[:sample_size]}")
            print(f"Train data: {self.train_data[:sample_size]}\n")
            print(f"Train targets: {self.train_targets[:sample_size]}\n")

        if val_only:
            val_start_index = len(self.train_data)
            print(f"Data from val_start_index: {self.data[val_start_index:(val_start_index+5)]}")
            print(f"Val data: {self.val_data[:sample_size]}\n")
            print(f"Val targets: {self.val_targets[:sample_size]}\n")

        if test_only:
            print(f"Data from test_start_index: {self.data[self.test_start_index:(self.test_start_index+15)]}")
            print(f"Test data: {self.test_data[:sample_size]}\n")
            print(f"Test targets: {self.test_targets[:sample_size]}\n")

        print("\tSequences")
        if train_only:
            print(f"Train sequences: {self.train_data_seqs[:seq_sample_size]}")
            print(f"Train sequence targets: {self.train_seq_targets[:seq_sample_size]}\n")
        if val_only:
            print(f"Val sequences: {self.val_data_seqs[:seq_sample_size]}")
            print(f"Val sequence targets: {self.val_seq_targets[:seq_sample_size]}\n")
        if test_only:
            print(f"Test sequences: {self.test_data_seqs[:seq_sample_size]}")
            print(f"Test sequence targets: {self.test_seq_targets[:seq_sample_size]}\n")

        print("\tBatches")
        if train_only:
            print(f"Train batchsize: {self.train_dataloader.batch_size}\n")
        if val_only:
            print(f"Val batchsize: {self.val_dataloader.batch_size}\n")
        if test_only:
            print(f"Test batchsize: {self.test_dataloader.batch_size}\n")

    def processDataFrame(self, df:pd.DataFrame):
        if "index_col" in self.kwargs.keys():
            df = df.reset_index(drop = True) # remove the index column

        # add technical indicators if the data is forex data 
        # if self.to_log_returns:

        if self.date_col_name:
            df[self.date_col_name] = pd.to_datetime(df[self.date_col_name])
            self.date_series = df[self.date_col_name].copy()
        # remove the target columns such that the model does not have to see them.
        # first save them as the target labels 
        if self.targetNames:
            for tN in self.targetNames:
                self.target_dict[tN] = df[tN]
        elif self.targetIndices:
            for tI in self.targetIndices:
                self.target_dict[tI] = df[df.columns[tI]]

        # remove the target columns from the data frame
        if not (self.date_col_name and (len(self.df.columns) == 2)): # there is only a single row of data which is both the target and the feature
            if self.targetIndices:
                if not self.model_type == "FxFCWavenet":
                    [df.drop(columns = df.columns[tI]) for tI in self.targetIndices]
            elif self.targetNames: 
                if not self.model_type == "FxFCWavenet":
                    for tN in self.targetNames:
                        df = df.drop(columns = tN)
            else:
                self.console_logger.error("Neither Target index nor targetNames provided")
                handleExit()
        else:
            self.console_logger.info("Dataframe has only a single feature which is at the same time the target")
        
        # remove any other columns not wanted forexample Date as provided by the user in the drop_names list
        try:
            if self.drop_names:
                for drop_name in self.drop_names: 
                    df = df.drop(columns = drop_name)
        except Exception as e:
            self.console_logger.error(f"Error dropping columns: {e}")
            handleExit()
        # now cater for the targets 
        target_df = pd.DataFrame(self.target_dict)
        # round off the values in the dataframe to 5dps
        df = df.round(5)
        self.df_column_names.extend(df.columns.to_list())
        target_df = target_df.round(5)
        # set the class variables appropriately 
        self.data_column_names = df.columns.copy().to_list()
        self.target_column_names = target_df.columns.copy().to_list()

        self.data = torch.tensor(df.to_numpy(dtype=np.float32), dtype = torch.float32)
        self.targets = torch.tensor(target_df.to_numpy(dtype=np.float32), dtype = torch.float32) if not self.model_type == "FxFCWavenet" else torch.tensor(df.to_numpy(dtype=np.float32), dtype = torch.float32)

    def fetchData(self):
        if self.data_filepath:
            if Path(self.data_filepath).is_file():
                try:
                    index_col = None
                    if "index_col" in self.kwargs.keys():
                        index_col = self.kwargs["index_col"]
                    df = pd.read_csv(self.data_filepath,index_col=index_col)
                    self.df = df.copy()
                except Exception as e:
                    self.console_logger.error(f"Error reading file: {e}")
                    handleExit()
                self.processDataFrame(df)

            else:
                __log = f"File not Found: {self.data_filepath}"
                self.console_logger.error(__log)
                # file_logger.error(__log)
        if isinstance(self.data, pd.DataFrame):
            self.df = self.data.copy()
            self.processDataFrame(self.data)

    def getData(self):
        if self.data_filepath:
            self.fetchData()
        if isinstance(self.data, torch.Tensor):
            pass
        elif isinstance(self.data, pd.DataFrame):
            self.fetchData()

        # Note: by this step all the data is of type np.ndarray

        # calculate the log returns before rescaling the values
        if self.to_log_returns:
            # Calculate log returns for the first three columns and retain the volume column
            if "Volume" in self.drop_names:
                self.data = self.calculateLogReturns(prices=self.data, fx=True)
                self.targets = self.calculateLogReturns(prices=self.targets, fx=True)                
            else:
                log_returns = self.calculateLogReturns(prices=self.data[:, :3], fx=True)
                self.data = torch.column_stack((log_returns, self.data[1:, 3])) 
                self.targets = self.calculateLogReturns(prices=self.targets, fx=True)

    def generateSequences(self, train = False, test= False, val=False):
        data_seqs = []
        eq_target_seqs = []
        target_seqs = []

        sequence_length = self.sequenceLength
        stride =self.stride
        if train:
            data = self.train_data 
            targets = self.train_targets 
        elif test: 
            if self.is_autoregressive:
                if self.test_stride:
                    stride = self.test_stride
                sequence_length = self.test_sequence_length
            data = self.test_data 
            targets = self.test_targets 
        elif val: 
            data = self.val_data
            targets = self.val_targets

        list_data = data.tolist()
        list_targets = targets.tolist()

        for idx in range(0, len(list_data)-sequence_length, stride):
            if idx + sequence_length + self.future_pred_length <= len(list_targets):
                data_seq = list_data[idx:idx+sequence_length]
                eq_target_seq = list_targets[idx:idx+sequence_length]
                target = list_targets[idx+sequence_length:idx+sequence_length+self.future_pred_length]
                data_seqs.append(data_seq)
                eq_target_seqs.append(eq_target_seq)
                target_seqs.append(target) if isinstance(target, list) else target_seqs.append([target])

        # transform the lists into tensors
        data_tensor_seqs = torch.tensor(data_seqs, dtype=torch.float32)
        eq_target_tensor_seqs = torch.tensor(eq_target_seqs, dtype=torch.float32)
        target_tensor_seqs = torch.tensor(target_seqs, dtype=torch.float32)
        return data_tensor_seqs, target_tensor_seqs, eq_target_tensor_seqs

    def showSeriesComponents(self, period, model = "additive", column_name = None,
                             column_idx=None, height = 800):
        """
        Decomposes and visualizes the components of a time series.

        This function decomposes a time series into its observed, trend, seasonal, and residual components
        using seasonal decomposition. It then visualizes these components using a plot with four subplots.

        Parameters:
            period (int): The period for seasonal decomposition.
            model (str): The type of seasonal decomposition model to use. Default is "additive".
            column_name (str): The name of the column in the DataFrame to decompose.
            column_idx (int): The index of the column in the DataFrame to decompose. Default is None.
            height (int): The height of the plot. Default is 800.

        Returns:
        None
        """
        titles = ["observed", "trendComponent", "seasonalComponent", "residualComponent"]
        colors = ["blue", "green", "orange", "red"]
        data = self.df[column_name]
        dc = seasonal.seasonal_decompose(
            data,
            model = model, 
            period = period
        )
        x_axes = self.df.index
        componets = [dc.observed, dc.trend, dc.seasonal, dc.resid]
        fig = subplots.make_subplots(4, 1, shared_xaxes=True, subplot_titles=titles)
        for idx, (cmp, title, color) in enumerate(zip(componets, titles, colors)):
            scatter_trace= graph_objects.Scatter(x = x_axes, y = cmp,
                                                mode="lines", name=title,
                                                line=dict(color=color, width=2))
            fig.add_trace(scatter_trace,row=idx+1,col=1)
        fig.update_layout(height=height, title=f'Decomposed Analysis of {column_name}',    
                  xaxis_title='Date', yaxis_title='Value', showlegend=True)
        fig.show()

    def createSequences(self):
        """
        Create sequences for each of the datasets ie train_data, val_data, test_data
        """
        # generate train_sequences 
        self.train_data_seqs, self.train_seq_targets, self.train_eq_target_seqs = self.generateSequences(train= True)
        self.test_data_seqs, self.test_seq_targets, self.test_eq_target_seqs = self.generateSequences(test= True)
        self.val_data_seqs, self.val_seq_targets, self.val_eq_target_seqs = self.generateSequences(val= True)

    def transformTargets(self, transform):
        if self.is_targets_transformed:
            self.console_logger.info("Targets already transformed. Not transforming")
        else:
            if self.transform_targets:
                # transform the targets using the same transform that was used on the train_data repeat 
                if self.train_data.shape[-1] > 1:
                    num_features = self.train_targets.shape[-1]
                    # Note: tile is used to repeat the targets the number of times as the number of features in the train_data since the transform was fitted on the train_data 
                    if isinstance(self.train_targets, np.ndarray):
                        train_targets_placeholder = np.zeros((self.train_targets.shape[0], 1))
                        val_targets_placeholder = np.zeros((self.val_targets.shape[0], 1))
                        test_targets_placeholder = np.zeros((self.test_targets.shape[0], 1))
                        # concatenate the targets with the placeholder for a specific number of times
                        for i in range(self.train_data.shape[-1] - self.train_targets.shape[-1]):
                            self.train_targets = np.concatenate((self.train_targets, train_targets_placeholder), axis=1)
                            self.val_targets = np.concatenate((self.val_targets, val_targets_placeholder), axis=1)
                            self.test_targets = np.concatenate((self.test_targets, test_targets_placeholder), axis=1)

                        self.train_targets = transform.transform(self.train_targets)[:, 0:(num_features)]
                        self.val_targets = transform.transform(self.val_targets)[:, 0:(num_features)]
                        self.test_targets = transform.transform(self.test_targets)[:, 0:(num_features)]

                    elif isinstance(self.train_targets, torch.Tensor):
                        train_targets_placeholder = torch.zeros(self.train_targets.shape[0], 1)
                        val_targets_placeholder = torch.zeros(self.val_targets.shape[0], 1) 
                        test_targets_placeholder = torch.zeros(self.test_targets.shape[0], 1)
                        # concatenate the targets with the placeholder for a specific number of times
                        for i in range(self.train_data.shape[-1]-self.train_targets.shape[-1]):
                            self.train_targets = torch.cat((self.train_targets, train_targets_placeholder), dim=1)
                            self.val_targets = torch.cat((self.val_targets, val_targets_placeholder), dim=1)
                            self.test_targets = torch.cat((self.test_targets, test_targets_placeholder), dim=1)

                        self.train_targets = transform.transform(self.train_targets)[:,0:(num_features)]
                        self.val_targets = transform.transform(self.val_targets)[:,0:(num_features)]
                        self.test_targets = transform.transform(self.test_targets)[:,0:(num_features)]
                else:
                    self.train_targets = transform.transform(self.train_targets)
                    self.val_targets = transform.transform(self.val_targets)
                    self.test_targets = transform.transform(self.test_targets)

    def transform_data(self):
        # rescale the data

        if self.is_data_transformed == False:
            if self.transform is None:
                if self.use_default_scaler:
                    # fit the transform on the train data and use it to transform the other data
                    self.default_transform.fit(self.train_data)
                    # use the fitted transform to transform even the val and test data
                    self.train_data = self.default_transform.transform(self.train_data)
                    self.val_data = self.default_transform.transform(self.val_data)
                    self.test_data = self.default_transform.transform(self.test_data)

                    self.transformTargets(self.default_transform)

            else:
                    # fit the transform on the train data and use it to transform the other data
                    self.transform = self.transform.fit(self.train_data)
                    # use the fitted transform to transform even the val and test data
                    self.train_data = self.transform.transform(self.train_data)
                    self.val_data = self.transform.transform(self.val_data)
                    self.test_data = self.transform.transform(self.test_data)

                    self.transformTargets(self.transform)

            self.is_data_transfomed = True 
        else:
            self.console_logger.info("Data already transformed. Not transforming ...")

    def splitData(self):
        # note that slicing does not create a copy of the original data it just creates a view
        train_size = int(self.train_split*self.dataset_size)
        val_size = int(self.val_split*self.dataset_size)
        test_size = self.dataset_size - (train_size + val_size)

        if val_size < self.sequenceLength or test_size < self.sequenceLength:
            self.console_logger.error(f"Sequence length  `{self.sequenceLength}` cannot be greater than val `{val_size}` or test `{test_size}` dataset sizes.\nCannot continue ...")
            handleExit()

        self.val_end_index = train_size 
        self.test_start_index = (train_size+val_size)

        self.train_data = self.data[:self.val_end_index]
        self.train_targets = self.targets[:self.val_end_index]

        if val_size != 0:
            self.val_data = self.data[self.val_end_index:self.test_start_index]
            self.val_targets = self.targets[self.val_end_index:self.test_start_index]
        if test_size != 0:
            self.test_data = self.data[self.test_start_index:]
            self.test_targets = self.targets[self.test_start_index:]

        self.transform_data()

    def datasets(self):
        """ 
        Returns:
            train_dataset, val_dataset, test_dataset (all of which are of type 
            torch.utils.data.Dataset)
        """
        self.splitData()
        train_dataset = self.TimeSeriesDataset(self.train_data_seqs, self.train_seq_targets, model_type=self.model_type)
        val_dataset = self.TimeSeriesDataset(self.val_data_seqs, self.val_seq_targets, model_type=self.model_type)
        test_dataset = self.TimeSeriesDataset(self.test_data_seqs, self.test_seq_targets, model_type=self.model_type)
        return train_dataset, val_dataset, test_dataset

    def generateDataloaders(self):
        train_dataset, val_dataset, test_dataset =  self.datasets()
        self.train_dataloader = DataLoader(train_dataset, shuffle = False, batch_size = self.batchsize)
        self.val_dataloader =  DataLoader(val_dataset, shuffle = False, batch_size = self.batchsize)
        self.test_dataloader = DataLoader(test_dataset, shuffle = False, batch_size = self.test_batchsize)

    def dataloaders(self):
        """
        Returns:
            train_dataloader, val_dataloader test_dataloader (all of which are of type
            torch.utils.data.DataLoader)
        """
        return self.train_dataloader, self.val_dataloader, self.test_dataloader
    
    def plotProportionGraph(self, figsize = (10, 10), column_name = None):
        """
        Plots a graph showing the proportions of the train, validation, and test data.
        """
        if (len(self.df.columns) ==2) and self.date_col_name : # we have only a single data column which is at the same time the target
            train_axes = self.train_data
            val_axes = self.val_data
            test_axes = self.test_data
            val_start_index = len(train_axes)
            val_end_index = len(train_axes)+len(val_axes)
            test_end_index = val_end_index+len(test_axes)
        else:
            train_axes = self.train_data[:,1]
            val_axes = self.val_data[:,1]
            test_axes = self.test_data[:,1]
            val_start_index = len(train_axes)
            val_end_index = len(train_axes)+len(val_axes)
            test_end_index = val_end_index+len(test_axes)
        fig  = plt.figure(figsize = figsize)
        axs = fig.add_subplot(1,1,1)
        axs.set_title("Graph showing test val test proportions")
        axs.plot(range(len(train_axes)), train_axes, c = "black", label = "train")
        axs.plot(range(val_start_index, val_end_index), val_axes, c = "green", label = "validation")
        axs.plot(range(val_end_index, test_end_index), test_axes, c = "blue", label = "test")
        axs.grid(True)
        fig.legend()

    def plotSampleColumn(self, column_name,figsize=(6,6)):
        """
        Plots a graph showing a sample of a column from the data.

        Parameters:
            column_name (str): The name of the column to plot.
            figsize (tuple, optional): The size of the figure. Defaults to (6, 6).

        Returns:
            None
        """
        column_name_idx = None
        for idx, cN in enumerate(self.df_column_names):
            if cN == column_name:
                column_name_idx = idx
                break
        if column_name_idx:
            fig = plt.figure(figsize = figsize)
            axs = fig.add_subplot(1,1,1)
            data = self.data[:,column_name_idx]
            axs.plot(data)
        else:
            self.console_logger.error(f"Column name: {column_name} not found")

    def convertLogReturnsToCurPrices(self, prevPrcs = None, log_returns = None, fx=True):
        """
        Converts the log returns to the current prices.

        Parameters:
            prevPrcs: The previous prices
            log_returns: The log returns
            fx: Whether the data is for foreign exchange
        """
        if isinstance(log_returns, np.ndarray):
            log_returns = torch.from_numpy(log_returns)
        if isinstance(prevPrcs, np.ndarray):
            prevPrcs = torch.from_numpy(prevPrcs)
        prices = torch.exp(log_returns) * prevPrcs
        if fx:
            prices = prices*10000
        return prices

    def calculateLogReturns(self, curPrc = None, prevPrc = None, prices = None, fx=True, cum = None):
        """
        Calculates the log returns of a time series.

        Parameters:
            curPrc: The current price
            prevPrc: The previous price
            prices: The prices of the time series
            fx: Whether the data is for foreign exchange
            cum: Whether to calculate the cumulative log returns
        """
        multiplier = 1
        if fx:
            multiplier = 10000
        if curPrc and prevPrc:
            return torch.log((curPrc/prevPrc))*multiplier
        else:
            if isinstance(prices, np.ndarray):
                prices = torch.from_numpy(prices)
                prices = torch.log(prices[1:]/prices[:-1])*multiplier
                return prices.numpy()
            else:
                return torch.log(prices[1:]/prices[:-1])*multiplier

    def inverse_targets(self, targets, transform = None):
        """
        Inverses the targets using the transform that was used to transform the data.

        Parameters:
            targets: The targets to inverse
            transform: The transform that was used to transform the data. Defaults to the default_transform
        """
        if transform is None:
            transform = self.default_transform

        # if self.train_data.shape[-1] > 1:
        #     if isinstance(targets, np.ndarray):
        #         targets = np.expand_dims(transform.inverse_transform(np.tile(targets, self.train_data.shape[-1]))[:,0], axis = 1)
        #     elif isinstance(targets, torch.Tensor):
        #         targets = transform.inverse_transform(targets.repeat(1, self.train_data.shape[-1]))[:,0].unsqueeze(1)
        # else:
        #     targets = transform.inverse_transform(targets)
        
        # transform the targets using the same transform that was used on the train_data repeat 
        if self.train_data.shape[-1] > 1:
            num_features = targets.shape[-1]
            if isinstance(targets, np.ndarray):
                targets_placeholder = np.zeros((targets.shape[0], 1))
                for i in range(self.train_data.shape[-1] - targets.shape[-1]):
                    targets = np.concatenate((targets, targets_placeholder), axis=1)
                targets = transform.inverse_transform(targets)[:, 0:(num_features)]
            elif isinstance(targets, torch.Tensor):
                targets_placeholder = torch.zeros((targets.shape[0], 1))
                for i in range(self.train_data.shape[-1]-targets.shape[-1]):
                    targets = torch.cat((targets, targets_placeholder), dim=1)
                targets = transform.inverse_transform(targets)[:,0:(num_features)]
        else:
            targets = transform.inverse_transform(targets)
        return targets

    def set_seed(self, seed):
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        np.random.seed(seed)

