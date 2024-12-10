import abc
import torch
import torch.nn as nn
from torchlayers.regularization import L1, L2


REGULARIZER_REGISTRY = {"l1": L1, "l2": L2}
