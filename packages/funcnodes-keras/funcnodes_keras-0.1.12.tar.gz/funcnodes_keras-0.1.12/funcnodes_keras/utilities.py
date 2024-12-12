from typing import Optional, Union
import numpy as np
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.ops import convert_to_tensor


@NodeDecorator(
    node_id="tensorflow.keras.utils.to_categorical",
    name="to_categorical",
)
@controlled_wrapper(to_categorical, wrapper_attribute="__fnwrapped__")
def _to_categorical(
    x: Union[list, np.ndarray],
    num_classes: Optional[int] = None,
) -> np.ndarray:
    return to_categorical(x, num_classes)


@NodeDecorator(
    node_id="tensorflow.keras.ops.convert_to_tensor",
    name="to_tensor",
)
@controlled_wrapper(convert_to_tensor, wrapper_attribute="__fnwrapped__")
def _convert_to_tensor(
    x: np.ndarray,
) -> tf.Tensor:
    return convert_to_tensor(x)


UTILS_NODE_SHELFE = Shelf(
    nodes=[_to_categorical, _convert_to_tensor],
    subshelves=[],
    name="Utilities",
    description="Python & NumPy utilities",
)
