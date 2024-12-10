from typing import Callable, Optional, Tuple, Union, Literal, List, Mapping, Any
from ._config import load_config
import torch.nn as nn
from pathlib import Path
import os
HERE = Path(__file__).parent


def DeepSTARR(
    input_len: int,
    output_dim: int,
) -> nn.Module:
    """Build a DeepSTARR model

    Parameters
    ----------
    input_len : int
        The length of the input sequence
    output_dim : int
        The number of output units

    Returns
    -------
    nn.Module
        A DeepSTARR model
    """
    config = os.path.join(HERE, "cre_activity_predictors", "deepstarr.yaml")
    model = load_config(config, **dict(input_len=input_len, output_dim=output_dim))
    return model


def DeepSEA(
    input_len: int,
    output_dim: int,
) -> nn.Module:
    """Build a DeepSEA model

    Parameters
    ----------
    input_len : int
        The length of the input sequence
    output_dim : int
        The number of output units

    Returns
    -------
    nn.Module
        A DeepSEA model
    """
    config = os.path.join(HERE, "regulatory_classifiers", "deepsea.yaml")
    model = load_config(config, **dict(input_len=input_len, output_dim=output_dim))
    return model
