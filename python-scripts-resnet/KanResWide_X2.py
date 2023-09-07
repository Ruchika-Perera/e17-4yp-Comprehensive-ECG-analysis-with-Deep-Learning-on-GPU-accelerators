import torch.nn.functional as F
from KanResInit import KanResInit
from KanResModule import KanResModule
from torch import nn
import torch

class KanResWide_X2(nn.Module):
    def __init__(self, input_shape, output_size):
        super(KanResWide_X2, self).__init__()

        #print(input_shape[0])
        #print(input_shape[1])

        self.input_shape = input_shape
        self.output_size = output_size
        
        self.init_block = KanResInit(input_shape[0], 64, 32, 8, 3, 1)
        self.pool = nn.AvgPool1d(kernel_size=2)
        
        self.module_blocks = nn.Sequential(
            KanResModule(32, 64, 32, 50, 50, 1),
            KanResModule(32, 64, 32, 50, 50, 1),
            KanResModule(32, 64, 32, 50, 50, 1),
            KanResModule(32, 64, 32, 50, 50, 1),
            KanResModule(32, 64, 32, 50, 50, 1),
            KanResModule(32, 64, 32, 50, 50, 1),
            KanResModule(32, 64, 32, 50, 50, 1),
            KanResModule(32, 64, 32, 50, 50, 1)
        )
        
        self.global_avg_pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(32, output_size)
        
    def forward(self, x):
        x = self.init_block(x)
        #print("init block trained")
        #print(x.shape)
        x = self.pool(x)
        #print("pool 1 trained")
        #print(x.shape)
        x = self.module_blocks(x)
        #print("module blocks trained")
        x = self.global_avg_pool(x)
        #print(x.shape)
        x = x.view(x.size(0), -1)
        #q: explain the above line
        #a: it flattens the input
        x = self.fc(x)
        #print(x.shape)
        # squeeze the output
        x = torch.squeeze(x)
        #print(x.shape)
        return x

