from typing import List, Dict, Union, Tuple, Optional
from ._layers import MultiHeadAttention
from ._blocks import Conv1DBlock, RecurrentBlock, DenseBlock
from ._towers import Tower

# Helper for going from config to tower, simplifies the config for the user
def build_conv1d_tower(
    input_len: int,
    conv1d_tower_params: Dict[str, Union[List, str]],
):
    # Read in the args
    dynamic_block_args = {}
    static_block_args = {}
    static_block_args["input_len"] = input_len
    dynamic_block_args["input_channels"] = conv1d_tower_params["conv_channels"][:-1]
    dynamic_block_args["output_channels"] = conv1d_tower_params["conv_channels"][1:]
    if "conv_kernels" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["conv_kernels"], list):
            dynamic_block_args["conv_kernel"] = conv1d_tower_params["conv_kernels"]
        else:
            static_block_args["conv_kernel"] = conv1d_tower_params["conv_kernels"]
    if "conv_types" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["conv_types"], list):
            dynamic_block_args["conv_type"] = conv1d_tower_params["conv_types"]
        else:
            static_block_args["conv_type"] = conv1d_tower_params["conv_types"]
    if "conv_strides" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["conv_strides"], list):
            dynamic_block_args["conv_stride"] = conv1d_tower_params["conv_strides"]
        else:
            static_block_args["conv_stride"] = conv1d_tower_params["conv_strides"]
    if "conv_paddings" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["conv_paddings"], list):
            dynamic_block_args["conv_padding"] = conv1d_tower_params["conv_paddings"]
        else:
            static_block_args["conv_padding"] = conv1d_tower_params["conv_paddings"]
    if "conv_dilations" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["conv_dilations"], list):
            dynamic_block_args["conv_dilation"] = conv1d_tower_params["conv_dilations"]
        else:
            static_block_args["conv_dilation"] = conv1d_tower_params["conv_dilations"]
    if "conv_biases" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["conv_biases"], list):
            dynamic_block_args["conv_bias"] = conv1d_tower_params["conv_biases"]
        else:
            static_block_args["conv_bias"] = conv1d_tower_params["conv_biases"]
    if "activations" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["activations"], list):
            dynamic_block_args["activation"] = conv1d_tower_params["activations"]
        else:
            static_block_args["activation"] = conv1d_tower_params["activations"]
    if "pool_types" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["pool_types"], list):
            dynamic_block_args["pool_type"] = conv1d_tower_params["pool_types"]
        else:
            static_block_args["pool_type"] = conv1d_tower_params["pool_types"]
    if "pool_kernels" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["pool_kernels"], list):
            dynamic_block_args["pool_kernel"] = conv1d_tower_params["pool_kernels"]
        else:
            static_block_args["pool_kernel"] = conv1d_tower_params["pool_kernels"]
    if "pool_strides" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["pool_strides"], list):
            dynamic_block_args["pool_stride"] = conv1d_tower_params["pool_strides"]
        else:
            static_block_args["pool_stride"] = conv1d_tower_params["pool_strides"]
    if "pool_paddings" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["pool_paddings"], list):
            dynamic_block_args["pool_padding"] = conv1d_tower_params["pool_paddings"]
        else:
            static_block_args["pool_padding"] = conv1d_tower_params["pool_paddings"]
    if "norm_types" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["norm_types"], list):
            dynamic_block_args["norm_type"] = conv1d_tower_params["norm_types"]
        else:
            static_block_args["norm_type"] = conv1d_tower_params["norm_types"]
    if "norm_dims" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["norm_dims"], list):
            dynamic_block_args["norm_dim"] = conv1d_tower_params["norm_dims"]
        else:
            static_block_args["norm_dim"] = conv1d_tower_params["norm_dims"]
    if "dropout_rates" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["dropout_rates"], list):
            dynamic_block_args["dropout_rate"] = conv1d_tower_params["dropout_rates"]
        else:
            static_block_args["dropout_rate"] = conv1d_tower_params["dropout_rates"]
    if "residuals" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["residuals"], list):
            dynamic_block_args["residual"] = conv1d_tower_params["residuals"]
        else:
            static_block_args["residual"] = conv1d_tower_params["residuals"]
    if "orders" in conv1d_tower_params:
        if isinstance(conv1d_tower_params["orders"], list):
            dynamic_block_args["order"] = conv1d_tower_params["orders"]
        else:
            static_block_args["order"] = conv1d_tower_params["orders"]

    # Contruct the tower
    conv1d_tower = Tower(
        input_size=(conv1d_tower_params["conv_channels"][0], input_len),
        block=Conv1DBlock,
        repeats=len(conv1d_tower_params["conv_channels"])-1,
        static_block_args=static_block_args,
        dynamic_block_args=dynamic_block_args,
    )
    return conv1d_tower


