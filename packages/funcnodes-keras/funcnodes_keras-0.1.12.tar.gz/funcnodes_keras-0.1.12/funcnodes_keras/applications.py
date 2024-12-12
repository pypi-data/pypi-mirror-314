from typing import Union, Optional, Tuple, Callable
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from enum import Enum

from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.applications import (
    Xception,
    VGG16,
    VGG19,
    ResNet50,
    ResNet50V2,
    ResNet101,
    ResNet101V2,
    ResNet152,
    ResNet152V2,
    InceptionV3,
    InceptionResNetV2,
    MobileNet,
    MobileNetV2,
    MobileNetV3Small,
    MobileNetV3Large,
    DenseNet121,
    DenseNet169,
    DenseNet201,
    NASNetLarge,
    NASNetMobile,
    EfficientNetB0,
    EfficientNetB1,
    EfficientNetB2,
    EfficientNetB3,
    EfficientNetB4,
    EfficientNetB5,
    EfficientNetB6,
    EfficientNetB7,
    EfficientNetV2B0,
    EfficientNetV2B1,
    EfficientNetV2B2,
    EfficientNetV2B3,
    EfficientNetV2S,
    EfficientNetV2M,
    EfficientNetV2L,
    ConvNeXtTiny,
    ConvNeXtSmall,
    ConvNeXtBase,
    ConvNeXtLarge,
    ConvNeXtXLarge,
)


class Weights(Enum):
    imagenet = "imagenet"
    NONE = None

    @classmethod
    def default(cls):
        return cls.imagenet.value


class Pooling(Enum):
    avg = "avg"
    max = "max"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


class ClassifierActivation(Enum):
    softmax = "softmax"
    relu = "relu"
    sigmoid = "sigmoid"
    tanh = "tanh"
    linear = "linear"
    selu = "selu"
    elu = "elu"
    exponential = "exponential"
    swish = "swish"
    gelu = "gelu"
    softplus = "softplus"
    softsign = "softsign"

    @classmethod
    def default(cls):
        return cls.softmax.value


