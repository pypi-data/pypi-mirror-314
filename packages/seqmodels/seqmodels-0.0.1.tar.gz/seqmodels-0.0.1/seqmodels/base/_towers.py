import torch
from torch import nn
from inspect import signature
from typing import Type, Dict, Union, Callable, List, Any
from .._utils import get_output_size


class Tower(nn.Module):
    """A tower of blocks.

    This is modeled after David Kelley's Basenji repo for conv towers
    but is generalized to any block type.

    Parameters
    ----------
    block : Type[nn.Module]
        The type of block to repeat.
    repeats : int
        The number of times to repeat the block.
    input_size : tuple
        The input size to the first block.
    static_block_args : Dict[str, Any]
        Arguments to initialize blocks that are static across repeats.
    dynamic_block_args : Dict[str, Any]
        Arguments to initialize blocks that change across repeats.
    mults : Dict[str, float]
        Multipliers for dynamic block arguments.
    name : str
        Name of the tower. Useful for pulling out specific towers
        in a complex model.
    """
    def __init__(
        self,
        block: Type[nn.Module],
        repeats: int,
        input_size: tuple,
        static_block_args: Dict[str, Any] = None,
        dynamic_block_args: Dict[str, Any] = None,
        mults: Dict[str, float] = None,
        name: str = "tower",
    ):
        super().__init__()
        self.input_size = input_size
        self.repeats = repeats
        self.block_name = block.__name__.lower()
        self.name = name

        blocks = nn.ModuleList()
        if static_block_args is None:
            static_block_args = {}
        if dynamic_block_args is None:
            dynamic_block_args = {}
        if mults is None:
            mults = {}

        for arg, mult in mults.items():
            # replace initial value with geometric progression
            init_val = dynamic_block_args.get(
                arg, signature(block).parameters[arg].default
            )
            dynamic_block_args[arg] = (
                (
                    init_val
                    * torch.logspace(start=0, end=repeats - 1, steps=repeats, base=mult)
                )
                .to(dtype=signature(block).parameters[arg].annotation)
                .tolist()
            )

        self.blocks = nn.Sequential()
        for i in range(repeats):
            args = {arg: vals[i] for arg, vals in dynamic_block_args.items()}
            args.update(static_block_args)
            self.blocks.add_module(f"{self.block_name}_{i}", block(**args))

        self.output_size = get_output_size(self.blocks, self.input_size)

    def forward(self, x):
        return self.blocks(x)
