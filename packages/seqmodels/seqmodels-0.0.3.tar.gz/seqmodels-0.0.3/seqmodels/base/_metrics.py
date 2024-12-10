from typing import Callable, Optional, Tuple, Union, Literal, List, Mapping, Any
import torch
import torch.nn as nn
import torchmetrics
import torch.nn.functional as F
import torchmetrics

METRIC_REGISTRY = {
    "r2": torchmetrics.functional.r2_score,
    "pearson": torchmetrics.functional.pearson_corrcoef,
    "spearman": torchmetrics.functional.spearman_corrcoef,
    "mse": torchmetrics.functional.mean_squared_error,
    "mae": torchmetrics.functional.mean_absolute_error,
    "poisson": F.poisson_nll_loss,
    "kl_div": torchmetrics.functional.kl_divergence,
    "accuracy": torchmetrics.functional.accuracy,
    "auroc": torchmetrics.functional.auroc,
    "average_precision": torchmetrics.functional.average_precision,
    "f1": torchmetrics.functional.f1_score,
}


class GeneralMetric(nn.Module):
    def __init__(
        self, 
        output_vars: List[str],
        target_vars: List[str],
        metric_fxn: Union[str, List[str], Callable],
        **kwargs
    ):
        super().__init__()
        self.output_vars = output_vars
        self.target_vars = target_vars
        if not isinstance(metric_fxn, str) and not isinstance(metric_fxn, list):
            self.custom = True
            self.name = "custom"
            self.fxn = metric_fxn
        elif isinstance(metric_fxn, list):
            self.custom = False
            self.name = metric_fxn
            self.fxn = [METRIC_REGISTRY[metric] for metric in metric_fxn]
        else:
            self.custom = False
            self.name = metric_fxn
            self.fxn = METRIC_REGISTRY[metric_fxn]
        self.metric_kwargs = kwargs


    def forward(self, output_dict: Mapping[str, torch.Tensor], target_dict: Mapping[str, torch.Tensor]) -> torch.Tensor:
        """Forward pass of the metric function.

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
        metric: torch.Tensor
            The metric value.
        """
        if self.custom:
            return self.fxn(output_dict, target_dict, **self.metric_kwargs)
        elif isinstance(self.fxn, list):
            output = output_dict[self.output_vars[0]]
            target = target_dict[self.target_vars[0]]
            return {metric: fxn(output, target, **self.metric_kwargs) for metric, fxn in zip(self.name, self.fxn)}
        else:
            output = output_dict[self.output_vars[0]]
            target = target_dict[self.target_vars[0]]
            return {self.name: self.fxn(output, target, **self.metric_kwargs)}
