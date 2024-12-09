import torch
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from lxfx.data import TimeSeriesDatasetManager

class PredPlotter():
    """
    This handles all instances of plotting predictions in different ways.
    """
    def __init__(self, preds, dataset_manager:TimeSeriesDatasetManager,
                 autoreg_batch_plots:bool = False, test_only:bool = False, 
                 length:int = None, show_gridlines = True, interactive_cursor = True,
                 figsize = (6,6), test_plots = 1, is_production = False):
        self.is_production = is_production
        self.preds = preds
        self.dataset_manager = dataset_manager
        self.autoreg_batch_plots = autoreg_batch_plots
        self.test_plots = test_plots
        self.test_only = test_only
        self.length = length
        self.show_gridlines = show_gridlines
        self.interactive_cursor = interactive_cursor

        self.figsize = figsize
        self.figure = plt.figure(figsize = self.figsize)
        self.num_rows = self.test_plots
        self.idx_count = 0

        self.initialize_data()

        self.plot_train_targets = None
        self.plot_val_targets = None
        self.plot_test_data = None
        self.plot_pred_data = None

        self.train_y_axes = None 
        self.val_y_axes = None 
        self.test_prev_y_axes = None
        self.model_feed_seq_y_axes = None
        self.true_pred_y_axes = None
        self.pred_y_axes = None

        self.train_x_axes = None
        self.val_x_axes = None
        self.test_x_axes = None
        self.test_prev_x_axes = None
        self.model_feed_seq_x_axes = None
        self.true_pred_x_axes = None
        self.pred_x_axes = None

        self.val_start_index = None
        self.val_end_index = None
        self.test_start_index = None
        self.test_end_index = None
        self.test_prev_start_index = None 
        self.test_prev_end_index = None 
        self.model_feed_seq_start_index = None 
        self.model_feed_seq_end_index = None 
        self.true_pred_start_index = None 
        self.true_pred_end_index = None
        self.pred_start_index = None
        self.pred_end_index = None

        self.plot_test_prev = None 
        self.plot_model_feed_seq = None 
        self.plot_true_pred = None

    def initialize_data(self):
        self.train_targets = self.dataset_manager.train_targets
        self.val_targets = self.dataset_manager.val_targets
        self.test_data = self.dataset_manager.test_targets
        self.test_eq_target_seqs = self.dataset_manager.test_eq_target_seqs
        self.test_target_seqs = self.dataset_manager.test_seq_targets
        self.transform = self.dataset_manager.transform if self.dataset_manager.transform is not None else self.dataset_manager.default_transform

        if self.dataset_manager.model_type == "FxFCWavenet":
            train_targets = []
            val_targets = []
            test_targets = []
            test_eq_target_seqs = []
            test_target_seqs = []
            for idx in self.dataset_manager.targets_idx_in_tensor_data:
                train_targets.append(self.train_targets[:, idx])
                val_targets.append(self.val_targets[:, idx])
                test_targets.append(self.test_data[:, idx])
                test_eq_target_seqs.append(self.test_eq_target_seqs[:, :, idx])
                test_target_seqs.append(self.test_target_seqs[:, :, idx])

            self.train_targets = torch.stack(train_targets, dim = 1) # stack in the column dim
            self.val_targets = torch.stack(val_targets, dim = 1)
            self.test_data = torch.stack(test_targets, dim=1)
            self.test_eq_target_seqs = torch.stack(test_eq_target_seqs, dim = 2) # column dim since sequences are of shape (num_seqs, data_len, n_features)
            self.test_target_seqs = torch.stack(test_target_seqs, dim = 2)

    def get_prev_batch_time_steps(self, seq_index = None):
        if seq_index > 0:
            additional_seqs = self.test_eq_target_seqs[:seq_index]
        else:
            additional_seqs = []
        return additional_seqs
    
    def get_plot_data(self, preds, seq_index = None, column_idx = 0):
        self.plot_train_targets = self.dataset_manager.inverse_targets(self.train_targets)[:,column_idx]

        self.plot_val_targets = self.dataset_manager.inverse_targets(self.val_targets)[:,column_idx]

        if self.autoreg_batch_plots:
            if seq_index > 0:
                num_prev_test_data_points = self.dataset_manager.test_sequence_length*(seq_index)
                self.plot_test_prev = self.dataset_manager.inverse_targets(self.test_data[:num_prev_test_data_points])[:,column_idx]
            self.plot_model_feed_seq = self.dataset_manager.inverse_targets(self.test_eq_target_seqs[seq_index])[:,column_idx]
            self.plot_true_pred = self.dataset_manager.inverse_targets(self.test_target_seqs[seq_index])[:,column_idx]
        else:
            self.plot_test_data = self.dataset_manager.inverse_targets(self.test_data)[:,column_idx]
        # preds for the column of column index column_idx are the ones provided in the preds parameter
        self.plot_pred_data = self.dataset_manager.inverse_targets(preds)

    def get_y_axes(self):
        self.train_y_axes = self.plot_train_targets 
        self.val_y_axes = self.plot_val_targets

        # length only affects the test data and predictions when not autoregressive
        if not self.autoreg_batch_plots:    
            if self.length is None:
                self.test_y_axes = self.plot_test_data
                self.pred_y_axes = self.plot_pred_data
            else:
                if self.length > len(self.plot_test_data):
                    self.length = len(self.plot_test_data)
                self.test_y_axes = self.plot_test_data[:self.length]
                self.pred_y_axes = self.plot_pred_data[self.dataset_manager.sequenceLength:self.length]
        else:
            # We want to see the whole autoregressive prediction vs the test curve
            if self.plot_test_prev is not None:
                self.test_prev_y_axes = self.plot_test_prev
            self.model_feed_seq_y_axes = self.plot_model_feed_seq
            self.true_pred_y_axes = self.plot_true_pred
            self.pred_y_axes = self.plot_pred_data

    def get_plot_indices(self, seq_idx = 0):
        self.val_start_index = len(self.train_y_axes)
        self.val_end_index = len(self.train_y_axes)+len(self.val_y_axes)
        if self.autoreg_batch_plots:
            if self.plot_test_prev is not None:
                self.test_prev_start_index = self.val_end_index
                self.test_prev_end_index = self.test_prev_start_index+len(self.test_prev_y_axes)
                
                self.model_feed_seq_start_index = self.test_prev_end_index
            else:
                self.model_feed_seq_start_index = self.val_end_index
            self.model_feed_seq_end_index = self.model_feed_seq_start_index+len(self.model_feed_seq_y_axes)

            self.true_pred_start_index = self.model_feed_seq_end_index 
            self.true_pred_end_index = self.true_pred_start_index+len(self.true_pred_y_axes)

            self.pred_start_index = self.true_pred_start_index
            self.pred_end_index = self.pred_start_index + len(self.pred_y_axes)
        else:
            self.test_start_index = self.val_end_index
            self.test_end_index = self.val_end_index+len(self.test_y_axes)
            self.pred_start_index = self.test_start_index + self.dataset_manager.sequenceLength
            self.pred_end_index = self.test_end_index

    def get_x_axes(self):
        self.train_x_axes = range(len(self.train_y_axes))
        self.val_x_axes = range(self.val_start_index, self.val_end_index)
        # if not self.test_only:
            # self.test_x_axes = range(self.val_end_index, self.test_end_index)
        if self.autoreg_batch_plots:
            if self.plot_test_prev is not None:
                self.test_prev_x_axes = range(self.test_prev_start_index, self.test_prev_end_index)
            self.model_feed_seq_x_axes = range(self.model_feed_seq_start_index, self.model_feed_seq_end_index)
            self.true_pred_x_axes = range(self.true_pred_start_index, self.true_pred_end_index)
        else:
            self.test_x_axes = range(self.test_start_index, self.test_end_index)
        self.pred_x_axes = range(self.pred_start_index, self.pred_end_index)
        # else:
        #     self.test_x_axes = range(self.test_start_index, self.test_end_index)
        #     self.pred_x_axes = range(self.pred_start_index, self.test_end_index)

    def plotColumnPreds(self, preds:torch.Tensor, seq_index:int = None,
                        column_idx:int = 0, seq_idx = 0):
        self.get_plot_data(preds, seq_index, column_idx)
        self.get_y_axes()
        self.get_plot_indices(seq_idx)
        self.get_x_axes()

        if isinstance(self.preds, torch.Tensor):
            num_columns = self.preds.shape[-1]
        else:
            num_columns = self.preds[seq_idx].shape[-1]
        self.idx_count += 1
        # Plotting
        # fig = plt.figure(figsize = figsize)
        axs = self.figure.add_subplot(self.num_rows, num_columns, self.idx_count)
        # axs.set_title(f"Predictions for column {self.dataset_manager.df.columns[column_idx]}")

        if not self.test_only:
            axs.plot(self.train_x_axes, self.train_y_axes, c = "black", label = "train")
            axs.plot(self.val_x_axes, self.val_y_axes, c = "green", label = "val")
        if self.autoreg_batch_plots:
            if self.plot_test_prev is not None:
                axs.plot(self.test_prev_x_axes, self.test_prev_y_axes, c = "blue", label = "Test Prev")
            axs.plot(self.model_feed_seq_x_axes, self.model_feed_seq_y_axes, c = "cyan", label = "Seq fed to Model")
            axs.plot(self.true_pred_x_axes, self.true_pred_y_axes, c = "magenta", label = "Actual preds")
        else:
            axs.plot(self.test_x_axes, self.test_y_axes, c = "blue", label = "test")
        axs.plot(self.pred_x_axes, self.pred_y_axes, c = "red", label = "preds")
        axs.set_title(f"{self.dataset_manager.target_column_names[column_idx]}")
        axs.legend()

        if self.interactive_cursor:
            cursor = Cursor(axs, useblit=True, color='red', linewidth=1)
        if self.show_gridlines:
            axs.grid(True)

    def plotAutoRegPreds(self):
        if isinstance(self.preds, list): # We have an autogressive prediction model

            # handle each autoregressive prediction
            for seq_idx, future_preds in enumerate(self.preds):
                if seq_idx >= self.test_plots:
                    break
                # Note: batch dim is at index 0
                future_preds = future_preds.squeeze(0) # remove the batch dimension

                # handle multiple columns
                if future_preds.shape[-1] > 1:
                    for t in range(future_preds.shape[-1]):
                        feature_future_preds = future_preds[:,t].unsqueeze(1)

                        self.plotColumnPreds(feature_future_preds, seq_index = seq_idx,
                                             column_idx = t, seq_idx = seq_idx)
                else:
                    self.plotColumnPreds(future_preds, seq_index=seq_idx)
            plt.show()

    def plotTimeStepPreds(self):
        future_preds = self.preds
        # handle multiple columns
        if future_preds.shape[-1] > 1:
            future_preds = future_preds.squeeze(1)
            for t in range(future_preds.shape[-1]):
                feature_future_preds = future_preds[:,t].unsqueeze(1)
                self.plotColumnPreds(feature_future_preds, column_idx=t)
        else:
            self.plotColumnPreds(future_preds)
        plt.show()

    def plotPredictions(self):
        if isinstance(self.preds, list):
            self.autoreg_batch_plots = True
            self.plotAutoRegPreds()
        else:
            self.autoreg_batch_plots = False
            self.plotTimeStepPreds()