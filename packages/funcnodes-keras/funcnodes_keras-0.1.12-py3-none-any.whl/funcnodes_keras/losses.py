from typing import Union, Optional, List
import numpy as np
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from enum import Enum
from tensorflow.keras.losses import (
    Loss,
    BinaryCrossentropy,
    BinaryFocalCrossentropy,
    CategoricalCrossentropy,
    CategoricalFocalCrossentropy,
    SparseCategoricalCrossentropy,
    Poisson,
    KLDivergence,
    CTC,
    MeanSquaredError,
    MeanAbsoluteError,
    MeanAbsolutePercentageError,
    MeanSquaredLogarithmicError,
    CosineSimilarity,
    Huber,
    LogCosh,
    Hinge,
    SquaredHinge,
    CategoricalHinge,
)


class Reduction(Enum):
    sum = "sum"
    sum_over_batch_size = "sum_over_batch_size"
    NONE = None

    @classmethod
    def default(cls):
        return cls.sum_over_batch_size.value


@NodeDecorator(
    node_id="tensorflow.keras.losses.BinaryCrossentropy",
    name="BinaryCrossentropy",
)
@controlled_wrapper(BinaryCrossentropy, wrapper_attribute="__fnwrapped__")
def _BinaryCrossentropy(
    from_logits: bool = True,
    label_smoothing: float = 0.0,
    axis: int = -1,
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return BinaryCrossentropy(
        from_logits=from_logits,
        label_smoothing=label_smoothing,
        axis=axis,
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.BinaryFocalCrossentropy",
    name="BinaryFocalCrossentropy",
)
@controlled_wrapper(BinaryFocalCrossentropy, wrapper_attribute="__fnwrapped__")
def _BinaryFocalCrossentropy(
    apply_class_balancing: bool = False,
    alpha: float = 0.25,
    gamma: float = 2.0,
    from_logits: bool = True,
    label_smoothing: float = 0.0,
    axis: int = -1,
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return BinaryFocalCrossentropy(
        apply_class_balancing=apply_class_balancing,
        alpha=alpha,
        gamma=gamma,
        from_logits=from_logits,
        label_smoothing=label_smoothing,
        axis=axis,
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.CategoricalCrossentropy",
    name="CategoricalCrossentropy",
)
@controlled_wrapper(CategoricalCrossentropy, wrapper_attribute="__fnwrapped__")
def _CategoricalCrossentropy(
    from_logits: bool = True,
    label_smoothing: float = 0.0,
    axis: int = -1,
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return CategoricalCrossentropy(
        from_logits=from_logits,
        label_smoothing=label_smoothing,
        axis=axis,
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.CategoricalFocalCrossentropy",
    name="CategoricalFocalCrossentropy",
)
@controlled_wrapper(CategoricalFocalCrossentropy, wrapper_attribute="__fnwrapped__")
def _CategoricalFocalCrossentropy(
    alpha: float = 0.25,
    gamma: float = 2.0,
    from_logits: bool = True,
    label_smoothing: float = 0.0,
    axis: int = -1,
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return CategoricalFocalCrossentropy(
        alpha=alpha,
        gamma=gamma,
        from_logits=from_logits,
        label_smoothing=label_smoothing,
        axis=axis,
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.SparseCategoricalCrossentropy",
    name="SparseCategoricalCrossentropy",
)
@controlled_wrapper(SparseCategoricalCrossentropy, wrapper_attribute="__fnwrapped__")
def _SparseCategoricalCrossentropy(
    from_logits: bool = True,
    ignore_class: Optional[int] = None,
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return SparseCategoricalCrossentropy(
        from_logits=from_logits,
        ignore_class=ignore_class,
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.Poisson",
    name="Poisson",
)
@controlled_wrapper(Poisson, wrapper_attribute="__fnwrapped__")
def _Poisson(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return Poisson(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.KLDivergence",
    name="KLDivergence",
)
@controlled_wrapper(KLDivergence, wrapper_attribute="__fnwrapped__")
def _KLDivergence(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return KLDivergence(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.CTC",
    name="CTC",
)
@controlled_wrapper(CTC, wrapper_attribute="__fnwrapped__")
def _CTC(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return CTC(
        reduction=reduction,
    )


PROBABILISTIC_NODE_SHELFE = Shelf(
    nodes=[
        _BinaryCrossentropy,
        _BinaryFocalCrossentropy,
        _CategoricalCrossentropy,
        _CategoricalFocalCrossentropy,
        _SparseCategoricalCrossentropy,
        _Poisson,
        _KLDivergence,
        _CTC,
    ],
    subshelves=[],
    name="Probabilistic ",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.losses.MeanSquaredError",
    name="MeanSquaredError",
)
@controlled_wrapper(MeanSquaredError, wrapper_attribute="__fnwrapped__")
def _MeanSquaredError(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return MeanSquaredError(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.MeanAbsoluteError",
    name="MeanAbsoluteError",
)
@controlled_wrapper(MeanAbsoluteError, wrapper_attribute="__fnwrapped__")
def _MeanAbsoluteError(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return MeanAbsoluteError(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.MeanAbsolutePercentageError",
    name="MeanAbsolutePercentageError",
)
@controlled_wrapper(MeanAbsolutePercentageError, wrapper_attribute="__fnwrapped__")
def _MeanAbsolutePercentageError(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return MeanAbsolutePercentageError(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.MeanSquaredLogarithmicError",
    name="MeanSquaredLogarithmicError",
)
@controlled_wrapper(MeanSquaredLogarithmicError, wrapper_attribute="__fnwrapped__")
def _MeanSquaredLogarithmicError(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return MeanSquaredLogarithmicError(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.CosineSimilarity",
    name="CosineSimilarity",
)
@controlled_wrapper(CosineSimilarity, wrapper_attribute="__fnwrapped__")
def _CosineSimilarity(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return CosineSimilarity(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.Huber",
    name="Huber",
)
@controlled_wrapper(Huber, wrapper_attribute="__fnwrapped__")
def _Huber(
    delta: float = 1.0,
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return Huber(
        delta=delta,
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.LogCosh",
    name="LogCosh",
)
@controlled_wrapper(LogCosh, wrapper_attribute="__fnwrapped__")
def _LogCosh(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return LogCosh(
        reduction=reduction,
    )


REGRESSION_NODE_SHELFE = Shelf(
    nodes=[
        _MeanSquaredError,
        _MeanAbsoluteError,
        _MeanAbsolutePercentageError,
        _MeanSquaredLogarithmicError,
        _CosineSimilarity,
        _Huber,
        _LogCosh,
    ],
    subshelves=[],
    name="Regression",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.losses.Hinge",
    name="Hinge",
)
@controlled_wrapper(Hinge, wrapper_attribute="__fnwrapped__")
def _Hinge(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return Hinge(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.SquaredHinge",
    name="SquaredHinge",
)
@controlled_wrapper(SquaredHinge, wrapper_attribute="__fnwrapped__")
def _SquaredHinge(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return SquaredHinge(
        reduction=reduction,
    )


@NodeDecorator(
    node_id="tensorflow.keras.losses.CategoricalHinge",
    name="CategoricalHinge",
)
@controlled_wrapper(CategoricalHinge, wrapper_attribute="__fnwrapped__")
def _CategoricalHinge(
    reduction: Reduction = Reduction.default(),
) -> Loss:
    if isinstance(reduction, Reduction):
        reduction = reduction.value
    return CategoricalHinge(
        reduction=reduction,
    )


HINGE_NODE_SHELFE = Shelf(
    nodes=[_Hinge, _SquaredHinge, _CategoricalHinge],
    subshelves=[],
    name="Hinge",
    description="Hinge losses for 'maximum-margin' classification",
)

LOSSES_NODE_SHELFE = Shelf(
    nodes=[],
    subshelves=[PROBABILISTIC_NODE_SHELFE, REGRESSION_NODE_SHELFE, HINGE_NODE_SHELFE],
    name="Losses",
    description="The purpose of loss functions is to compute the quantity that a model should seek to minimize during training.",
)
