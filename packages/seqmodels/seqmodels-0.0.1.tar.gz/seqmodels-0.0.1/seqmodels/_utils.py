from typing import Union, Optional, List, Dict, Any, Literal
import torch.nn as nn
import torchinfo

def list(
    registry_key: Literal["activation", "convolutional", "pooling", "normalizer", "loss"],
) -> List[str]:
    """List all available models, layers, or losses
    
    Parameters
    ----------
    registry_key : str
        The type of object to list. Must be one of "convolutional"

    Returns
    -------
    List[str]
        A list of all available models, layers, or losses
    """
    if registry_key == "activation":
        from .base._layers import ACTIVATION_REGISTRY
        return ACTIVATION_REGISTRY.keys()
    elif registry_key == "convolutional":
        from .base._layers import CONVOLUTION_REGISTRY
        return CONVOLUTION_REGISTRY.keys()
    elif registry_key == "pooling":
        from .base._layers import POOLING_REGISTRY
        return POOLING_REGISTRY.keys()
    elif registry_key == "normalizer":
        from .base._layers import NORMALIZER_REGISTRY
        return NORMALIZER_REGISTRY.keys()
    elif registry_key == "loss":
        from .base._losses import LOSS_REGISTRY
        return LOSS_REGISTRY.keys()
    elif registry_key == "metric":
        from .base._metrics import METRIC_REGISTRY
        return METRIC_REGISTRY.keys()
    else:
        raise ValueError(f"registry_key must be one of 'convolutional', got {registry_key} instead")
    
    
def get_output_size(modules, input_size):
    if isinstance(input_size, int):
        input_size = (input_size,)
    summary = torchinfo.summary(
        modules, input_size=(1, *input_size), verbose=0, device="cpu"
    )
    out_size = summary.summary_list[-1].output_size[1:]
    return out_size


def list_available_layers(
    model: nn.Module,
) -> list:
    """List all layers in a model
    
    Parameters
    ----------
    model : nn.Module
        The PyTorch model to list the layers of (nn.Module)

    Returns
    -------
    list
        A list of all layers in the model
    """
    return [name for name, _ in model.named_modules() if len(name) > 0]


def get_layer(
    model: nn.Module,
    layer_name,
) -> Dict[str, nn.Module]:
    """Get a layer from a model by name
    
    Parameters
    ----------
    model : nn.Module
        The PyTorch model to get the layer from
    layer_name : str
        The name of the layer to get
    
    Returns
    -------
    nn.Module
        The layer from the model
    """
    return dict([*model.named_modules()])[layer_name]
