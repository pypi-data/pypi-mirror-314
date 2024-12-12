from typing import Optional, Union, Sequence, Callable
from enum import Enum
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from tensorflow.keras import KerasTensor
from tensorflow.keras.initializers import Initializer
from tensorflow.keras.regularizers import Regularizer
from tensorflow.keras.constraints import Constraint
from tensorflow.keras.layers import (
    Input,
    Dense,
    MaxPooling1D,
    MaxPooling2D,
    MaxPooling3D,
    AveragePooling1D,
    AveragePooling2D,
    AveragePooling3D,
    GlobalMaxPooling1D,
    GlobalMaxPooling2D,
    GlobalMaxPooling3D,
    GlobalAveragePooling1D,
    GlobalAveragePooling2D,
    GlobalAveragePooling3D,
    Conv1D,
    Conv2D,
    Conv3D,
    Dropout,
    Flatten,
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
    node_id="tensorflow.keras.layers.Input",
    name="Input",
)
@controlled_wrapper(Input, wrapper_attribute="__fnwrapped__")
def _Input(
    shape_1_height_or_sequence_length: Optional[int] = None,
    shape_2_width_or_input_dim: Optional[int] = None,
    shape_3_channels: Optional[int] = None,
    batch_size: Optional[int] = None,
    name: Optional[str] = None,
    dtype: DataType = DataType.default(),
    sparse: bool = False,
    tensor: Optional[KerasTensor] = None,
) -> Callable[[], KerasTensor]:
    if shape_3_channels is None:
        shape = (shape_1_height_or_sequence_length, shape_2_width_or_input_dim)
    if shape_3_channels is None and shape_2_width_or_input_dim == 1:
        shape = (shape_1_height_or_sequence_length,)
    if shape_3_channels is not None:
        shape = (
            shape_1_height_or_sequence_length,
            shape_2_width_or_input_dim,
            shape_3_channels,
        )
    if isinstance(dtype, DataType):
        dtype = dtype.value
    return Input(
        shape=shape,
        batch_size=batch_size,
        name=name,
        dtype=dtype,
        sparse=sparse,
        tensor=tensor,
    )


class Activation(Enum):
    relu = "relu"
    sigmoid = "sigmoid"
    softmax = "softmax"
    tanh = "tanh"
    linear = "linear"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


@NodeDecorator(
    node_id="tensorflow.keras.layers.Dense",
    name="Dense",
)
@controlled_wrapper(Dense, wrapper_attribute="__fnwrapped__")
def _Dense(
    input_model: KerasTensor,
    units: int,
    activation: Activation = Activation.default(),
    use_bias: bool = True,
    kernel_initializer: Union[str, Initializer] = "glorot_uniform",
    bias_initializer: Union[str, Initializer] = "zeros",
    kernel_regularizer: Optional[Regularizer] = None,
    bias_regularizer: Optional[Regularizer] = None,
    activity_regularizer: Optional[Regularizer] = None,
    kernel_constraint: Optional[Constraint] = None,
    bias_constraint: Optional[Constraint] = None,
    lora_rank: Optional[int] = None,
) -> Callable[[], KerasTensor]:
    if isinstance(activation, Activation):
        activation = activation.value
    return Dense(
        units=units,
        activation=activation,
        use_bias=use_bias,
        kernel_initializer=kernel_initializer,
        bias_initializer=bias_initializer,
        kernel_regularizer=kernel_regularizer,
        bias_regularizer=bias_regularizer,
        activity_regularizer=activity_regularizer,
        kernel_constraint=kernel_constraint,
        bias_constraint=bias_constraint,
        lora_rank=lora_rank,
    )(input_model)


CORELAYERS_NODE_SHELFE = Shelf(
    nodes=[_Input, _Dense],
    subshelves=[],
    name="Core",
    description="",
)


class Padding(Enum):
    valid = "valid"
    same = "same"

    @classmethod
    def default(cls):
        return cls.valid.value


