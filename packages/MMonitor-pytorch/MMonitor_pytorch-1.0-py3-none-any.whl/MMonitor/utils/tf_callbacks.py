import os

from transformers.integrations.integration_utils import *

from ..visualize import Visualization
from ..mmonitor.monitor import Monitor
from .loader import load_monitor_config


class MonitorWandbCallback(WandbCallback):
    def __init__(self, monitor_config=None):
        self.monitor_config = load_monitor_config(monitor_config)
        
        super().__init__()

    def setup(self, args, state, model, **kwargs):
        if self._wandb is None or self.monitor_config is None:
            return
        self._initialized = True
        if state.is_world_process_zero:
            logger.info(
                'Automatic Weights & Biases logging enabled, to disable set os.environ["WANDB_DISABLED"] = "true"'
            )
            combined_dict = {**args.to_dict()}

            if hasattr(model, "config") and model.config is not None:
                model_config = model.config.to_dict()
                combined_dict = {**model_config, **combined_dict}
            trial_name = state.trial_name
            init_args = {}
            if trial_name is not None:
                init_args["name"] = trial_name
                init_args["group"] = args.run_name
            else:
                if not (args.run_name is None or args.run_name == args.output_dir):
                    init_args["name"] = args.run_name

            if self._wandb.run is None:
                self._wandb.init(
                    project=os.getenv("WANDB_PROJECT", "huggingface"),
                    **init_args,
                )
            # add config parameters (run may have been created manually)
            self._wandb.config.update(combined_dict, allow_val_change=True)

            # define default x-axis (for latest wandb versions)
            if getattr(self._wandb, "define_metric", None):
                self._wandb.define_metric("train/global_step")
                self._wandb.define_metric("*", step_metric="train/global_step", step_sync=True)

            # keep track of model topology and gradients, unsupported on TPU
            _watch_model = os.getenv("WANDB_WATCH", "false")
            if not is_torch_tpu_available() and _watch_model in ("all", "parameters", "gradients"):
                self._wandb.watch(model, log=_watch_model, log_freq=max(100, state.logging_steps))
            self._wandb.run._label(code="transformers_trainer")
            self.monitor = Monitor(model, self.monitor_config)
            self.vis = Visualization(self.monitor, self._wandb, project=os.getenv("WANDB_PROJECT", "huggingface"), name=init_args['name'])

    def on_train_begin(self, args, state, control, model=None, **kwargs):
        if self._wandb is None or self.monitor_config is None:
            return
        if not self._initialized:
            self.setup(args, state, model, **kwargs)

    def on_train_end(self, args, state, control, model=None, tokenizer=None, **kwargs):
        if self._wandb is None or self.monitor_config is None:
            return
        

    def on_log(self, args, state, control, model=None, logs=None, **kwargs):
        return
            
    def on_step_end(self, args, state, control, model=None, logs=None, **kwargs):
        if self._wandb is None:
            return
        if not self._initialized:
            self.setup(args, state, model)
        if state.is_world_process_zero:
            if self.monitor is not None:
                self.monitor.track(state.global_step)
            if self.vis is not None:
                self.vis.show(state.global_step)

    def on_save(self, args, state, control, **kwargs):
        return