import torch
import torch.nn as nn
import numpy as np

class RMSELoss(nn.Module):
    def __init__(self, eps = 1e-6):
        super(RMSELoss, self).__init__()
        self.mse = nn.MSELoss()
        self.eps = eps

    def forward(self, pred, true):
        loss = torch.sqrt(self.mse(pred, true)+self.eps)
        return loss

class TorchMinMaxScaler:
    def __init__(self, feature_range=(0, 1)):
        self.min = None
        self.max = None
        self.scale = None
        self.min_range, self.max_range = feature_range

    def fit(self, data):
        # Ensure data is a 2D PyTorch tensor
        if isinstance(data, np.ndarray):
            data = torch.tensor(data, dtype=torch.float32)
        if data.dim() == 1:
            data = data.unsqueeze(1)
        
        # Calculate the min and max for each feature
        self.min = data.min(dim=0, keepdim=True).values
        self.max = data.max(dim=0, keepdim=True).values
        self.scale = (self.max_range - self.min_range) / (self.max - self.min)

    def transform(self, data):
        return (data - self.min) * self.scale + self.min_range

    def inverse_transform(self, data):
        return (data - self.min_range) / self.scale + self.min

class TorchStandardScaler:
    def __init__(self):
        self.mean = None 
        self.std = None 

    def fit(self, data):
        self.mean = data.mean(dim = 0, keepdim = True)
        self.std = data.std(dim = 0, keepdim = True, unbiased = False)

    def transform(self, data):
        return (data-self.mean)/self.std
    
    def inverse_transform(self, data):
        return data*self.std + self.mean

def MAPE(y_pred, y_true):
    """This function implements the mean absolute percentage error accuracy where we are just
    trying to see how well the predicted value corresponds to the true value.
    Parameters:
        y_pred: predicted value 
        y_true: true value 
    Returns:
        a float representing the percentage accuracy
    """
    return 1-torch.mean(torch.abs((y_true - y_pred)/y_true))