@NodeDecorator(
    node_id="tensorflow.keras.applications.Xception",
    name="Xception",
)
@controlled_wrapper(Xception, wrapper_attribute="__fnwrapped__")
def _Xception(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 299,
    input_shape_width: int = 299,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (299, 299, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (229, 229)."
            )

        if input_shape[0] < 71 or input_shape[1] < 71:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return Xception(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.VGG16",
    name="VGG16",
)
@controlled_wrapper(VGG16, wrapper_attribute="__fnwrapped__")
def _VGG16(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return VGG16(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.VGG19",
    name="VGG19",
)
@controlled_wrapper(VGG19, wrapper_attribute="__fnwrapped__")
def _VGG19(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return VGG19(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ResNet50",
    name="ResNet50",
)
@controlled_wrapper(ResNet50, wrapper_attribute="__fnwrapped__")
def _ResNet50(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ResNet50(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ResNet50V2",
    name="ResNet50V2",
)
@controlled_wrapper(ResNet50V2, wrapper_attribute="__fnwrapped__")
def _ResNet50V2(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ResNet50V2(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ResNet101",
    name="ResNet101",
)
@controlled_wrapper(ResNet101, wrapper_attribute="__fnwrapped__")
def _ResNet101(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ResNet101(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ResNet101V2",
    name="ResNet101V2",
)
@controlled_wrapper(ResNet101V2, wrapper_attribute="__fnwrapped__")
def _ResNet101V2(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ResNet101V2(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ResNet152",
    name="ResNet152",
)
@controlled_wrapper(ResNet152, wrapper_attribute="__fnwrapped__")
def _ResNet152(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ResNet152(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ResNet152V2",
    name="ResNet152V2",
)
@controlled_wrapper(ResNet152V2, wrapper_attribute="__fnwrapped__")
def _ResNet152V2(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ResNet152V2(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.InceptionV3",
    name="InceptionV3",
)
@controlled_wrapper(InceptionV3, wrapper_attribute="__fnwrapped__")
def _InceptionV3(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 299,
    input_shape_width: int = 299,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (299, 299, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (299, 299)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return InceptionV3(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.InceptionResNetV2",
    name="InceptionResNetV2",
)
@controlled_wrapper(InceptionResNetV2, wrapper_attribute="__fnwrapped__")
def _InceptionResNetV2(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 299,
    input_shape_width: int = 299,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (299, 299, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (299, 299)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 31 or input_shape[1] < 31:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 31."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return InceptionResNetV2(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.MobileNet",
    name="MobileNet",
)
@controlled_wrapper(MobileNet, wrapper_attribute="__fnwrapped__")
def _MobileNet(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    alpha: float = 1.0,
    depth_multiplier: int = 1,
    dropout: float = 0.001,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 32."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return MobileNet(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        alpha=alpha,
        depth_multiplier=depth_multiplier,
        dropout=dropout,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.MobileNetV2",
    name="MobileNetV2",
)
@controlled_wrapper(MobileNetV2, wrapper_attribute="__fnwrapped__")
def _MobileNetV2(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    alpha: float = 1.0,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 32."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return MobileNetV2(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        alpha=alpha,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.MobileNetV3Small",
    name="MobileNetV3Small",
)
@controlled_wrapper(MobileNetV3Small, wrapper_attribute="__fnwrapped__")
def _MobileNetV3Small(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    alpha: float = 1.0,
    minimalistic: bool = False,
    dropout_rate: float = 0.2,
    include_preprocessing: bool = True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 32."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return MobileNetV3Small(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        alpha=alpha,
        minimalistic=minimalistic,
        dropout_rate=dropout_rate,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.MobileNetV3Large",
    name="MobileNetV3Large",
)
@controlled_wrapper(MobileNetV3Large, wrapper_attribute="__fnwrapped__")
def _MobileNetV3Large(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    alpha: float = 1.0,
    minimalistic: bool = False,
    dropout_rate: float = 0.2,
    include_preprocessing: bool = True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 32."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return MobileNetV3Large(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        alpha=alpha,
        minimalistic=minimalistic,
        dropout_rate=dropout_rate,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.DenseNet121",
    name="DenseNet121",
)
@controlled_wrapper(DenseNet121, wrapper_attribute="__fnwrapped__")
def _DenseNet121(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return DenseNet121(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.DenseNet169",
    name="DenseNet169",
)
@controlled_wrapper(DenseNet169, wrapper_attribute="__fnwrapped__")
def _DenseNet169(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return DenseNet169(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.DenseNet201",
    name="DenseNet201",
)
@controlled_wrapper(DenseNet201, wrapper_attribute="__fnwrapped__")
def _DenseNet201(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return DenseNet201(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.NASNetLarge",
    name="NASNetLarge",
)
@controlled_wrapper(NASNetLarge, wrapper_attribute="__fnwrapped__")
def _NASNetLarge(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 331,
    input_shape_width: int = 331,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (331, 331, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (331, 331)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return NASNetLarge(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.NASNetMobile",
    name="NASNetMobile",
)
@controlled_wrapper(NASNetMobile, wrapper_attribute="__fnwrapped__")
def _NASNetMobile(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return NASNetMobile(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB0",
    name="EfficientNetB0",
)
@controlled_wrapper(EfficientNetB0, wrapper_attribute="__fnwrapped__")
def _EfficientNetB0(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB0(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB1",
    name="EfficientNetB1",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetB1(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 240,
    input_shape_width: int = 240,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (240, 240, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (240, 240)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB1(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB2",
    name="EfficientNetB2",
)
@controlled_wrapper(EfficientNetB2, wrapper_attribute="__fnwrapped__")
def _EfficientNetB2(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 260,
    input_shape_width: int = 260,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (260, 260, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (260, 260)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB2(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB3",
    name="EfficientNetB3",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetB3(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 300,
    input_shape_width: int = 300,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (300, 300, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (300, 300)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB3(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB4",
    name="EfficientNetB4",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetB4(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 380,
    input_shape_width: int = 380,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (380, 380, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (380, 380)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB4(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB5",
    name="EfficientNetB5",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetB5(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 456,
    input_shape_width: int = 456,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (456, 456, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (456, 456)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB5(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB6",
    name="EfficientNetB6",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetB6(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 528,
    input_shape_width: int = 528,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (528, 528, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (528, 528)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB6(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetB7",
    name="EfficientNetB7",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetB7(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 600,
    input_shape_width: int = 600,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (600, 600, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (600, 600)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetB7(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetV2B0",
    name="EfficientNetV2B0",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetV2B0(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: Optional[int] = 224,
    input_shape_width: Optional[int] = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    if include_top:
        input_shape = (224, 224, 3)
    else:
        if input_shape_height is None or input_shape_width is None:
            raise ValueError("If top is not included provide height and width")
        input_shape = (int(input_shape_height), int(input_shape_width), 3)

    if input_shape[0] < 32 or input_shape[1] < 32:
        raise ValueError(
            "input_shape dimensions (height, width) must be no smaller than 71."
        )

    return EfficientNetV2B0(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetV2B1",
    name="EfficientNetV2B1",
)
@controlled_wrapper(EfficientNetV2B1, wrapper_attribute="__fnwrapped__")
def _EfficientNetV2B1(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 240,
    input_shape_width: int = 240,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (240, 240, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (240, 240)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetV2B1(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetV2B2",
    name="EfficientNetV2B2",
)
@controlled_wrapper(EfficientNetV2B2, wrapper_attribute="__fnwrapped__")
def _EfficientNetV2B2(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 260,
    input_shape_width: int = 260,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (260, 260, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (260, 260)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetV2B2(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetV2B3",
    name="EfficientNetV2B3",
)
@controlled_wrapper(EfficientNetV2B3, wrapper_attribute="__fnwrapped__")
def _EfficientNetV2B3(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 300,
    input_shape_width: int = 300,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (300, 300, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (300, 300)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetV2B3(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetV2S",
    name="EfficientNetV2S",
)
@controlled_wrapper(EfficientNetB1, wrapper_attribute="__fnwrapped__")
def _EfficientNetV2S(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 384,
    input_shape_width: int = 384,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (384, 384, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (384, 384)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetV2S(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetV2M",
    name="EfficientNetV2M",
)
@controlled_wrapper(EfficientNetV2M, wrapper_attribute="__fnwrapped__")
def _EfficientNetV2M(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 480,
    input_shape_width: int = 480,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (480, 480, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (480, 480)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetV2M(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.EfficientNetV2L",
    name="EfficientNetV2L",
)
@controlled_wrapper(EfficientNetV2L, wrapper_attribute="__fnwrapped__")
def _EfficientNetV2L(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 480,
    input_shape_width: int = 480,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (480, 480, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (480, 480)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return EfficientNetV2L(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ConvNeXtTiny",
    name="ConvNeXtTiny",
)
@controlled_wrapper(ConvNeXtTiny, wrapper_attribute="__fnwrapped__")
def _ConvNeXtTiny(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ConvNeXtTiny(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ConvNeXtSmall",
    name="ConvNeXtSmall",
)
@controlled_wrapper(ConvNeXtSmall, wrapper_attribute="__fnwrapped__")
def _ConvNeXtSmall(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ConvNeXtSmall(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ConvNeXtBase",
    name="ConvNeXtBase",
)
@controlled_wrapper(ConvNeXtBase, wrapper_attribute="__fnwrapped__")
def _ConvNeXtBase(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ConvNeXtBase(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ConvNeXtLarge",
    name="ConvNeXtLarge",
)
@controlled_wrapper(ConvNeXtLarge, wrapper_attribute="__fnwrapped__")
def _ConvNeXtLarge(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ConvNeXtLarge(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


@NodeDecorator(
    node_id="tensorflow.keras.applications.ConvNeXtXLarge",
    name="ConvNeXtXLarge",
)
@controlled_wrapper(ConvNeXtXLarge, wrapper_attribute="__fnwrapped__")
def _ConvNeXtXLarge(
    include_top: bool = True,
    weights: Weights = Weights.default(),
    input_tensor: Optional[Input] = None,
    input_shape_height: int = 224,
    input_shape_width: int = 224,
    pooling: Pooling = Pooling.default(),
    classes: int = 1000,
    classifier_activation: Optional[
        Union[ClassifierActivation, Callable]
    ] = ClassifierActivation.default(),
    include_preprocessing=True,
) -> Callable[[], Model]:
    if isinstance(classifier_activation, ClassifierActivation):
        classifier_activation = classifier_activation.value
    if isinstance(pooling, Pooling):
        pooling = pooling.value
    if isinstance(weights, Weights):
        weights = weights.value

    input_shape: Tuple[int, int, int] = (input_shape_height, input_shape_width, 3)
    # Validate input_shape
    if input_shape is not None:
        if include_top and input_shape != (224, 224, 3):
            raise ValueError(
                "if include_top is True, the (input_shape_height, input_shape_width) has to be (224, 224)."
            )
        if len(input_shape) != 3 or input_shape[2] != 3:
            raise ValueError(
                "input_shape must be a tuple of three integers (height, width, 3)."
            )
        if input_shape[0] < 32 or input_shape[1] < 32:
            raise ValueError(
                "input_shape dimensions (height, width) must be no smaller than 71."
            )
    elif not include_top:
        input_shape = (input_shape_height, input_shape_width, 3)

    return ConvNeXtXLarge(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes,
        classifier_activation=classifier_activation,
        include_preprocessing=include_preprocessing,
    )


APPLICATION_NODE_SHELFE = Shelf(
    nodes=[
        _Xception,
        _VGG16,
        _VGG19,
        _ResNet50,
        _ResNet50V2,
        _ResNet101,
        _ResNet101V2,
        _ResNet152,
        _ResNet152V2,
        _InceptionV3,
        _InceptionResNetV2,
        _MobileNet,
        _MobileNetV2,
        _MobileNetV3Small,
        _MobileNetV3Large,
        _DenseNet121,
        _DenseNet169,
        _DenseNet201,
        _NASNetLarge,
        _NASNetMobile,
        _EfficientNetB0,
        _EfficientNetB1,
        _EfficientNetB1,
        _EfficientNetB2,
        _EfficientNetB3,
        _EfficientNetB4,
        _EfficientNetB5,
        _EfficientNetB6,
        _EfficientNetB7,
        _EfficientNetV2B0,
        _EfficientNetV2B1,
        _EfficientNetV2B2,
        _EfficientNetV2B2,
        _EfficientNetV2B3,
        _EfficientNetV2S,
        _EfficientNetV2M,
        _EfficientNetV2L,
        _ConvNeXtTiny,
        _ConvNeXtSmall,
        _ConvNeXtBase,
        _ConvNeXtLarge,
        _ConvNeXtXLarge,
    ],
    subshelves=[],
    name="Applications",
    description="Keras Applications are deep learning models that"
    + "are made available alongside pre-trained weights. "
    + "These models can be used for prediction, feature "
    + "extraction, and fine-tuning.Weights are downloaded "
    + "automatically when instantiating a model. "
    + "They are stored at ~/.keras/models/.Upon instantiation, "
    + "the models will be built according to the image data format"
    + "set in your Keras configuration file at ~/.keras/keras.json. "
    + "For instance, if you have set image_data_format=channels_last, "
    + "then any model loaded from this repository will get built "
    + "according to the data format convention 'Height-Width-Depth'.",
)
