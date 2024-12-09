import os
import mindspore.nn as nn
import mindspore.dataset as Dataset
import wandb

from ..visualize import Visualization
from MMonitor.mmonitor.monitor import Monitor
from .loader import load_monitor_config


class MonitorWandbCallback:
    def __init__(self, monitor_config=None):
        self.monitor_config = load_monitor_config(monitor_config)
        self._initialized = False
        self._wandb = wandb

    def setup(self, args, model):
        if self._wandb is None or self.monitor_config is None:
            return
        self._initialized = True
        if wandb.run is None:
            wandb.init(project=os.getenv("WANDB_PROJECT", "jittor"), config=args)

        # Log model config
        if hasattr(model, "config") and model.config is not None:
            model_config = model.config.to_dict()
            wandb.config.update(model_config)

        # Track model parameters
        _watch_model = os.getenv("WANDB_WATCH", "false")
        if _watch_model in ("all", "parameters", "gradients"):
            wandb.watch(model, log=_watch_model)

        self.monitor = Monitor(model, self.monitor_config)
        self.vis = Visualization(self.monitor, self._wandb, project=os.getenv("WANDB_PROJECT", "jittor"))

    def on_train_begin(self, args, model):
        if self._wandb is None or self.monitor_config is None:
            return
        if not self._initialized:
            self.setup(args, model)

    def on_train_end(self):
        if self._wandb is None or self.monitor_config is None:
            return
        # Optionally, handle end of training

    def on_log(self, logs=None):
        # Optionally log custom metrics
        pass

    def on_step_end(self, global_step):
        if self._wandb is None:
            return
        if not self._initialized:
            self.setup(args, model)
        if self.monitor is not None:
            self.monitor.track(global_step)
        if self.vis is not None:
            self.vis.show(global_step)

    def on_save(self):
        # Optionally handle saving the model
        pass
