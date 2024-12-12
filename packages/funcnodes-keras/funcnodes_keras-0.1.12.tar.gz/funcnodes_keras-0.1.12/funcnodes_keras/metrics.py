from typing import Union, Optional, List
import numpy as np
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from enum import Enum
from tensorflow.keras.metrics import (
    Metric,
    Accuracy,
    BinaryAccuracy,
    CategoricalAccuracy,
    SparseCategoricalAccuracy,
    TopKCategoricalAccuracy,
    SparseTopKCategoricalAccuracy,
    BinaryCrossentropy,
    CategoricalCrossentropy,
    SparseCategoricalCrossentropy,
    KLDivergence,
    Poisson,
    MeanSquaredError,
    RootMeanSquaredError,
    MeanAbsoluteError,
    MeanAbsolutePercentageError,
    MeanSquaredLogarithmicError,
    CosineSimilarity,
    LogCoshError,
    R2Score,
    AUC,
    Precision,
    Recall,
    TruePositives,
    TrueNegatives,
    FalsePositives,
    FalseNegatives,
    PrecisionAtRecall,
    RecallAtPrecision,
    SensitivityAtSpecificity,
    SpecificityAtSensitivity,
    F1Score,
    FBetaScore,
    IoU,
    BinaryIoU,
    OneHotIoU,
    OneHotMeanIoU,
    MeanIoU,
    Hinge,
    SquaredHinge,
    CategoricalHinge,
)


class DataType(Enum):
    float16 = "float16"
    float32 = "float32"
    float64 = "float64"
    int16 = "int16"
    int32 = "int32"
    int64 = "int64"
    uint8 = "uint8"
    bool = "bool"
    string = "string"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