# Probably don't need, as args are straightforward
def build_recurrent_block(
    input_dim: int,
    recurrent_block_params: Dict[str, Union[List, str]],
):
    args = {}
    args["input_dim"] = input_dim
    if "hidden_dim" in recurrent_block_params:
        args["hidden_dim"] = recurrent_block_params["hidden_dim"]
    if "num_layers" in recurrent_block_params:
        args["num_layers"] = recurrent_block_params["num_layers"]
    if "unit_type" in recurrent_block_params:
        args["unit_type"] = recurrent_block_params["unit_type"]
    if "bidirectional" in recurrent_block_params:
        args["bidirectional"] = recurrent_block_params["bidirectional"]
    if "dropout_rates" in recurrent_block_params:
        args["dropout_rates"] = recurrent_block_params["dropout_rates"]
    if "bias" in recurrent_block_params:
        args["bias"] = recurrent_block_params["bias"]
    if "batch_first" in recurrent_block_params:
        args["batch_first"] = recurrent_block_params["batch_first"]
    recurrent_block = RecurrentBlock(**args)
    return recurrent_block


# Probably don't need, as args are straightforward
def build_mha_layer(
    input_dim: int,
    mha_layer_params: Dict[str, Union[List, str]],
):
    args = {}
    args["input_dim"] = input_dim
    if "head_dim" in mha_layer_params:
        args["head_dim"] = mha_layer_params["head_dim"]
    if "num_heads" in mha_layer_params:
        args["num_heads"] = mha_layer_params["num_heads"]
    if "dropout_rate" in mha_layer_params:
        args["dropout_rate"] = mha_layer_params["dropout_rate"]

    # Construct the block
    mha_layer = MultiHeadAttention(**args)

    return mha_layer


# Helper for going from config to tower, simplifies the config for the user
def build_dense_tower(
    input_size: int,
    output_dim: int,
    dense_tower_params: Dict[str, Union[List, str]],
):
    # Read in the args
    dynamic_block_args = {}
    static_block_args = {}
    dynamic_block_args["input_dim"] = [input_size] + dense_tower_params["hidden_dims"] if dense_tower_params["hidden_dims"] else [input_size]
    dynamic_block_args["output_dim"] = dense_tower_params["hidden_dims"] + [output_dim]
    if "biases" in dense_tower_params:
        if isinstance(dense_tower_params["biases"], list):
            dynamic_block_args["bias"] = dense_tower_params["biases"]
        else:
            static_block_args["bias"] = dense_tower_params["biases"]
    if "activations" in dense_tower_params:
        if isinstance(dense_tower_params["activations"], list):
            dynamic_block_args["activation"] = dense_tower_params["activations"]
        else:
            static_block_args["activation"] = dense_tower_params["activations"]
    if "dropout_rates" in dense_tower_params:
        if isinstance(dense_tower_params["dropout_rates"], list):
            dynamic_block_args["dropout_rate"] = dense_tower_params["dropout_rates"]
        else:
            static_block_args["dropout_rate"] = dense_tower_params["dropout_rates"]
    if "norm_types" in dense_tower_params:
        if isinstance(dense_tower_params["norm_types"], list):
            dynamic_block_args["norm_type"] = dense_tower_params["norm_types"]
        else:
            static_block_args["norm_type"] = dense_tower_params["norm_types"]
    if "norm_dims" in dense_tower_params:
        if isinstance(dense_tower_params["norm_dims"], list):
            dynamic_block_args["norm_dim"] = dense_tower_params["norm_dims"]
        else:
            static_block_args["norm_dim"] = dense_tower_params["norm_dims"]
    if "orders" in dense_tower_params:
        if isinstance(dense_tower_params["orders"], list):
            dynamic_block_args["order"] = dense_tower_params["orders"]
        else:
            static_block_args["order"] = dense_tower_params["orders"]
    
    # Contruct the tower
    dense_tower = Tower(
        input_size=input_size,
        block=DenseBlock,
        repeats=len(dense_tower_params["hidden_dims"])+1,
        static_block_args=static_block_args,
        dynamic_block_args=dynamic_block_args,
    )
    return dense_tower
