import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas


class VkDataset(Dataset):
    def __init__(self):
        clear_dataset()
        xy = np.loadtxt('datasets/for_model.csv', delimiter=',', dtype=np.float64, skiprows=1)
        self.x = torch.from_numpy(np.delete(xy, 8, 1))
        self.y = torch.from_numpy(xy[:, [8]])
        self.n_samples = xy.shape[0]
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]
    
    def __len__(self):
        return self.n_samples
    

def clear_dataset():
    df = pandas.read_csv('datasets/10Kflat.csv')
    df.drop(['id'], axis=1, inplace=True)
    df['higher_degree'] = df['higher_degree'].astype(int)
    df['employment'] = df['higher_degree'].astype(int)
    df.fillna(0, inplace=True)
    for index in range(20):
        df.drop([f'friend{index}-id'], axis=1, inplace=True)
        df[f'friend{index}-higher_degree'] = df['higher_degree'].astype(int)
        df[f'friend{index}-employment'] = df['higher_degree'].astype(int)
    df.to_csv('datasets/for_model.csv', index=False)
