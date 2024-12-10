import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from typing import Union, Callable, Optional, Any, Tuple, List, Dict
from ._construct import build_conv1d_tower, build_recurrent_block, build_mha_layer, build_dense_tower


class CNN(nn.Module):
    """Basic convolutional network

    Instantiate a CNN model with a set of convolutional layers and a set of fully
    connected layers.

    By default, this architecture passes the one-hot encoded sequence through a set
    1D convolutions with 4 channels followed by a set of fully connected layers.

    Parameters
    ----------
    input_len:
        The length of the input sequence.
    output_dim:
        The dimension of the output.
    conv_kwargs:
        The keyword arguments for the convolutional layers. These come from the
        models.Conv1DTower class. See the documentation for that class for more
        information on what arguments are available.
    dense_kwargs:
        The keyword arguments for the fully connected layer. If not provided, the
        default passes the flattened output of the convolutional layers directly to
        the output layer. These come from the models.DenseBlock class. See the
        documentation for that class for more information on what arguments are
        available.
    """
    def __init__(
        self,
        input_len: int,
        output_dim: Optional[int] = None,
        conv1d_tower_params: Optional[Dict[str, Union[List, str]]] = None,
        dense_tower_params: Optional[Dict[str, Union[List, str]]] = None,
        conv1d_tower_conv_channels: Optional[Union[List, str]] = None,
        conv1d_tower_conv_kernels: Optional[Union[List, str]] = None,
        conv1d_tower_conv_types: Optional[Union[List, str]] = "conv1d",
        conv1d_tower_conv_strides: Optional[Union[List, str]] = 1,
        conv1d_tower_conv_paddings: Optional[Union[List, str]] = "valid",
        conv1d_tower_conv_dilations: Optional[Union[List, str]] = 1,
        conv1d_tower_conv_biases: Optional[Union[List, str]] = True,
        conv1d_tower_conv_activations: Optional[Union[List, str]] = "relu",
        conv1d_tower_pool_types: Optional[Union[List, str]] = "max",
        conv1d_tower_pool_kernels: Optional[Union[List, str]] = 1,
        conv1d_tower_pool_strides: Optional[Union[List, str]] = None,
        conv1d_tower_pool_paddings: Optional[Union[List, str]] = 0,
        conv1d_tower_norm_types: Optional[Union[List, str]] = "batchnorm",
        conv1d_tower_norm_dims: Optional[Union[List, str]] = None,
        conv1d_tower_dropout_rates: Optional[Union[List, str]] = 0.0,
        conv1d_tower_residuals: Optional[Union[List, str]] = False,
        conv1d_tower_orders: Optional[Union[List, str]] = "conv-act-pool-dropout-norm",
        dense_tower_hidden_dims: Union[List, str] = [],
        dense_tower_biases: Optional[Union[List, str]] = True,
        dense_tower_activations: Optional[Union[List, str]] = "relu",
        dense_tower_dropout_rates: Optional[Union[List, str]] = 0.0,
        dense_tower_norm_types: Optional[Union[List, str]] = "batchnorm",
        dense_tower_norm_dims: Optional[Union[List, str]] = None,
        dense_tower_orders: Optional[Union[List, str]] = "linear-act-dropout-norm",
        model_name: str = "cnn",
    ):
        super(CNN, self).__init__()

        # Set the attributes
        self.input_len = input_len
        self.output_dim = output_dim
        self.model_name = model_name
        self.conv1d_tower_params = {
            "conv_channels": conv1d_tower_conv_channels,
            "conv_kernels": conv1d_tower_conv_kernels,
            "conv_types": conv1d_tower_conv_types,
            "conv_strides": conv1d_tower_conv_strides,
            "conv_paddings": conv1d_tower_conv_paddings,
            "conv_dilations": conv1d_tower_conv_dilations,
            "conv_biases": conv1d_tower_conv_biases,
            "activations": conv1d_tower_conv_activations,
            "pool_types": conv1d_tower_pool_types,
            "pool_kernels": conv1d_tower_pool_kernels,
            "pool_strides": conv1d_tower_pool_strides,
            "pool_paddings": conv1d_tower_pool_paddings,
            "norm_types": conv1d_tower_norm_types,
            "norm_dims": conv1d_tower_norm_dims,
            "dropout_rates": conv1d_tower_dropout_rates,
            "residuals": conv1d_tower_residuals,
            "orders": conv1d_tower_orders,
        }
        if conv1d_tower_params is not None:
            self.conv1d_tower_params.update(conv1d_tower_params)
        if conv1d_tower_params is not None:
            self.conv1d_tower_params.update(conv1d_tower_params)
        assert (
            self.conv1d_tower_params["conv_channels"] is not None
        ), "Must specify number of conv_channels in either 'conv1d_tower_params' or 'conv1d_tower_conv_channels'"
        assert (
            self.conv1d_tower_params["conv_kernels"] is not None
        ), "Must specify number of conv_kernels in either 'conv1d_tower_params' or 'conv1d_tower_conv_kernels'"
        self.dense_block_params = {
            "hidden_dims": dense_tower_hidden_dims,
            "biases": dense_tower_biases,
            "activations": dense_tower_activations,
            "dropout_rates": dense_tower_dropout_rates,
            "norm_types": dense_tower_norm_types,
            "norm_dims": dense_tower_norm_dims,
            "orders": dense_tower_orders,
        }
        if dense_tower_params is not None:
            self.dense_block_params.update(dense_tower_params)
            
        # Construct the conv tower
        self.conv1d_tower = build_conv1d_tower(
            input_len=input_len,
            conv1d_tower_params=self.conv1d_tower_params,
        )
        self.flatten_dim = int(np.prod(self.conv1d_tower.output_size))
        
        # Get to output_dim through dense tower
        if self.output_dim is not None:
            # Flatten the output
            self.flatten = nn.Flatten(1, -1)

            # Construct the dense tower
            self.dense_block = build_dense_tower(
                input_size=self.flatten_dim,
                output_dim=self.output_dim,
                dense_tower_params=self.dense_block_params,
            )

    def forward(self, x):
        x = self.conv1d_tower(x)
        if self.output_dim is not None:
            x = self.flatten(x)
            x = self.dense_block(x)
        return x
  

