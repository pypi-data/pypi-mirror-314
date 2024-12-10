import yaml
from ..base._architectures import CNN, Hybrid, Transformer
import torch.nn as nn
from typing import Union, List, Mapping, Callable, Literal, Tuple
from os import PathLike


def load_cnn_config(
    config_path: Union[str, PathLike],
    **kwargs,
) -> nn.Module:

    # Read the config file
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Grab the globals
    if "model_name" in config:
        print(f"Loading {config['model_name']}")
        model_name = config.pop("model_name")
    else:
        print("No model name specified. Using 'model'")
        model_name = "model"
    if "input_len" in config:
        input_len = config.pop("input_len")
        if "input_len" in kwargs:
            input_len = kwargs.pop("input_len")
    else:
        raise ValueError("'input_len' must be specified in config")
    if "output_dim" in config:
        output_dim = config.pop("output_dim")
        if "output_dim" in kwargs:
            output_dim = kwargs.pop("output_dim")
    if "arch" in config:
        arch_params = config.pop("arch")
    else:
        raise ValueError("'arch' must be specified in config")
    
    # Parse arch parameters
    if "conv1d_tower" in arch_params:
        conv1d_tower_params = arch_params.pop("conv1d_tower")
    else:
        raise ValueError("'conv1d_tower' must be specified in config")
    if "dense_tower" in arch_params:
        dense_tower_params = arch_params.pop("dense_tower")

    # Update with kwargs
    conv1d_tower_params.update(kwargs)

    # Build CNN
    arch = CNN(
        input_len=input_len,
        output_dim=output_dim,
        conv1d_tower_params=conv1d_tower_params,
        dense_tower_params=dense_tower_params,
        model_name=model_name,
    )

    return arch


def load_hybrid_config(
    config_path: Union[str, PathLike],
    **kwargs,
) -> nn.Module:
    
        # Read the config file
        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    
        # Grab the globals
        if "model_name" in config:
            print(f"Loading {config['model_name']}")
            model_name = config.pop("model_name")
        else:
            print("No model name specified. Using 'model'")
            model_name = "model"
        if "input_len" in config:
            input_len = config.pop("input_len")
            if "input_len" in kwargs:
                input_len = kwargs.pop("input_len")
        else:
            raise ValueError("'input_len' must be specified in config")
        if "output_dim" in config:
            output_dim = config.pop("output_dim")
            if "output_dim" in kwargs:
                output_dim = kwargs.pop("output_dim")
        if "arch" in config:
            arch_params = config.pop("arch")
        else:
            raise ValueError("'arch' must be specified in config")
        
        # Parse arch parameters
        if "conv1d_tower" in arch_params:
            conv1d_tower_params = arch_params.pop("conv1d_tower")
        else:
            raise ValueError("'conv1d_tower' must be specified in config")
        if "dense_tower" in arch_params:
            dense_tower_params = arch_params.pop("dense_tower")
        if "recurrent_block" in arch_params:
            recurrent_block_params = arch_params.pop("recurrent_block")
        if "dense_tower" in arch_params:
            dense_tower_params = arch_params.pop("dense_tower")

        # Build CNN
        arch = Hybrid(
            input_len=input_len,
            output_dim=output_dim,
            conv1d_tower_params=conv1d_tower_params,
            recurrent_block_params=recurrent_block_params,
            dense_tower_params=dense_tower_params,
            model_name=model_name,
        )
    
        return arch


def load_transformer_config(
    config_path: Union[str, PathLike],
    **kwargs,
) -> nn.Module:
    
        # Read the config file
        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    
        # Grab the globals
        if "model_name" in config:
            print(f"Loading {config['model_name']}")
            model_name = config.pop("model_name")
        else:
            print("No model name specified. Using 'model'")
            model_name = "model"
        if "input_len" in config:
            input_len = config.pop("input_len")
            if "input_len" in kwargs:
                input_len = kwargs.pop("input_len")
        else:
            raise ValueError("'input_len' must be specified in config")
        if "output_dim" in config:
            output_dim = config.pop("output_dim")
            if "output_dim" in kwargs:
                output_dim = kwargs.pop("output_dim")
        if "arch" in config:
            arch_params = config.pop("arch")
        else:
            raise ValueError("'arch' must be specified in config")
        
        # Parse arch parameters
        if "conv1d_tower" in arch_params:
            conv1d_tower_params = arch_params.pop("conv1d_tower")
        else:
            raise ValueError("'conv1d_tower' must be specified in config")
        if "dense_tower" in arch_params:
            dense_tower_params = arch_params.pop("dense_tower")
        if "mha_layer":
            mha_layer_params = arch_params.pop("mha_layer")
        if "dense_tower" in arch_params:
            dense_tower_params = arch_params.pop("dense_tower")
    
        # Build CNN
        arch = Transformer(
            input_len=input_len,
            output_dim=output_dim,
            conv1d_tower_params=conv1d_tower_params,
            mha_layer_params=mha_layer_params,
            dense_tower_params=dense_tower_params,
            model_name=model_name,
        )
    
        return arch


def load_config(
    config_path: Union[str, PathLike],
    **kwargs,
) -> nn.Module:
    """Load in a torch.nn.Module from a config file

    Parameters
    ----------
    config_path : Union[str, PathLike]
        The path to the config file, must contain a key "arch_name" with
        value "CNN", "Hybrid", or "Transformer"
    
    Returns
    -------
    nn.Module
        The PyTorch model specified in the config file
    """
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        arch_name = config["arch_name"].lower()
    if arch_name == "cnn":
        arch = load_cnn_config(config_path, **kwargs)
    elif arch_name == "hybrid":
        arch = load_hybrid_config(config_path, **kwargs)
    elif arch_name == "transformer":
        arch = load_transformer_config(config_path, **kwargs)
    else:
        raise ValueError(f"Unknown architecture name: {arch_name}")
    return arch
