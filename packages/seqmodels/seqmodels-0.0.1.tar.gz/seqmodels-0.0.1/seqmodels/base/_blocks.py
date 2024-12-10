import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Union, Callable, List
from .._utils import get_output_size, list
from . import _layers as layers


class Conv1DBlock(nn.Module):
    """Flexible block for convolutional models

    Allows for flexible specification of convolutional layers, pooling layers,
    normalization layers, activation layers, and dropout layers.

    Parameters
    ----------
    input_len : int
        The length of the input. The last dimension of the input tensor.
    input_channels : int
        The number of input channels. The second to last dimension of the input tensor.
    output_channels : int
        The number of output channels.
    conv_kernel : int
        The size of the convolutional kernel.
    conv_type : str or callable
        The type of convolutional layer to use. If a string, must be a key in
        `sm.list("convolutional")`. If a callable, must be a
        subclass of `torch.nn.Module` and you should still specify the kernel size
        input channels, and output channels.
    conv_stride : int
        The stride of the convolutional kernel.
    conv_padding : str or int
        The padding of the convolutional kernel. See `torch.nn.Conv1d` for more details.
    conv_dilation : int
        The dilation of the convolutional kernel.
    conv_bias : bool
        Whether or not to include a bias term in the convolutional layer.
    activation : str or callable
        The type of activation to use. If a string, must be a key in `sm.list("activation").
        If a callable, must be a subclass of `torch.nn.Module`.
    pool_type : str or callable
        The type of pooling layer to use. If a string, must be a key in
        `sm.list("pooling")`. If a callable, must be a subclass of `torch.nn.Module`.
    pool_kernel : int
        The size of the pooling kernel.
    pool_stride : int
        The stride of the pooling kernel.
    pool_padding : int
        The padding of the pooling kernel.
    norm_type : str or callable
        The type of normalization layer to use. If a string, must be a key in
        `sm.list("normalizer")`. If a callable, must be a subclass of `torch.nn.Module`.
    norm_dim : int
        The dimension to normalize over. If `None`, defaults to the number of output
        channels.
    dropout_rate : float
        The dropout rate to use. If `None`, no dropout is used.
    residual : bool
        Whether or not to use a residual connection.
    order : str
        The order of the layers in the block. Must be a string of the following
        characters: `conv`, `norm`, `act`, `pool`, `dropout`. For example, the string
        `conv-norm-act-pool-dropout` would result in a block with a convolutional layer,
        a normalization layer, an activation layer, a pooling layer, and a dropout layer
        in that order. If `None`, defaults to `conv-norm-act-pool-dropout`.
    """
    def __init__(
        self,
        input_len: int,
        input_channels: int,
        output_channels: int,
        conv_kernel: int,
        conv_type: Union[str, Callable] = "conv1d",
        conv_stride: int = 1,
        conv_padding: Union[str, int] = "valid",
        conv_dilation: int = 1,
        conv_bias: bool = True,
        activation: Union[str, Callable] = "relu",
        pool_type: Union[str, Callable] = "max",
        pool_kernel: int = 1,
        pool_stride: int = None,
        pool_padding: int = 0,
        norm_type: Union[str, Callable] = "batchnorm",
        norm_dim: int = None,
        dropout_rate: float = 0.0,
        residual=False,
        order: str = "conv-norm-act-pool-dropout",
    ):
        super(Conv1DBlock, self).__init__()

        # Define the block's attributes
        self.input_len = input_len
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.conv_kernel = conv_kernel
        self.conv_type = conv_type
        self.conv_stride = conv_stride
        self.conv_dilation = conv_dilation
        self.conv_padding = conv_padding
        self.conv_bias = conv_bias
        self.activation = activation
        self.pool_type = pool_type
        self.pool_kernel = pool_kernel
        self.pool_stride = pool_stride
        self.pool_padding = pool_padding
        self.dropout_rate = dropout_rate
        self.norm_type = norm_type
        self.norm_dim = norm_dim if norm_dim is not None else self.output_channels
        self.residual = residual
        self.order = order

        # Define the conv layer
        if isinstance(self.conv_type, str):
            if self.conv_type in layers.CONVOLUTION_REGISTRY:
                self.conv_type = layers.CONVOLUTION_REGISTRY[conv_type]
                conv = self.conv_type(
                    in_channels=self.input_channels,
                    out_channels=self.output_channels,
                    kernel_size=self.conv_kernel,
                    stride=self.conv_stride,
                    padding=self.conv_padding,
                    dilation=self.conv_dilation,
                    bias=self.conv_bias,
                )
            else:
                raise ValueError("'conv_type' must be one of {}".format(list("convolutional")))
        elif isinstance(self.conv_type, Callable):
            conv = self.conv_type
        else:
            raise ValueError("'conv_type' must be one of 'str' or 'Callable'")

        # Define the norm layer
        if self.norm_type is not None:
            if isinstance(self.norm_type, str):
                if self.norm_type in layers.NORMALIZER_REGISTRY:
                    norm = layers.NORMALIZER_REGISTRY[self.norm_type](self.norm_dim)
                else:
                    raise ValueError("'norm_type' must be one of {}".format(list("normalizer")))
            elif isinstance(self.norm_type, Callable):
                norm = self.norm_type(self.norm_dim)
            else:
                raise ValueError("'norm_type' must be one of 'str' or 'Callable'")
        else:
            norm = self.norm_type

        # Define the activation
        if self.activation is not None:
            if isinstance(self.activation, str):
                if self.activation in layers.ACTIVATION_REGISTRY:
                    activation = layers.ACTIVATION_REGISTRY[self.activation](inplace=False)
                else:
                    raise ValueError("'activation must' be one of {}".format(list("activation")))
            elif isinstance(self.activation, Callable):
                activation = self.activation
            else:
                raise ValueError("'activation' must be one of 'str' or 'Callable'")
        else:
            activation = self.activation

        # Define the pooling layer
        if self.pool_type is not None:
            if isinstance(self.pool_type, str):
                if self.pool_type in layers.POOLING_REGISTRY:
                    pool = layers.POOLING_REGISTRY[self.pool_type](
                        kernel_size=self.pool_kernel,
                        stride=self.pool_stride,
                        padding=self.pool_padding,
                    )
                else:
                    raise ValueError("'pool_type' must be one of {}".format(list("pooling")))
            elif isinstance(self.pool_type, Callable):
                pool = self.pool_type(
                    kernel_size=self.pool_kernel,
                    stride=self.pool_stride,
                    padding=self.pool_padding,
                )
        else:
            pool = self.pool_type

        # Define the dropout layer
        if self.dropout_rate is not None and self.dropout_rate != 0.0:
            dropout = nn.Dropout(self.dropout_rate)
        else:
            dropout = None
        
        # Define the order of the layers
        self.order = self.order.split("-")
        self.layers = nn.Sequential()
        for layer in self.order:
            if layer == "conv":
                self.layers.add_module("conv", conv)
            elif layer == "norm":
                if norm is not None:
                    self.layers.add_module("norm", norm)
            elif layer == "act":
                if self.activation is not None:
                    self.layers.add_module("act", activation)
            elif layer == "pool":
                if pool is not None:
                    self.layers.add_module("pool", pool)
            elif layer == "dropout":
                if dropout is not None:
                    self.layers.add_module("dropout", dropout)
            else:
                raise ValueError("Invalid layer type: {}".format(layer))

        self.output_size = get_output_size(
            self.layers, (self.input_channels, self.input_len)
        )
        if residual:
            assert (self.output_size[0] == self.input_channels) and (self.output_size[1] == self.input_len), "Residual connection must have same size as input"
            self.layers = layers.Residual(self.layers)

    def forward(self, x):
        return self.layers(x)