class Hybrid(nn.Module):
    """Basic Hybrid network

    A hybrid model that uses both a CNN and an RNN to extract features then passes the
    features through a set of fully connected layers.

    By default, the CNN is used to extract features from the input sequence, and the RNN is used to
    to combine those features. The output of the RNN is passed to a set of fully connected
    layers to make the final prediction.

    Parameters
    ----------
    input_len:
        The length of the input sequence.
    output_dim:
        The dimension of the output.
    conv_kwargs:
        The keyword arguments for the convolutional layers. These come from the
        models.Conv1DTower class. See the documentation for that class for more
        information on what arguments are available.
    recurrent_kwargs:
        The keyword arguments for the recurrent layers. These come from the
        models.RecurrentBlock class. See the documentation for that class for more
        information on what arguments are available.
    dense_kwargs:
        The keyword arguments for the fully connected layer. These come from
        the models.DenseBlock class. See the documentation for that class for
        more information on what arguments are available.
    """
    def __init__(
        self,
        input_len: int,
        output_dim: Optional[int] = None,
        conv1d_tower_params: Optional[Dict[str, Union[List, str]]] = None,
        recurrent_block_params: Optional[Dict[str, Union[List, str]]] = None,
        recurrent_block_hidden_dim: int = None,
        recurrent_block_num_layers: int = 1,
        recurrent_block_unit_type: str = "lstm",
        recurrent_block_bidirectional: bool = False,
        recurrent_block_dropout_rates: float = 0.0,
        recurrent_block_biases: bool = True,
        recurrent_block_batch_first: bool = True,
        dense_tower_params: Optional[Dict[str, Union[List, str]]] = None,
        conv1d_tower_conv_channels: Optional[Union[List, str]] = None,
        conv1d_tower_conv_kernels: Optional[Union[List, str]] = None,
        conv1d_tower_conv_types: Optional[Union[List, str]] = "conv1d",
        conv1d_tower_conv_strides: Optional[Union[List, str]] = 1,
        conv1d_tower_conv_paddings: Optional[Union[List, str]] = "valid",
        conv1d_tower_conv_dilations: Optional[Union[List, str]] = 1,
        conv1d_tower_conv_biases: Optional[Union[List, str]] = True,
        conv1d_tower_conv_activations: Optional[Union[List, str]] = "relu",
        conv1d_tower_pool_types: Optional[Union[List, str]] = "max",
        conv1d_tower_pool_kernels: Optional[Union[List, str]] = 1,
        conv1d_tower_pool_strides: Optional[Union[List, str]] = None,
        conv1d_tower_pool_paddings: Optional[Union[List, str]] = 0,
        conv1d_tower_norm_types: Optional[Union[List, str]] = "batchnorm",
        conv1d_tower_norm_dims: Optional[Union[List, str]] = None,
        conv1d_tower_dropout_rates: Optional[Union[List, str]] = 0.0,
        conv1d_tower_residuals: Optional[Union[List, str]] = False,
        conv1d_tower_orders: Optional[Union[List, str]] = "conv-act-pool-dropout-norm",
        dense_tower_hidden_dims: Union[List, str] = [],
        dense_tower_biases: Optional[Union[List, str]] = True,
        dense_tower_activations: Optional[Union[List, str]] = "relu",
        dense_tower_dropout_rates: Optional[Union[List, str]] = 0.0,
        dense_tower_norm_types: Optional[Union[List, str]] = "batchnorm",
        dense_tower_norm_dims: Optional[Union[List, str]] = None,
        dense_tower_orders: Optional[Union[List, str]] = "linear-act-dropout-norm",
        model_name: str = "hybrid",
    ):
        super(Hybrid, self).__init__()

        # Set the attributes
        self.input_len = input_len
        self.output_dim = output_dim
        self.model_name = model_name
        self.conv1d_tower_params = {
            "conv_channels": conv1d_tower_conv_channels,
            "conv_kernels": conv1d_tower_conv_kernels,
            "conv_types": conv1d_tower_conv_types,
            "conv_strides": conv1d_tower_conv_strides,
            "conv_paddings": conv1d_tower_conv_paddings,
            "conv_dilations": conv1d_tower_conv_dilations,
            "conv_biases": conv1d_tower_conv_biases,
            "activations": conv1d_tower_conv_activations,
            "pool_types": conv1d_tower_pool_types,
            "pool_kernels": conv1d_tower_pool_kernels,
            "pool_strides": conv1d_tower_pool_strides,
            "pool_paddings": conv1d_tower_pool_paddings,
            "norm_types": conv1d_tower_norm_types,
            "norm_dims": conv1d_tower_norm_dims,
            "dropout_rates": conv1d_tower_dropout_rates,
            "residuals": conv1d_tower_residuals,
            "orders": conv1d_tower_orders,
        }
        if conv1d_tower_params is not None:
            self.conv1d_tower_params.update(conv1d_tower_params)
        assert (
            self.conv1d_tower_params["conv_channels"] is not None
        ), "Must specify number of conv_channels in either 'conv1d_tower_params' or 'conv1d_tower_conv_channels'"
        assert (
            self.conv1d_tower_params["conv_kernels"] is not None
        ), "Must specify number of conv_kernels in either 'conv1d_tower_params' or 'conv1d_tower_conv_kernels'"
        self.recurrent_block_params = {
            "hidden_dim": recurrent_block_hidden_dim,
            "num_layers": recurrent_block_num_layers,
            "unit_type": recurrent_block_unit_type,
            "bidirectional": recurrent_block_bidirectional,
            "dropout_rates": recurrent_block_dropout_rates,
            "bias": recurrent_block_biases,
            "batch_first": recurrent_block_batch_first,
        }
        if recurrent_block_params is not None:
            self.recurrent_block_params.update(recurrent_block_params)
        assert (
            self.recurrent_block_params["hidden_dim"] is not None
        ), "Must specify hidden_dim in either 'recurrent_block_params' or 'recurrent_block_hidden_dim'"
        self.dense_block_params = {
            "hidden_dims": dense_tower_hidden_dims,
            "biases": dense_tower_biases,
            "activations": dense_tower_activations,
            "dropout_rates": dense_tower_dropout_rates,
            "norm_types": dense_tower_norm_types,
            "norm_dims": dense_tower_norm_dims,
            "orders": dense_tower_orders,
        }
        if dense_tower_params is not None:
            self.dense_block_params.update(dense_tower_params)
        
        # Construct the conv tower
        self.conv1d_tower = build_conv1d_tower(
            input_len=input_len,
            conv1d_tower_params=self.conv1d_tower_params,
        )
        
        # Construct the recurrent block
        self.recurrent_block = build_recurrent_block(
            input_dim=self.conv1d_tower.output_size[0],
            recurrent_block_params=self.recurrent_block_params,
        )
        
        # Get to output_dim through dense tower
        if self.output_dim is not None:            
            self.dense_block = build_dense_tower(
                input_size=self.recurrent_block.out_channels,
                output_dim=self.output_dim,
                dense_tower_params=self.dense_block_params,
            )
        
    def forward(self, x):
        x = self.conv1d_tower(x).transpose(1, 2)
        out, _ = self.recurrent_block(x)
        if self.output_dim is not None:
            out = out[:, -1, :]
            out = self.dense_block(out)
        return out

 
