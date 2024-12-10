from typing import Callable, Optional, Tuple, Union, Literal, List, Mapping, Any

import numpy as np
import torch
import torch.nn as nn
from pytorch_lightning import seed_everything
from pytorch_lightning.core import LightningModule
from pytorch_lightning.utilities.model_summary import ModelSummary
from tqdm.auto import tqdm

from ._losses import GeneralLoss
from ._metrics import GeneralMetric
from ._optimizers import OPTIMIZER_REGISTRY
from ._schedulers import SCHEDULER_REGISTRY


class Module(LightningModule):
    """Base module for all seqmodels modules.

    Parameters
    ----------
    arch : torch.nn.Module
        The torch.nn.Module that will compute the forward pass of the model on the input_vars. The input_vars should be
        in the same order as the inputs to the forward pass of the arch.
    input_vars : List[str]
        The names of the input variables to the model. These should be in the same order as the inputs to the forward
        pass of the arch.
    output_vars : List[str]
        The names of the output variables of the model. These should be in the same order as the outputs of the forward
        pass of the arch.
    target_vars : List[str]
        The names of the target variables of the model. The ordering of these variables does not matter.
    squeeze_output : bool
        Some combinations of models and loss/metric functions require the output to be squeezed. If this is the case, set this
        to True.
    loss_fxn : Union[str, Callable]
        The loss function to use. This can either be a string corresponding to a loss function in LOSS_REGISTRY or a
        custom loss function. The availble losses can be retrieved using seqmodels.list("loss"). If a custom loss is
        provided, it should take in two dictionaries of tensors, output_dict and target_dict, and return a dictionary
        that at the very least contains a key "loss" with a single loss value. The keys of output_dict and target_dict
        should match the output_vars and target_vars, respectively.
    loss_kwargs : Mapping[str, Any]
        Keyword arguments to pass to the loss function. This is often something like alpha=0.5 for a weighted loss.
    train_metrics_fxn : Optional[Union[str, List[str], Callable]]
        The metrics function(s) to use. This can either be a string (or list of strings) corresponding to metrics in METRIC_REGISTRY
        or a custom metric function. The availble metrics can be retrieved using seqmodels.list("metric"). If a custom
        metric is provided, it should take in two dictionaries of tensors, output_dict and target_dict, and return a
        dictionary of metrics. The keys of output_dict and target_dict should match the output_vars and target_vars,
        respectively.
    metrics_kwargs : Mapping[str, Any]
    """

    def __init__(
        self,
        arch: torch.nn.Module,
        input_vars: List[str] = ["seq"],
        output_vars: List[str] = ["output"],
        target_vars: List[str] = ["target"],
        squeeze_output: bool = False,
        loss_fxn: Union[str, Callable] = "mse",
        loss_kwargs: Mapping[str, Any] = {},
        train_metrics_fxn: Optional[Union[str, List[str], Callable]] = None,
        train_metrics_kwargs: Mapping[str, Any] = {},
        val_metrics_fxn: Optional[Union[str, List[str], Callable]] = None,
        val_metrics_kwargs: Mapping[str, Any] = {},
        optimizer: Literal["adam", "sgd"] = "adam",
        optimizer_lr: Optional[float] = 1e-3,
        optimizer_kwargs: Optional[dict] = {},
        scheduler: Optional[str] = None,
        scheduler_monitor: str = "val_loss_epoch",
        scheduler_kwargs: dict = {},
    ):
        super().__init__()
        
        # Set the base architecture 
        self.arch = arch
        
        # Set variables
        self.input_vars = input_vars
        self.output_vars = output_vars
        self.target_vars = target_vars
        self.squeeze_output = squeeze_output

        # Loss function
        self.loss_fxn = GeneralLoss(output_vars=output_vars, target_vars=target_vars, loss_fxn=loss_fxn, **loss_kwargs)
        self.loss_kwargs = loss_kwargs
        
        # Train metrics
        if train_metrics_fxn is not None:
            self.train_metrics_fxn = GeneralMetric(output_vars=output_vars, target_vars=target_vars, metric_fxn=train_metrics_fxn, **train_metrics_kwargs)
            self.train_metrics_kwargs = train_metrics_kwargs
        else:
            self.train_metrics_fxn = None
            self.train_metrics_kwargs = {}

        # Validation metrics
        if val_metrics_fxn is not None:
            self.val_metrics_fxn = GeneralMetric(output_vars=output_vars, target_vars=target_vars, metric_fxn=val_metrics_fxn, **val_metrics_kwargs)
            self.val_metrics_kwargs = val_metrics_kwargs
        else:
            self.val_metrics_fxn = None
            self.val_metrics_kwargs = {}
        
        # Optimizer
        self.optimizer = OPTIMIZER_REGISTRY[optimizer] if isinstance(optimizer, str) else optimizer
        self.optimizer_lr = optimizer_lr if optimizer_lr is not None else 1e-3
        self.optimizer_kwargs = optimizer_kwargs
        
        # Scheduler
        self.scheduler = SCHEDULER_REGISTRY[scheduler] if isinstance(scheduler, str) else scheduler
        self.scheduler_monitor = scheduler_monitor
        self.scheduler_kwargs = scheduler_kwargs

        # Needed for PyTorch Lightning
        self.validation_step_outputs = []

        
    def forward(self, inputs_dict: Mapping[str, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass of the arch.

        Parameters
        ----------
        x : torch.Tensor
            inputs
        """
        return self.arch(*inputs_dict.values())
    

    def predict(
        self, 
        inputs_dict: Mapping[str, torch.Tensor],
        batch_size: int = 32,
        verbose: bool = True,
    ) -> torch.Tensor:
        """Predict the output of the architecture in batches

        Parameters:
        ----------
        x : np.ndarray or torch.Tensor
            input sequence, can be a numpy array or a torch tensor
        batch_size : int
            batch size
        verbose : bool
            whether to show a progress bar
        """
        with torch.no_grad():
            device = self.device
            self.eval()
            if isinstance(inputs_dict[self.input_vars[0]], np.ndarray):
                inputs_dict = {k: torch.from_numpy(v) for k, v in inputs_dict.items()}
            outputs_dict = {}
            for _, i in tqdm(
                enumerate(range(0, len(inputs_dict[self.input_vars[0]]), batch_size)),
                desc="Predicting on batches",
                total=len(inputs_dict[self.input_vars[0]]) // batch_size,
                disable=not verbose,
            ):
                batch = {k: v[i : i + batch_size].to(device) for k, v in inputs_dict.items()}
                out = self(batch)
                if len(self.output_vars) == 1:
                    out_dict = {self.output_vars[0]: out}
                else:
                    out_dict = {var: out[ind] for ind, var in enumerate(self.output_vars)}
                for k, v in out_dict.items():
                    if k not in outputs_dict:
                        outputs_dict[k] = []
                    outputs_dict[k].append(v)
            for k, v in outputs_dict.items():
                outputs_dict[k] = torch.cat(v, dim=0)
            return outputs_dict
        

    def _common_step(self, batch, batch_idx, stage: str):
        # Initialize dictionaries for inputs, outputs, and targets
        inputs_dict = {var: batch[var] for var in self.input_vars}
        targets_dict = {var: batch[var] for var in self.target_vars}
        
        # Forward pass through the model
        outputs = self(inputs_dict)
        if len(self.output_vars) == 1:
            outputs_dict = {self.output_vars[0]: outputs}
        else:
            outputs_dict = {var: outputs[ind] for ind, var in enumerate(self.output_vars)}
        if self.squeeze_output:
            outputs_dict = {k: v.squeeze() for k, v in outputs_dict.items()}
            
        # Calculate losses using the modules loss_fxn
        losses_dict = self.loss_fxn(outputs_dict, targets_dict)

        # Calculate metrics using the modules metrics_fxn
        if self.train_metrics_fxn is not None and stage == "train":
            metrics_dict = self.train_metrics_fxn(outputs_dict, targets_dict)
            step_dict = {**losses_dict, **metrics_dict}
        elif self.val_metrics_fxn is not None and stage == "val":
            metrics_dict = self.val_metrics_fxn(outputs_dict, targets_dict)
            step_dict = {**losses_dict, **metrics_dict}
        else:
            step_dict = losses_dict

        return step_dict
    
    
    def training_step(self, batch, batch_idx):
        """Training step"""
        step_dict = self._common_step(batch, batch_idx, "train")

        # Log loss on step
        self.log(
            "train_loss", 
            step_dict["loss"].mean(), 
            on_step=True, 
            on_epoch=False, 
            prog_bar=True,
        )
        
        # Log everything else on epoch
        self.log_dict(
            {f"train_{k}_epoch": v.mean() for k, v in step_dict.items()}, 
            on_step=False, 
            prog_bar=True,
            on_epoch=True,
        )
        return step_dict["loss"].mean()
    

    def validation_step(self, batch, batch_idx):
        """Validation step"""
        step_dict = self._common_step(batch, batch_idx, "val")

        # Log validation loss and metrics
        self.log_dict(
            {f"val_{k}_epoch": v.mean() for k, v in step_dict.items()}, 
            on_step=False, 
            on_epoch=True,
            prog_bar=True,
        )


    def configure_optimizers(self):
        """Configure optimizers

        Returns:
        ----------
        torch.optim.Optimizer:
            optimizer
        torch.optim.lr_scheduler._LRScheduler:
            learning rate scheduler
        """
        optimizer = self.optimizer(
            self.parameters(), lr=self.optimizer_lr, **self.optimizer_kwargs
        )
        if self.scheduler is None:
            return optimizer
        else:
            scheduler = self.scheduler(optimizer, **self.scheduler_kwargs)
            return {
                "optimizer": optimizer,
                "lr_scheduler": scheduler,
                "monitor": self.scheduler_monitor,
            }
        