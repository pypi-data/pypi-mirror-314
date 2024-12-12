from typing import Callable
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from tensorflow.keras.models import Model
from tensorflow.keras import KerasTensor, Sequential


@NodeDecorator(
    node_id="tensorflow.keras.models.Model",
    name="Model",
)
@controlled_wrapper(Model, wrapper_attribute="__fnwrapped__")
def _Model(
    input: KerasTensor,
    output: KerasTensor,
) -> Callable[[], Model]:
    return Model(inputs=input, outputs=output)


MODEL_NODE_SHELFE = Shelf(
    nodes=[_Model],
    subshelves=[],
    name="Models ",
    description="",
)


@NodeDecorator(
    node_id="tensorflow.keras.Sequential",
    name="Sequential",
)
@controlled_wrapper(Sequential, wrapper_attribute="__fnwrapped__")
def _Sequential() -> Callable[[], Model]:
    return Sequential()


@NodeDecorator(
    node_id="tensorflow.keras.add",
    name="add",
)
def _add(sequential_model: Model, input: KerasTensor) -> Callable[[], Model]:
    return sequential_model.add(input)


SEQUENTIAL_NODE_SHELFE = Shelf(
    nodes=[_Sequential, _add],
    subshelves=[],
    name="Sequential",
    description="",
)


MODELS_NODE_SHELFE = Shelf(
    nodes=[],
    subshelves=[MODEL_NODE_SHELFE],
    name="Models ",
    description="There are three ways to create Keras models:The Sequential model, which is very straightforward (a simple list of layers), but is limited to single-input, single-output stacks of layers (as the name gives away). The Functional API, which is an easy-to-use, fully-featured API that supports arbitrary model architectures. For most people and most use cases, this is what you should be using. This is the Keras 'industry strength' model. Model subclassing, where you implement everything from scratch on your own. Use this if you have complex, out-of-the-box research use cases.",
)
