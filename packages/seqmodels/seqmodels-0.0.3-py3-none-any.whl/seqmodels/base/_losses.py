from typing import Callable, Optional, Tuple, Union, Literal, List, Mapping, Any
import torch
import torch.nn as nn
import torch.nn.functional as F
from bpnetlite.losses import MNLLLoss, log1pMSELoss


LOSS_REGISTRY = {
    "mse": F.mse_loss,
    "mae": F.l1_loss,
    "poisson": F.poisson_nll_loss,
    "bce": F.binary_cross_entropy_with_logits,
    "cross_entropy": F.cross_entropy,
    "log1pmse": log1pMSELoss,
    "mnll": MNLLLoss,
}


class GeneralLoss(nn.Module):
    def __init__(
        self, 
        output_vars: List[str],
        target_vars: List[str],
        loss_fxn: Union[str, Callable],
        **kwargs
    ):
        super().__init__()
        self.output_vars = output_vars
        self.target_vars = target_vars
        if not isinstance(loss_fxn, str):
            self.custom = True
            self.name = "custom"
            self.fxn = loss_fxn
        else:
            self.custom = False
            self.name = loss_fxn
            self.fxn = LOSS_REGISTRY[loss_fxn]
        self.loss_kwargs = kwargs


    def forward(self, output_dict: Mapping[str, torch.Tensor], target_dict: Mapping[str, torch.Tensor]) -> torch.Tensor:
        """Forward pass of the loss function.

        Parameters
        ----------
        output_dict: Mapping[str, torch.Tensor]
            A dictionary of tensors containing the model outputs. The keys
            should match the `output_vars` provided to the constructor.
        target_dict: Mapping[str, torch.Tensor]
            A dictionary of tensors containing the targets. The keys
            should match the `target_vars` provided to the constructor.

        Returns
        -------
        loss: torch.Tensor
            The loss value.
        """
        if self.custom:
            return self.fxn(output_dict, target_dict, **self.loss_kwargs)
        else:
            output = output_dict[self.output_vars[0]]
            target = target_dict[self.target_vars[0]].float()
            return {"loss": self.fxn(output, target, **self.loss_kwargs)}
        
            