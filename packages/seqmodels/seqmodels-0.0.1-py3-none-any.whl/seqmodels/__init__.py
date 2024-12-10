"""Sequence-to-function models for genomics."""
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

package_name = "seqmodels"
__version__ = importlib_metadata.version(package_name)

# Model instantiations
from .base import _layers as layers
from .base._blocks import DenseBlock, Conv1DBlock, RecurrentBlock
from .base._towers import Tower

# Basic models
from .base._architectures import CNN, Hybrid, Transformer

# Zoo
from .zoo._load import DeepSTARR, DeepSEA

# Model initializers
from .base._initializers import init_motif_weights, init_weights
from .zoo._config import load_config

# Modules
from .base._modules import Module

# Helpers
from ._utils import get_output_size, list_available_layers, get_layer, list
