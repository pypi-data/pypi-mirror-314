from typing import Literal, Union, Optional, Tuple, List
import numpy as np
from funcnodes import Shelf, NodeDecorator
from enum import Enum
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.losses import Loss
from tensorflow.keras.metrics import Metric
from tensorflow.keras.callbacks import Callback, History


@NodeDecorator(
    node_id="tensorflow.keras.training.compile ",
    name="compile ",
    outputs=[
        {"name": "compiled_model"},
    ],
)
# @controlled_wrapper(compile , wrapper_attribute="__fnwrapped__")
def _compile(
    model: Model,
    optimizer: Optimizer,
    loss: Loss,
    metrics: Union[Metric, List[Metric], dict],
    loss_weights: Optional[Union[list, dict]] = None,
    weighted_metrics: Optional[list] = None,
    run_eagerly: bool = False,
    steps_per_execution: int = 1,
    jit_compile: Union[bool, Literal["auto"]] = "auto",
    auto_scale_loss: bool = True,
) -> Model:
    if isinstance(metrics, Metric):
        metrics = [metrics]
    model.compile(
        optimizer=optimizer,
        loss=loss,
        loss_weights=loss_weights,
        metrics=metrics,
        weighted_metrics=weighted_metrics,
        run_eagerly=run_eagerly,
        steps_per_execution=steps_per_execution,
        jit_compile=jit_compile,
        auto_scale_loss=auto_scale_loss,
    )
    return model


class Verbose(Enum):
    auto = "auto"
    zero = 0
    one = 1
    two = 2

    @classmethod
    def default(cls):
        return cls.auto.value


@NodeDecorator(
    node_id="tensorflow.keras.training.fit ",
    name="fit ",
    outputs=[
        {"name": "fitted_model"},
        {"name": "history"},
        {"name": "metrics_dictionary"},
    ],
)
def _fit(
    model: Model,
    x: Union[list, np.ndarray, dict],
    y: Optional[Union[list, np.ndarray, dict]] = None,
    batch_size: Optional[int] = None,
    epochs: int = 1,
    verbose: Verbose = Verbose.default(),
    callbacks: Optional[Union[Callback, List[Callback]]] = None,
    validation_split: float = 0.0,
    x_val: Optional[Union[list, np.ndarray, dict]] = None,
    y_val: Optional[Union[list, np.ndarray, dict]] = None,
    shuffle: bool = True,
    class_weight: Optional[dict] = None,
    sample_weight: Optional[np.ndarray] = None,
    initial_epoch: int = 0,
    steps_per_epoch: Optional[int] = None,
    validation_steps: Optional[int] = None,
    validation_batch_size: Optional[int] = None,
    validation_freq: int = 1,
) -> Tuple[Model, History, dict]:
    if isinstance(callbacks, Callback):
        callbacks = [callbacks]
    if x_val is not None and y_val is not None:
        validation_data: Tuple = [x_val, y_val]
    else:
        validation_data = None

    if not 0 <= validation_split < 1:
        raise ValueError("validation_split must be between 0 and 1")

    out = model.fit(
        x=x,
        y=y,
        batch_size=batch_size,
        epochs=epochs,
        verbose=verbose,
        callbacks=callbacks,
        validation_split=validation_split,
        validation_data=validation_data,
        shuffle=shuffle,
        class_weight=class_weight,
        sample_weight=sample_weight,
        initial_epoch=initial_epoch,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        validation_batch_size=validation_batch_size,
        validation_freq=validation_freq,
    )

    return model, out, out.history


@NodeDecorator(
    node_id="tensorflow.keras.training.evaluate ",
    name="evaluate ",
)
def _evaluate(
    model: Model,
    x: Union[list, np.ndarray, dict],
    y: Optional[Union[list, np.ndarray, dict]] = None,
    batch_size: Optional[int] = None,
    verbose: Verbose = Verbose.default(),
    sample_weight: Optional[np.ndarray] = None,
    steps: Optional[int] = None,
    callbacks: Optional[List[Callback]] = None,
) -> dict:
    return model.evaluate(
        x=x,
        y=y,
        batch_size=batch_size,
        verbose=verbose,
        sample_weight=sample_weight,
        steps=steps,
        callbacks=callbacks,
        return_dict=True,
    )


@NodeDecorator(
    node_id="tensorflow.keras.training.predict ",
    name="predict ",
)
def _predict(
    model: Model,
    x: Union[np.ndarray, List[np.ndarray]],
    batch_size: Optional[int] = None,
    verbose: Verbose = Verbose.default(),
    steps: Optional[int] = None,
    callbacks: Optional[List[Callback]] = None,
) -> np.ndarray:
    return model.predict(
        x=x,
        batch_size=batch_size,
        verbose=verbose,
        steps=steps,
        callbacks=callbacks,
    )


@NodeDecorator(
    node_id="tensorflow.keras.training.train_on_batch ",
    name="train_on_batch ",
)
def _train_on_batch(
    model: Model,
    x: np.ndarray,
    y: np.ndarray,
    sample_weight: Optional[np.ndarray] = None,
    class_weight: Optional[dict] = None,
) -> dict:
    return model.train_on_batch(
        x=x,
        y=y,
        sample_weight=sample_weight,
        class_weight=class_weight,
        return_dict=True,
    )


@NodeDecorator(
    node_id="tensorflow.keras.training.test_on_batch ",
    name="test_on_batch ",
)
def _test_on_batch(
    model: Model,
    x: np.ndarray,
    y: np.ndarray,
    sample_weight: Optional[np.ndarray] = None,
) -> dict:
    return model.test_on_batch(
        x=x,
        y=y,
        sample_weight=sample_weight,
        return_dict=True,
    )


@NodeDecorator(
    node_id="tensorflow.keras.training.predict_on_batch ",
    name="predict_on_batch ",
)
def _predict_on_batch(
    model: Model,
    x: np.ndarray,
) -> dict:
    return model.predict_on_batch(
        x=x,
    )


FIT_NODE_SHELFE = Shelf(
    nodes=[
        _fit,
        _compile,
        _evaluate,
        _predict,
        _train_on_batch,
        _test_on_batch,
        _predict_on_batch,
    ],
    subshelves=[],
    name="Fit",
    description="Methods for compiling, fitting, and more.",
)