@NodeDecorator(
    node_id="tensorflow.keras.layers.MaxPooling1D",
    name="MaxPooling1D",
)
@controlled_wrapper(MaxPooling1D, wrapper_attribute="__fnwrapped__")
def _MaxPooling1D(
    input_model: KerasTensor,
    pool_size: int = 2,
    strides: Optional[int] = None,
    padding: Padding = Padding.default(),
    data_format: DataType = DataType.default(),
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, Padding):
        padding = padding.value
    return MaxPooling1D(
        pool_size=pool_size,
        strides=strides,
        padding=padding,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.MaxPooling2D",
    name="MaxPooling2D",
)
@controlled_wrapper(MaxPooling2D, wrapper_attribute="__fnwrapped__")
def _MaxPooling2D(
    input_model: KerasTensor,
    pool_size_1: int = 2,
    pool_size_2: int = 2,
    strides: Optional[int] = None,
    padding: Padding = Padding.default(),
    data_format: DataType = DataType.default(),
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, Padding):
        padding = padding.value
    return MaxPooling2D(
        pool_size=(pool_size_1, pool_size_2),
        strides=strides,
        padding=padding,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.MaxPooling3D",
    name="MaxPooling3D",
)
@controlled_wrapper(MaxPooling3D, wrapper_attribute="__fnwrapped__")
def _MaxPooling3D(
    input_model: KerasTensor,
    pool_size_1: int = 2,
    pool_size_2: int = 2,
    pool_size_3: int = 2,
    strides: Optional[int] = None,
    padding: Padding = Padding.default(),
    data_format: DataType = DataType.default(),
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, Padding):
        padding = padding.value
    return MaxPooling3D(
        pool_size=(pool_size_1, pool_size_2, pool_size_3),
        strides=strides,
        padding=padding,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.AveragePooling1D",
    name="AveragePooling1D",
)
@controlled_wrapper(AveragePooling1D, wrapper_attribute="__fnwrapped__")
def _AveragePooling1D(
    input_model: KerasTensor,
    pool_size: int = 2,
    strides: Optional[int] = None,
    padding: Padding = Padding.default(),
    data_format: DataType = DataType.default(),
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, Padding):
        padding = padding.value
    return AveragePooling1D(
        pool_size=pool_size,
        strides=strides,
        padding=padding,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.AveragePooling2D",
    name="AveragePooling2D",
)
@controlled_wrapper(AveragePooling2D, wrapper_attribute="__fnwrapped__")
def _AveragePooling2D(
    input_model: KerasTensor,
    pool_size_1: int = 2,
    pool_size_2: int = 2,
    strides: Optional[int] = None,
    padding: Padding = Padding.default(),
    data_format: DataType = DataType.default(),
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, Padding):
        padding = padding.value
    return AveragePooling2D(
        pool_size=(pool_size_1, pool_size_2),
        strides=strides,
        padding=padding,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.AveragePooling3D",
    name="AveragePooling3D",
)
@controlled_wrapper(AveragePooling3D, wrapper_attribute="__fnwrapped__")
def _AveragePooling3D(
    input_model: KerasTensor,
    pool_size_1: int = 2,
    pool_size_2: int = 2,
    pool_size_3: int = 2,
    strides: Optional[int] = None,
    padding: Padding = Padding.default(),
    data_format: DataType = DataType.default(),
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, Padding):
        padding = padding.value
    return AveragePooling3D(
        pool_size=(pool_size_1, pool_size_2, pool_size_3),
        strides=strides,
        padding=padding,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.GlobalMaxPooling1D",
    name="GlobalMaxPooling1D",
)
@controlled_wrapper(GlobalMaxPooling1D, wrapper_attribute="__fnwrapped__")
def _GlobalMaxPooling1D(
    input_model: KerasTensor,
    data_format: DataType = DataType.default(),
    keepdims: bool = False,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    return GlobalMaxPooling1D(
        keepdims=keepdims,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.GlobalMaxPooling2D",
    name="GlobalMaxPooling2D",
)
@controlled_wrapper(GlobalMaxPooling2D, wrapper_attribute="__fnwrapped__")
def _GlobalMaxPooling2D(
    input_model: KerasTensor,
    data_format: DataType = DataType.default(),
    keepdims: bool = False,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    return GlobalMaxPooling2D(
        keepdims=keepdims,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.GlobalMaxPooling3D",
    name="GlobalMaxPooling3D",
)
@controlled_wrapper(GlobalMaxPooling3D, wrapper_attribute="__fnwrapped__")
def _GlobalMaxPooling3D(
    input_model: KerasTensor,
    data_format: DataType = DataType.default(),
    keepdims: bool = False,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    return GlobalMaxPooling3D(
        keepdims=keepdims,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.GlobalAveragePooling1D",
    name="GlobalAveragePooling1D",
)
@controlled_wrapper(GlobalAveragePooling1D, wrapper_attribute="__fnwrapped__")
def _GlobalAveragePooling1D(
    input_model: KerasTensor,
    data_format: DataType = DataType.default(),
    keepdims: bool = False,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    return GlobalAveragePooling1D(
        keepdims=keepdims,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.GlobalAveragePooling2D",
    name="GlobalAveragePooling2D",
)
@controlled_wrapper(GlobalAveragePooling2D, wrapper_attribute="__fnwrapped__")
def _GlobalAveragePooling2D(
    input_model: KerasTensor,
    data_format: DataType = DataType.default(),
    keepdims: bool = False,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    return GlobalAveragePooling2D(
        keepdims=keepdims,
        data_format=data_format,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.GlobalAveragePooling3D",
    name="GlobalAveragePooling3D",
)
@controlled_wrapper(GlobalAveragePooling3D, wrapper_attribute="__fnwrapped__")
def _GlobalAveragePooling3D(
    input_model: KerasTensor,
    data_format: DataType = DataType.default(),
    keepdims: bool = False,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    return GlobalAveragePooling3D(
        keepdims=keepdims,
        data_format=data_format,
    )(input_model)


POOLINGLAYERS_NODE_SHELFE = Shelf(
    nodes=[
        _MaxPooling1D,
        _MaxPooling2D,
        _MaxPooling3D,
        _AveragePooling1D,
        _AveragePooling2D,
        _AveragePooling3D,
        _GlobalMaxPooling1D,
        _GlobalMaxPooling2D,
        _GlobalMaxPooling3D,
        _GlobalAveragePooling1D,
        _GlobalAveragePooling2D,
        _GlobalAveragePooling3D,
    ],
    subshelves=[],
    name="Pooling",
    description="",
)


class ConvPadding(Enum):
    valid = "valid"
    same = "same"
    causal = "causal"

    @classmethod
    def default(cls):
        return cls.valid.value


@NodeDecorator(
    node_id="tensorflow.keras.layers.Conv1D",
    name="Conv1D",
)
@controlled_wrapper(Conv1D, wrapper_attribute="__fnwrapped__")
def _Conv1D(
    input_model: KerasTensor,
    filters: int,
    kernel_size: int,
    strides: Optional[int] = None,
    padding: ConvPadding = ConvPadding.default(),
    data_format: DataType = DataType.default(),
    dilation_rate: int = 1,
    groups: int = 1,
    activation: Activation = Activation.default(),
    use_bias: bool = True,
    kernel_initializer: Union[str, Initializer] = "glorot_uniform",
    bias_initializer: Union[str, Initializer] = "zeros",
    kernel_regularizer: Optional[Regularizer] = None,
    bias_regularizer: Optional[Regularizer] = None,
    activity_regularizer: Optional[Regularizer] = None,
    kernel_constraint: Optional[Constraint] = None,
    bias_constraint: Optional[Constraint] = None,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, ConvPadding):
        padding = padding.value
    if isinstance(activation, Activation):
        activation = activation.value
    return Conv1D(
        filters=filters,
        kernel_size=kernel_size,
        strides=strides,
        padding=padding,
        data_format=data_format,
        dilation_rate=dilation_rate,
        groups=groups,
        activation=activation,
        use_bias=use_bias,
        kernel_initializer=kernel_initializer,
        bias_initializer=bias_initializer,
        kernel_regularizer=kernel_regularizer,
        bias_regularizer=bias_regularizer,
        activity_regularizer=activity_regularizer,
        kernel_constraint=kernel_constraint,
        bias_constraint=bias_constraint,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.Conv2D",
    name="Conv2D",
)
@controlled_wrapper(Conv2D, wrapper_attribute="__fnwrapped__")
def _Conv2D(
    input_model: KerasTensor,
    filters: int,
    kernel_size_1: int,
    kernel_size_2: int,
    strides_1: int = 1,
    strides_2: int = 1,
    padding: ConvPadding = ConvPadding.default(),
    data_format: DataType = DataType.default(),
    dilation_rate_1: int = 1,
    dilation_rate_2: int = 1,
    groups: int = 1,
    activation: Activation = Activation.default(),
    use_bias: bool = True,
    kernel_initializer: Union[str, Initializer] = "glorot_uniform",
    bias_initializer: Union[str, Initializer] = "zeros",
    kernel_regularizer: Optional[Regularizer] = None,
    bias_regularizer: Optional[Regularizer] = None,
    activity_regularizer: Optional[Regularizer] = None,
    kernel_constraint: Optional[Constraint] = None,
    bias_constraint: Optional[Constraint] = None,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, ConvPadding):
        padding = padding.value
    if isinstance(activation, Activation):
        activation = activation.value
    return Conv2D(
        filters=filters,
        kernel_size=(kernel_size_1, kernel_size_2),
        strides=(strides_1, strides_2),
        padding=padding,
        data_format=data_format,
        dilation_rate=(dilation_rate_1, dilation_rate_2),
        groups=groups,
        activation=activation,
        use_bias=use_bias,
        kernel_initializer=kernel_initializer,
        bias_initializer=bias_initializer,
        kernel_regularizer=kernel_regularizer,
        bias_regularizer=bias_regularizer,
        activity_regularizer=activity_regularizer,
        kernel_constraint=kernel_constraint,
        bias_constraint=bias_constraint,
    )(input_model)


@NodeDecorator(
    node_id="tensorflow.keras.layers.Conv3D",
    name="Conv3D",
)
@controlled_wrapper(Conv3D, wrapper_attribute="__fnwrapped__")
def _Conv3D(
    input_model: KerasTensor,
    filters: int,
    kernel_size_1: int,
    kernel_size_2: int,
    kernel_size_3: int,
    strides_1: int = 1,
    strides_2: int = 1,
    strides_3: int = 1,
    padding: ConvPadding = ConvPadding.default(),
    data_format: DataType = DataType.default(),
    dilation_rate_1: int = 1,
    dilation_rate_2: int = 1,
    dilation_rate_3: int = 1,
    groups: int = 1,
    activation: Activation = Activation.default(),
    use_bias: bool = True,
    kernel_initializer: Union[str, Initializer] = "glorot_uniform",
    bias_initializer: Union[str, Initializer] = "zeros",
    kernel_regularizer: Optional[Regularizer] = None,
    bias_regularizer: Optional[Regularizer] = None,
    activity_regularizer: Optional[Regularizer] = None,
    kernel_constraint: Optional[Constraint] = None,
    bias_constraint: Optional[Constraint] = None,
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    if isinstance(padding, ConvPadding):
        padding = padding.value
    if isinstance(activation, Activation):
        activation = activation.value
    return Conv3D(
        filters=filters,
        kernel_size=(kernel_size_1, kernel_size_2, kernel_size_3),
        strides=(strides_1, strides_2, strides_3),
        padding=padding.value,
        data_format=data_format,
        dilation_rate=(dilation_rate_1, dilation_rate_2, dilation_rate_3),
        groups=groups,
        activation=activation,
        use_bias=use_bias,
        kernel_initializer=kernel_initializer,
        bias_initializer=bias_initializer,
        kernel_regularizer=kernel_regularizer,
        bias_regularizer=bias_regularizer,
        activity_regularizer=activity_regularizer,
        kernel_constraint=kernel_constraint,
        bias_constraint=bias_constraint,
    )(input_model)


CONVLAYERS_NODE_SHELFE = Shelf(
    nodes=[_Conv1D, _Conv2D, _Conv3D],
    subshelves=[],
    name="Convolution",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.layers.Dropout",
    name="Dropout",
)
@controlled_wrapper(Dropout, wrapper_attribute="__fnwrapped__")
def _Dropout(
    input_model: KerasTensor,
    rate: float,
    noise_shape: Optional[Sequence[int]] = None,
    seed: Optional[int] = None,
) -> Callable[[], KerasTensor]:
    if not 0 <= rate < 1:
        raise ValueError("rate must be between 0 and 1")

    return Dropout(rate=rate, noise_shape=noise_shape, seed=seed)(input_model)


REGLAYERS_NODE_SHELFE = Shelf(
    nodes=[_Dropout],
    subshelves=[],
    name="Regularization",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.layers.Flatten",
    name="Flatten",
)
@controlled_wrapper(Flatten, wrapper_attribute="__fnwrapped__")
def _Flatten(
    input_model: KerasTensor,
    data_format: DataType = DataType.default(),
) -> Callable[[], KerasTensor]:
    if isinstance(data_format, DataType):
        data_format = data_format.value
    return Flatten(data_format=data_format)(input_model)


RESHAPINGLAYERS_NODE_SHELFE = Shelf(
    nodes=[_Flatten],
    subshelves=[],
    name="Reshaping",
    description="",
)


LAYERS_NODE_SHELFE = Shelf(
    nodes=[],
    subshelves=[
        CORELAYERS_NODE_SHELFE,
        POOLINGLAYERS_NODE_SHELFE,
        CONVLAYERS_NODE_SHELFE,
        REGLAYERS_NODE_SHELFE,
        RESHAPINGLAYERS_NODE_SHELFE,
    ],
    name="Layers",
    description="Layers are the basic building blocks of neural networks in Keras. A layer consists of a tensor-in tensor-out computation function (the layer's call method) and some state, held in TensorFlow variables (the layer's weights).",
)
