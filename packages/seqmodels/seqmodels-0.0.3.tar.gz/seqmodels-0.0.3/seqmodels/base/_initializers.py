import torch
import torch.nn as nn
from typing import Dict
import torch.nn.init as init
from .._utils import get_layer
from typing import Union, Callable, Optional, Any, Tuple, List, Literal


INITIALIZERS_REGISTRY = {
    "uniform": init.uniform_,
    "normal": init.normal_,
    "constant": init.constant_,
    "eye": init.eye_,
    "dirac": init.dirac_,
    "xavier_uniform": init.xavier_uniform_,
    "xavier_normal": init.xavier_normal_,
    "kaiming_uniform": init.kaiming_uniform_,
    "kaiming_normal": init.kaiming_normal_,
    "orthogonal": init.orthogonal_,
    "sparse": init.sparse_,
    "ones": init.ones_,
    "zeros": init.zeros_,
}


def _init_weights(
    module: nn.Module,
    initializer: Union[str, Callable],
    **kwargs,
) -> None:
    """Initialize the weights of a module.

    Parameters
    ----------
    module : torch.nn.Module
        The module to initialize.
    initializer : str or callable
        The name of the initializer to use, or the initializer itself as a callable.
    **kwargs
        Additional arguments to pass to the initializer.
    """
    if initializer in INITIALIZERS_REGISTRY:
        init_func = INITIALIZERS_REGISTRY[initializer]
    elif callable(initializer):
        init_func = initializer
    else:
        raise ValueError(
            f"Initializer {initializer} not found in INITIALIZER_REGISTRY or is not callable."
        )
    if isinstance(module, nn.Linear) or isinstance(module, nn.Conv1d):
        init_func(module.weight)
    elif isinstance(module, nn.ParameterList):
        for param in module:
            if param.dim() > 1:
                init_func(param)


def init_weights(
    model: nn.Module,
    initializer: Union[str, Callable] = "kaiming_normal",
    **kwargs,
) -> None:
    """Initialize the weights of a model.

    Parameters
    ----------
    model : LightningModule
        The model to initialize.
    initializer : str or callable, optional
        The name of the initializer to use, or the initializer itself as a callable, by default "kaiming_normal"
    **kwargs
        Additional arguments to pass to the initializer.
    """
    model.apply(lambda m: _init_weights(m, initializer, **kwargs))