class RecurrentBlock(nn.Module):
    """Flexible block for recurrent layers

    A stack of recurrent layers with optional dropout. This block is a wrapper around
    `torch.nn.RNN`, `torch.nn.LSTM`, and `torch.nn.GRU`.

    Parameters
    ----------
    input_dim : int
        The dimension of the input.
    hidden_dim : int
        The dimension of the hidden state.
    num_layers : int
        The number of recurrent layers.
    unit_type : str
        The type of recurrent unit to use. Must be a key in
        `eugene.models.base._layers.RECURRENT_REGISTRY`.
    bidirectional : bool
        Whether or not to use a bidirectional recurrent layer.
    dropout_rates : float
        The dropout rate to use. If `None`, no dropout is used.
    bias : bool
        Whether or not to use a bias term.
    batch_first : bool
        Whether or not the input is batch first.
    """
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        num_layers: int = 1,
        unit_type: str = "lstm",
        bidirectional: bool = False,
        dropout_rates: float = 0.0,
        bias=True,
        batch_first=True,
    ):
        super(RecurrentBlock, self).__init__()

        # Define input parameters
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.unit_type = layers.RECURRENT_REGISTRY[unit_type]
        self.bidirectional = bidirectional
        self.dropout_rates = dropout_rates
        self.bias = bias
        self.batch_first = batch_first

        # Define recurrent layers
        self.layers = self.unit_type(
            input_size=self.input_dim,
            hidden_size=self.hidden_dim,
            num_layers=self.num_layers,
            bias=self.bias,
            batch_first=self.batch_first,
            dropout=self.dropout_rates,
            bidirectional=self.bidirectional,
        )

        # Define output parameters
        self.out_channels = (
            self.hidden_dim * 2 if self.bidirectional else self.hidden_dim
        )

    def forward(self, x):
        return self.layers(x)
    

