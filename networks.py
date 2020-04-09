import torch.nn as nn
import torch.nn.functional as F


class MLP(nn.Module):
    def __init__(self, inputdim, outputdim, hiddendim=0):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(inputdim, outputdim)
        # self.fc2 = nn.Linear(5, 5)

    def forward(self, din):
        # din = din.view(-1, 28 * 28)
        h1 = F.relu(self.fc1(din))
        # dout = F.relu(self.fc2(h1))
        return h1  # F.softmax(dout)