@NodeDecorator(
    node_id="tensorflow.keras.metrics.Accuracy",
    name="Accuracy",
)
@controlled_wrapper(Accuracy, wrapper_attribute="__fnwrapped__")
def _Accuracy(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return Accuracy(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.BinaryAccuracy",
    name="BinaryAccuracy",
)
@controlled_wrapper(BinaryAccuracy, wrapper_attribute="__fnwrapped__")
def _BinaryAccuracy(
    dtype: DataType = DataType.default(),
    threshold: Optional[float] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if threshold is not None and not 0 <= threshold < 1:
        raise ValueError("threshold must be between 0 and 1")
    return BinaryAccuracy(dtype=dtype, threshold=threshold)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.CategoricalAccuracy",
    name="CategoricalAccuracy",
)
@controlled_wrapper(CategoricalAccuracy, wrapper_attribute="__fnwrapped__")
def _CategoricalAccuracy(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return CategoricalAccuracy(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.SparseCategoricalAccuracy",
    name="SparseCategoricalAccuracy",
)
@controlled_wrapper(SparseCategoricalAccuracy, wrapper_attribute="__fnwrapped__")
def _SparseCategoricalAccuracy(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return SparseCategoricalAccuracy(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.TopKCategoricalAccuracy",
    name="TopKCategoricalAccuracy",
)
@controlled_wrapper(TopKCategoricalAccuracy, wrapper_attribute="__fnwrapped__")
def _TopKCategoricalAccuracy(
    k: int = 5,
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return TopKCategoricalAccuracy(k=k, dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.SparseTopKCategoricalAccuracy",
    name="SparseTopKCategoricalAccuracy",
)
@controlled_wrapper(SparseTopKCategoricalAccuracy, wrapper_attribute="__fnwrapped__")
def _SparseTopKCategoricalAccuracy(
    k: int = 5,
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return SparseTopKCategoricalAccuracy(k=k, dtype=dtype)


ACCURACY_NODE_SHELFE = Shelf(
    nodes=[
        _Accuracy,
        _BinaryAccuracy,
        _CategoricalAccuracy,
        _SparseCategoricalAccuracy,
        _TopKCategoricalAccuracy,
        _SparseTopKCategoricalAccuracy,
    ],
    subshelves=[],
    name="Accuracy ",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.BinaryCrossentropy",
    name="BinaryCrossentropy",
)
@controlled_wrapper(BinaryCrossentropy, wrapper_attribute="__fnwrapped__")
def _BinaryCrossentropy(
    name: Optional[str] = None,
    dtype: DataType = DataType.default(),
    from_logits: bool = False,
    label_smoothing: float = 0.0,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if not 0 <= label_smoothing < 1:
        raise ValueError("label_smoothing must be between 0 and 1")
    return BinaryCrossentropy(
        name=name, dtype=dtype, from_logits=from_logits, label_smoothing=label_smoothing
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.CategoricalCrossentropy",
    name="CategoricalCrossentropy",
)
@controlled_wrapper(CategoricalCrossentropy, wrapper_attribute="__fnwrapped__")
def _CategoricalCrossentropy(
    name: Optional[str] = None,
    dtype: DataType = DataType.default(),
    from_logits: bool = False,
    label_smoothing: float = 0.0,
    axis: int = -1,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if not 0 <= label_smoothing < 1:
        raise ValueError("label_smoothing must be between 0 and 1")

    return CategoricalCrossentropy(
        name=name,
        dtype=dtype,
        from_logits=from_logits,
        label_smoothing=label_smoothing,
        axis=axis,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.SparseCategoricalCrossentropy",
    name="SparseCategoricalCrossentropy",
)
@controlled_wrapper(SparseCategoricalCrossentropy, wrapper_attribute="__fnwrapped__")
def _SparseCategoricalCrossentropy(
    name: Optional[str] = None,
    dtype: DataType = DataType.default(),
    from_logits: bool = False,
    axis: int = -1,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return SparseCategoricalCrossentropy(
        name=name,
        dtype=dtype,
        from_logits=from_logits,
        axis=axis,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.KLDivergence",
    name="KLDivergence",
)
@controlled_wrapper(KLDivergence, wrapper_attribute="__fnwrapped__")
def _KLDivergence(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return KLDivergence(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.Poisson",
    name="Poisson",
)
@controlled_wrapper(Poisson, wrapper_attribute="__fnwrapped__")
def _Poisson(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return Poisson(dtype=dtype)


PROBABILISTIC_NODE_SHELFE = Shelf(
    nodes=[
        _BinaryCrossentropy,
        _CategoricalCrossentropy,
        _SparseCategoricalCrossentropy,
        _KLDivergence,
        _Poisson,
    ],
    subshelves=[],
    name="Probabilistic  ",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.MeanSquaredError",
    name="MeanSquaredError",
)
@controlled_wrapper(MeanSquaredError, wrapper_attribute="__fnwrapped__")
def _MeanSquaredError(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return MeanSquaredError(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.RootMeanSquaredError",
    name="RootMeanSquaredError",
)
@controlled_wrapper(RootMeanSquaredError, wrapper_attribute="__fnwrapped__")
def _RootMeanSquaredError(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return RootMeanSquaredError(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.MeanAbsoluteError",
    name="MeanAbsoluteError",
)
@controlled_wrapper(MeanAbsoluteError, wrapper_attribute="__fnwrapped__")
def _MeanAbsoluteError(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return MeanAbsoluteError(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.MeanAbsolutePercentageError",
    name="MeanAbsolutePercentageError",
)
@controlled_wrapper(MeanAbsolutePercentageError, wrapper_attribute="__fnwrapped__")
def _MeanAbsolutePercentageError(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return MeanAbsolutePercentageError(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.MeanSquaredLogarithmicError",
    name="MeanSquaredLogarithmicError",
)
@controlled_wrapper(MeanSquaredLogarithmicError, wrapper_attribute="__fnwrapped__")
def _MeanSquaredLogarithmicError(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return MeanSquaredLogarithmicError(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.CosineSimilarity",
    name="CosineSimilarity",
)
@controlled_wrapper(CosineSimilarity, wrapper_attribute="__fnwrapped__")
def _CosineSimilarity(
    dtype: DataType = DataType.default(),
    axis: int = -1,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return CosineSimilarity(dtype=dtype, axis=axis)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.LogCoshError",
    name="LogCoshError",
)
@controlled_wrapper(LogCoshError, wrapper_attribute="__fnwrapped__")
def _LogCoshError(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return LogCoshError(dtype=dtype)


class ClassAggregation(Enum):
    uniform_average = "uniform_average"
    variance_weighted_average = "variance_weighted_average"
    NONE = None

    @classmethod
    def default(cls):
        return cls.uniform_average.value


@NodeDecorator(
    node_id="tensorflow.keras.metrics.R2Score",
    name="R2Score",
)
@controlled_wrapper(R2Score, wrapper_attribute="__fnwrapped__")
def _R2Score(
    class_aggregation: ClassAggregation = ClassAggregation.default(),
    num_regressors: int = 0,
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if isinstance(class_aggregation, ClassAggregation):
        class_aggregation = class_aggregation.value
    return R2Score(
        class_aggregation=class_aggregation, num_regressors=num_regressors, dtype=dtype
    )


REGRESSION_NODE_SHELFE = Shelf(
    nodes=[
        _MeanSquaredError,
        _RootMeanSquaredError,
        _MeanAbsoluteError,
        _MeanAbsolutePercentageError,
        _MeanSquaredLogarithmicError,
        _CosineSimilarity,
        _LogCoshError,
        _R2Score,
    ],
    subshelves=[],
    name="Probabilistic  ",
    description="",
)


class Curve(Enum):
    ROC = "ROC"
    PR = "PR"

    @classmethod
    def default(cls):
        return cls.ROC.value


class SummationMethod(Enum):
    interpolation = "interpolation"
    minoring = "minoring"
    majoring = "majoring"

    @classmethod
    def default(cls):
        return cls.interpolation.value


@NodeDecorator(
    node_id="tensorflow.keras.metrics.AUC",
    name="AUC",
)
@controlled_wrapper(AUC, wrapper_attribute="__fnwrapped__")
def _AUC(
    num_thresholds: int = 200,
    curve: Curve = Curve.default(),
    summation_method: SummationMethod = SummationMethod.default(),
    dtype: DataType = DataType.default(),
    thresholds: Optional[List[float]] = None,
    multi_label: bool = False,
    num_labels: Optional[int] = None,
    label_weights: Optional[Union[List[float], np.ndarray]] = None,
    from_logits: bool = False,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if isinstance(curve, Curve):
        curve = curve.value
    if isinstance(summation_method, SummationMethod):
        summation_method = summation_method.value

    return AUC(
        num_thresholds=num_thresholds,
        curve=curve,
        summation_method=summation_method,
        dtype=dtype,
        thresholds=thresholds,
        multi_label=multi_label,
        num_labels=num_labels,
        label_weights=label_weights,
        from_logits=from_logits,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.Precision",
    name="Precision",
)
@controlled_wrapper(Precision, wrapper_attribute="__fnwrapped__")
def _Precision(
    dtype: DataType = DataType.default(),
    thresholds: Optional[Union[float, List[float]]] = None,
    top_k: Optional[int] = None,
    class_id: Optional[int] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return Precision(
        top_k=top_k,
        class_id=class_id,
        dtype=dtype,
        thresholds=thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.Recall",
    name="Recall",
)
@controlled_wrapper(Recall, wrapper_attribute="__fnwrapped__")
def _Recall(
    dtype: DataType = DataType.default(),
    thresholds: Optional[Union[float, List[float]]] = None,
    top_k: Optional[int] = None,
    class_id: Optional[int] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return Recall(
        top_k=top_k,
        class_id=class_id,
        dtype=dtype,
        thresholds=thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.TruePositives",
    name="TruePositives",
)
@controlled_wrapper(TruePositives, wrapper_attribute="__fnwrapped__")
def _TruePositives(
    dtype: DataType = DataType.default(),
    thresholds: Union[float, List[float]] = 0.5,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return TruePositives(
        dtype=dtype,
        thresholds=thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.TrueNegatives",
    name="TrueNegatives",
)
@controlled_wrapper(TrueNegatives, wrapper_attribute="__fnwrapped__")
def _TrueNegatives(
    dtype: DataType = DataType.default(),
    thresholds: Union[float, List[float]] = 0.5,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return TrueNegatives(
        dtype=dtype,
        thresholds=thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.FalsePositives",
    name="FalsePositives",
)
@controlled_wrapper(FalsePositives, wrapper_attribute="__fnwrapped__")
def _FalsePositives(
    dtype: DataType = DataType.default(),
    thresholds: Union[float, List[float]] = 0.5,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return FalsePositives(
        dtype=dtype,
        thresholds=thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.FalseNegatives",
    name="FalseNegatives",
)
@controlled_wrapper(FalseNegatives, wrapper_attribute="__fnwrapped__")
def _FalseNegatives(
    dtype: DataType = DataType.default(),
    thresholds: Union[float, List[float]] = 0.5,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return FalseNegatives(
        dtype=dtype,
        thresholds=thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.PrecisionAtRecall",
    name="PrecisionAtRecall",
)
@controlled_wrapper(PrecisionAtRecall, wrapper_attribute="__fnwrapped__")
def _PrecisionAtRecall(
    recall: float,
    dtype: DataType = DataType.default(),
    num_thresholds: int = 200,
    class_id: Optional[int] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if not 0 <= recall < 1:
        raise ValueError("recall must be between 0 and 1")
    return PrecisionAtRecall(
        recall=recall,
        class_id=class_id,
        dtype=dtype,
        num_thresholds=num_thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.RecallAtPrecision",
    name="RecallAtPrecision",
)
@controlled_wrapper(RecallAtPrecision, wrapper_attribute="__fnwrapped__")
def _RecallAtPrecision(
    precision: float,
    dtype: DataType = DataType.default(),
    num_thresholds: int = 200,
    class_id: Optional[int] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if not 0 <= precision < 1:
        raise ValueError("precision must be between 0 and 1")
    return RecallAtPrecision(
        precision=precision,
        class_id=class_id,
        dtype=dtype,
        num_thresholds=num_thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.SensitivityAtSpecificity",
    name="SensitivityAtSpecificity",
)
@controlled_wrapper(SensitivityAtSpecificity, wrapper_attribute="__fnwrapped__")
def _SensitivityAtSpecificity(
    specificity: float,
    dtype: DataType = DataType.default(),
    num_thresholds: int = 200,
    class_id: Optional[int] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if not 0 <= specificity < 1:
        raise ValueError("specificity must be between 0 and 1")
    return SensitivityAtSpecificity(
        specificity=specificity,
        class_id=class_id,
        dtype=dtype,
        num_thresholds=num_thresholds,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.SpecificityAtSensitivity",
    name="SpecificityAtSensitivity",
)
@controlled_wrapper(SpecificityAtSensitivity, wrapper_attribute="__fnwrapped__")
def _SpecificityAtSensitivity(
    sensitivity: float,
    dtype: DataType = DataType.default(),
    num_thresholds: int = 200,
    class_id: Optional[int] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if not 0 <= sensitivity < 1:
        raise ValueError("sensitivity must be between 0 and 1")
    return SpecificityAtSensitivity(
        sensitivity=sensitivity,
        class_id=class_id,
        dtype=dtype,
        num_thresholds=num_thresholds,
    )


class Average(Enum):
    NONE = None
    micro = "micro"
    macro = "macro"
    weighted = "weighted"

    @classmethod
    def default(cls):
        return cls.NONE.value


@NodeDecorator(
    node_id="tensorflow.keras.metrics.F1Score",
    name="F1Score",
)
@controlled_wrapper(F1Score, wrapper_attribute="__fnwrapped__")
def _F1Score(
    average: Average = Average.default(),
    dtype: DataType = DataType.default(),
    threshold: Optional[float] = None,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if isinstance(average, Average):
        average = Average.average
    if threshold is not None and 0 <= threshold < 1:
        raise ValueError("threshold must be between 0 and 1")
    return F1Score(average=average, dtype=dtype, threshold=threshold)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.FBetaScore",
    name="FBetaScore",
)
@controlled_wrapper(FBetaScore, wrapper_attribute="__fnwrapped__")
def _FBetaScore(
    average: Average = Average.default(),
    dtype: DataType = DataType.default(),
    threshold: Optional[float] = None,
    beta: float = 1.0,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if isinstance(average, Average):
        average = Average(average)
    if threshold is not None and 0 <= threshold < 1:
        raise ValueError("threshold must be between 0 and 1")

    return FBetaScore(average=average, dtype=dtype, threshold=threshold, beta=beta)


CLASSIFICATION_NODE_SHELFE = Shelf(
    nodes=[
        _AUC,
        _Precision,
        _Recall,
        _TruePositives,
        _TrueNegatives,
        _FalsePositives,
        _FalseNegatives,
        _PrecisionAtRecall,
        _RecallAtPrecision,
        _SensitivityAtSpecificity,
        _SpecificityAtSensitivity,
        _F1Score,
        _FBetaScore,
    ],
    subshelves=[],
    name="Classification",
    description="Classification metrics based on True/False positives & negatives",
)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.IoU",
    name="IoU",
)
@controlled_wrapper(IoU, wrapper_attribute="__fnwrapped__")
def _IoU(
    num_classes: int,
    target_class_ids: Union[list, tuple],
    dtype: DataType = DataType.default(),
    ignore_class: Optional[int] = None,
    sparse_y_true: bool = True,
    sparse_y_pred: bool = True,
    axis: int = -1,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return IoU(
        num_classes=num_classes,
        target_class_ids=target_class_ids,
        dtype=dtype,
        ignore_class=ignore_class,
        sparse_y_true=sparse_y_true,
        sparse_y_pred=sparse_y_pred,
        axis=axis,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.BinaryIoU",
    name="BinaryIoU",
)
@controlled_wrapper(BinaryIoU, wrapper_attribute="__fnwrapped__")
def _BinaryIoU(
    target_class_ids: Union[list, tuple],
    threshold: float = 0.5,
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    if not 0 <= threshold < 1:
        raise ValueError("threshold must be between 0 and 1")
    return BinaryIoU(
        target_class_ids=target_class_ids,
        dtype=dtype,
        threshold=threshold,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.OneHotIoU",
    name="OneHotIoU",
)
@controlled_wrapper(OneHotIoU, wrapper_attribute="__fnwrapped__")
def _OneHotIoU(
    num_classes: int,
    target_class_ids: Union[list, tuple],
    dtype: DataType = DataType.default(),
    ignore_class: Optional[int] = None,
    sparse_y_pred: bool = True,
    axis: int = -1,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return OneHotIoU(
        num_classes=num_classes,
        target_class_ids=target_class_ids,
        dtype=dtype,
        ignore_class=ignore_class,
        sparse_y_pred=sparse_y_pred,
        axis=axis,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.OneHotMeanIoU",
    name="OneHotMeanIoU",
)
@controlled_wrapper(OneHotMeanIoU, wrapper_attribute="__fnwrapped__")
def _OneHotMeanIoU(
    num_classes: int,
    dtype: DataType = DataType.default(),
    ignore_class: Optional[int] = None,
    sparse_y_pred: bool = True,
    axis: int = -1,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return OneHotMeanIoU(
        num_classes=num_classes,
        dtype=dtype,
        ignore_class=ignore_class,
        sparse_y_pred=sparse_y_pred,
        axis=axis,
    )


@NodeDecorator(
    node_id="tensorflow.keras.metrics.MeanIoU",
    name="MeanIoU",
)
@controlled_wrapper(MeanIoU, wrapper_attribute="__fnwrapped__")
def _MeanIoU(
    num_classes: int,
    dtype: DataType = DataType.default(),
    ignore_class: Optional[int] = None,
    sparse_y_true: bool = True,
    sparse_y_pred: bool = True,
    axis: int = -1,
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value

    return MeanIoU(
        num_classes=num_classes,
        dtype=dtype,
        ignore_class=ignore_class,
        sparse_y_true=sparse_y_true,
        sparse_y_pred=sparse_y_pred,
        axis=axis,
    )


IMAGE_SEGMENTATION_NODE_SHELFE = Shelf(
    nodes=[_IoU, _BinaryIoU, _OneHotIoU, _OneHotMeanIoU, _MeanIoU],
    subshelves=[],
    name="Image segmentation",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.Hinge",
    name="Hinge",
)
@controlled_wrapper(Hinge, wrapper_attribute="__fnwrapped__")
def _Hinge(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return Hinge(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.SquaredHinge",
    name="SquaredHinge",
)
@controlled_wrapper(SquaredHinge, wrapper_attribute="__fnwrapped__")
def _SquaredHinge(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return SquaredHinge(dtype=dtype)


@NodeDecorator(
    node_id="tensorflow.keras.metrics.CategoricalHinge",
    name="CategoricalHinge",
)
@controlled_wrapper(CategoricalHinge, wrapper_attribute="__fnwrapped__")
def _CategoricalHinge(
    dtype: DataType = DataType.default(),
) -> Metric:
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return CategoricalHinge(dtype=dtype)


HINGE_NODE_SHELFE = Shelf(
    nodes=[_Hinge, _SquaredHinge, _CategoricalHinge],
    subshelves=[],
    name="Hinge",
    description="Hinge metrics for 'maximum-margin' classification",
)


METRICS_NODE_SHELFE = Shelf(
    nodes=[],
    subshelves=[
        ACCURACY_NODE_SHELFE,
        PROBABILISTIC_NODE_SHELFE,
        REGRESSION_NODE_SHELFE,
        CLASSIFICATION_NODE_SHELFE,
        IMAGE_SEGMENTATION_NODE_SHELFE,
        HINGE_NODE_SHELFE,
    ],
    name="Metrics ",
    description="A metric is a function that is used to judge the performance of your model./n "
    + "Metric functions are similar to loss functions, except that the results from evaluating a metric "
    + "are not used when training the model. Note that you may use any loss function as a metric.",
)