class DenseBlock(nn.Module):
    """Flexible block for dense layers

    A stack of linear layers with optional activation, batchnorm, and dropout.

    Parameters
    ----------
    input_dim : int
        The dimension of the input.
    output_dim : int
        The dimension of the output.
    bias : bool
        Whether or not to use a bias term.
    activation : str or callable
        The type of activation to use. If a string, must be a key in `sm.list("activation").
        If a callable, must be a subclass of `torch.nn.Module`.
    norm_type : str or callable
        The type of normalization layer to use. If a string, must be a key in
        `sm.list("normalizer")`. If a callable, must be a subclass of `torch.nn.Module`.
    norm_dim : int
        The dimension to normalize over. If `None`, defaults to the number of output
        channels.
    dropout_rate : float
        The dropout rate to use. If `None`, no dropout is used.
    order : str
        The order of the layers in the block. Must be a string of the following
        characters: `linear`, `norm`, `act`, `dropout`. For example, the string
        `linear-norm-act-dropout` would result in a block with a linear layer,
        a normalization layer, an activation layer, and a dropout layer in that order.
        If `None`, defaults to `linear-norm-act-dropout`.
    """
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        bias: bool = True,
        activation: Union[str, Callable, List[Union[str, Callable]]] = "relu",
        norm_type: Union[str, Callable, List[Union[str, Callable]]] = "batchnorm",
        norm_dim: int = None,
        dropout_rate: float = 0.0,
        order: str = "linear-norm-act-dropout",
        residual=False,
    ):
        super(DenseBlock, self).__init__()

        # Define the layers
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.bias = bias
        self.activation = activation
        self.norm_type = norm_type
        self.norm_dim = norm_dim if norm_dim is not None else self.output_dim
        self.dropout_rate = dropout_rate
        self.order = order

        # Define the linear layer
        linear = nn.Linear(self.input_dim, self.output_dim, bias=self.bias)

        # Define the norm layer
        if self.norm_type is not None:
            if isinstance(self.norm_type, str):
                if self.norm_type in layers.NORMALIZER_REGISTRY:
                    norm = layers.NORMALIZER_REGISTRY[self.norm_type](self.norm_dim)
                else:
                    raise ValueError("'norm_type' must be one of {}".format(list("normalizer")))
            elif isinstance(self.norm_type, Callable):
                norm = self.norm_type(self.norm_dim)
            else:
                raise ValueError("'norm_type' must be one of 'str' or 'Callable'")
        else:
            norm = self.norm_type

        # Define the activation
        if self.activation is not None:
            if isinstance(self.activation, str):
                if self.activation in layers.ACTIVATION_REGISTRY:
                    activation = layers.ACTIVATION_REGISTRY[self.activation](inplace=False)
                else:
                    raise ValueError("'activation must' be one of {}".format(list("activation")))
            elif isinstance(self.activation, Callable):
                activation = self.activation
            else:
                raise ValueError("'activation' must be one of 'str' or 'Callable'")
        else:
            activation = self.activation

        # Define the dropout rate
        if self.dropout_rate is not None and self.dropout_rate != 0.0:
            dropout = nn.Dropout(self.dropout_rate)
        else:
            dropout = None

        # Define the order of the layers
        self.order = self.order.split("-")
        self.layers = nn.Sequential()
        for layer in self.order:
            if layer == "linear":
                self.layers.add_module("linear", linear)
            elif layer == "norm":
                if norm is not None:
                    self.layers.add_module("norm", norm)
            elif layer == "act":
                if self.activation is not None:
                    self.layers.add_module("act", activation)
            elif layer == "dropout":
                if dropout is not None:
                    self.layers.add_module("dropout", dropout)
            else:
                raise ValueError("Invalid layer type: {}".format(layer))
        if residual:
            assert (self.input_dim == self.output_dim), "Residual connection must have same size as input"
            self.layers = layers.Residual(self.layers)

    def forward(self, x):
        return self.layers(x)


BLOCK_REGISTRY = {
    "dense": DenseBlock,
    "conv1d": Conv1DBlock,
    "recurrent": RecurrentBlock,
}