class Transformer(nn.Module):
    def __init__(
        self,
        input_len: int,
        output_dim: Optional[int] = None,
        conv1d_tower_params: Optional[Dict[str, Union[List, str]]] = None,
        mha_layer_params: Optional[Dict[str, Union[List, str]]] = None,
        mha_layer_head_dim: Optional[Union[List, str]] = None,
        mha_layer_num_heads: Optional[Union[List, str]] = 1,
        mha_layer_dropout_rate: Optional[Union[List, str]] = 0.0,
        dense_tower_params: Optional[Dict[str, Union[List, str]]] = None,
        conv1d_tower_conv_channels: Optional[Union[List, str]] = None,
        conv1d_tower_conv_kernels: Optional[Union[List, str]] = None,
        conv1d_tower_conv_types: Optional[Union[List, str]] = "conv1d",
        conv1d_tower_conv_strides: Optional[Union[List, str]] = 1,
        conv1d_tower_conv_paddings: Optional[Union[List, str]] = "valid",
        conv1d_tower_conv_dilations: Optional[Union[List, str]] = 1,
        conv1d_tower_conv_biases: Optional[Union[List, str]] = True,
        conv1d_tower_conv_activations: Optional[Union[List, str]] = "relu",
        conv1d_tower_pool_types: Optional[Union[List, str]] = "max",
        conv1d_tower_pool_kernels: Optional[Union[List, str]] = 1,
        conv1d_tower_pool_strides: Optional[Union[List, str]] = None,
        conv1d_tower_pool_paddings: Optional[Union[List, str]] = 0,
        conv1d_tower_norm_types: Optional[Union[List, str]] = "batchnorm",
        conv1d_tower_norm_dims: Optional[Union[List, str]] = None,
        conv1d_tower_dropout_rates: Optional[Union[List, str]] = 0.0,
        conv1d_tower_residuals: Optional[Union[List, str]] = False,
        conv1d_tower_orders: Optional[Union[List, str]] = "conv-act-pool-dropout-norm",
        dense_tower_hidden_dims: Union[List, str] = [],
        dense_tower_biases: Optional[Union[List, str]] = True,
        dense_tower_activations: Optional[Union[List, str]] = "relu",
        dense_tower_dropout_rates: Optional[Union[List, str]] = 0.0,
        dense_tower_norm_types: Optional[Union[List, str]] = "batchnorm",
        dense_tower_norm_dims: Optional[Union[List, str]] = None,
        dense_tower_orders: Optional[Union[List, str]] = "linear-act-dropout-norm",
        model_name: str = "hybrid",
    ):
        super(Transformer, self).__init__()

        # Set the attributes
        self.input_len = input_len
        self.output_dim = output_dim
        self.model_name = model_name
        self.conv1d_tower_params = {
            "conv_channels": conv1d_tower_conv_channels,
            "conv_kernels": conv1d_tower_conv_kernels,
            "conv_types": conv1d_tower_conv_types,
            "conv_strides": conv1d_tower_conv_strides,
            "conv_paddings": conv1d_tower_conv_paddings,
            "conv_dilations": conv1d_tower_conv_dilations,
            "conv_biases": conv1d_tower_conv_biases,
            "activations": conv1d_tower_conv_activations,
            "pool_types": conv1d_tower_pool_types,
            "pool_kernels": conv1d_tower_pool_kernels,
            "pool_strides": conv1d_tower_pool_strides,
            "pool_paddings": conv1d_tower_pool_paddings,
            "norm_types": conv1d_tower_norm_types,
            "norm_dims": conv1d_tower_norm_dims,
            "dropout_rates": conv1d_tower_dropout_rates,
            "residuals": conv1d_tower_residuals,
            "orders": conv1d_tower_orders,
        }
        if conv1d_tower_params is not None:
            self.conv1d_tower_params.update(conv1d_tower_params)
        assert (
            self.conv1d_tower_params["conv_channels"] is not None
        ), "Must specify number of conv_channels in either 'conv1d_tower_params' or 'conv1d_tower_conv_channels'"
        assert (
            self.conv1d_tower_params["conv_kernels"] is not None
        ), "Must specify number of conv_kernels in either 'conv1d_tower_params' or 'conv1d_tower_conv_kernels'"
        self.mha_layer_params = {
            "head_dim": mha_layer_head_dim,
            "num_heads": mha_layer_num_heads,
            "dropout_rate": mha_layer_dropout_rate,
        }
        if mha_layer_params is not None:
            self.mha_layer_params.update(mha_layer_params)
        assert (
            self.mha_layer_params["head_dim"] is not None
        ), "Must specify head_dim in either 'mha_layer_params' or 'mha_layer_head_dim'"
        self.dense_block_params = {
            "hidden_dims": dense_tower_hidden_dims,
            "biases": dense_tower_biases,
            "activations": dense_tower_activations,
            "dropout_rates": dense_tower_dropout_rates,
            "norm_types": dense_tower_norm_types,
            "norm_dims": dense_tower_norm_dims,
            "orders": dense_tower_orders,
        }
        if dense_tower_params is not None:
            self.dense_block_params.update(dense_tower_params)
        
        # Construct the conv tower
        self.conv1d_tower = build_conv1d_tower(
            input_len=input_len,
            conv1d_tower_params=self.conv1d_tower_params,
        )
        
        # Construct the mha layer
        self.mha_layer = build_mha_layer(
            input_dim=self.conv1d_tower.output_size[-1],
            mha_layer_params=self.mha_layer_params,
        )
        
        # Get to output_dim through dense tower
        if self.output_dim is not None:
            self.flatten = nn.Flatten(1, -1)          
            self.dense_block = build_dense_tower(
                input_size=int(np.prod(self.conv1d_tower.output_size)),
                output_dim=self.output_dim,
                dense_tower_params=self.dense_block_params,
            )
        
    def forward(self, x):
        x = self.conv1d_tower(x)
        x = self.mha_layer(x)
        if self.output_dim is not None:
            x = self.flatten(x)
            x = self.dense_block(x)
        return x
   