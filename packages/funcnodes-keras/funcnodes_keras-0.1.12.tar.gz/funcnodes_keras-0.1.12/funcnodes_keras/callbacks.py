from typing import Optional, Union
from enum import Enum
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
import os
from tensorflow.keras.callbacks import Callback, ModelCheckpoint


class Monitor(Enum):
    accuracy = "accuracy"
    loss = "loss"
    val_loss = "val_loss"
    val_accuracy = "val_accuracy"

    @classmethod
    def default(cls):
        return cls.val_loss.value


class Verbose(Enum):
    zero = 0
    one = 1

    @classmethod
    def default(cls):
        return cls.zero.value


class Mode(Enum):
    min = "min"
    max = "max"
    auto = "auto"

    @classmethod
    def default(cls):
        return cls.auto.value


@NodeDecorator(
    node_id="tensorflow.keras.callbacks.ModelCheckpoint",
    name="ModelCheckpoint",
)
@controlled_wrapper(ModelCheckpoint, wrapper_attribute="__fnwrapped__")
def _ModelCheckpoint(
    monitor: Monitor = Monitor.default(),
    verbose: Verbose = Verbose.default(),
    save_best_only: bool = False,
    mode: Mode = Mode.default(),
    save_weights_only: bool = False,
    save_freq: Optional[int] = None,
    initial_value_threshold: Optional[float] = None,
) -> Callback:
    if isinstance(monitor, Monitor):
        monitor = monitor.value
    if isinstance(verbose, Verbose):
        verbose = verbose.value
    if isinstance(mode, Mode):
        mode = mode.value

    if save_freq is None:
        save_freq = "epoch"

    filepath: Union[str, os.PathLike] = "model.{epoch:02d}-{monitor:.2f}.h5"

    return ModelCheckpoint(
        filepath=filepath,
        monitor=monitor,
        verbose=verbose,
        save_best_only=save_best_only,
        mode=mode,
        save_weights_only=save_weights_only,
        save_freq=save_freq,
        initial_value_threshold=initial_value_threshold,
    )


