from typing import Literal, Union, Optional, Iterator, Tuple, Callable, List
import numpy as np
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from enum import Enum
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.metrics import Metric
from tensorflow.keras.callbacks import Callback, History
from tensorflow.keras.datasets import (
    mnist,
    cifar10,
    cifar100,
    imdb,
    reuters,
    fashion_mnist,
    california_housing,
)


@NodeDecorator(
    node_id="tensorflow.keras.datasets.mnist ",
    name="mnist ",
    outputs=[
        {"name": "x_train"},
        {"name": "y_train"},
        {"name": "x_test"},
        {"name": "y_test"},
    ],
)
def _mnist() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    return x_train, y_train, x_test, y_test


@NodeDecorator(
    node_id="tensorflow.keras.datasets.cifar10 ",
    name="cifar10 ",
    outputs=[
        {"name": "x_train"},
        {"name": "y_train"},
        {"name": "x_test"},
        {"name": "y_test"},
    ],
)
def _cifar10() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    return x_train, y_train, x_test, y_test


class LabelMode(Enum):
    fine = "fine"
    coarse = "coarse"

    @classmethod
    def default(cls):
        return cls.fine.value


@NodeDecorator(
    node_id="tensorflow.keras.datasets.cifar100 ",
    name="cifar100 ",
    outputs=[
        {"name": "x_train"},
        {"name": "y_train"},
        {"name": "x_test"},
        {"name": "y_test"},
    ],
)
def _cifar100(
    label_mode: LabelMode = LabelMode.default(),
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if isinstance(label_mode, LabelMode):
        label_mode = label_mode.value
    (x_train, y_train), (x_test, y_test) = cifar100.load_data(label_mode=label_mode)
    return x_train, y_train, x_test, y_test


@NodeDecorator(
    node_id="tensorflow.keras.datasets.imdb ",
    name="imdb ",
    outputs=[
        {"name": "x_train"},
        {"name": "y_train"},
        {"name": "x_test"},
        {"name": "y_test"},
    ],
)
def _imdb(
    num_words: Optional[int] = None,
    skip_top: int = 0,
    maxlen: Optional[int] = None,
    seed: int = 113,
    start_char: int = 1,
    oov_char: int = 2,
    index_from: int = 3,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    (x_train, y_train), (x_test, y_test) = imdb.load_data(
        num_words=num_words,
        skip_top=skip_top,
        maxlen=maxlen,
        seed=seed,
        start_char=start_char,
        oov_char=oov_char,
        index_from=index_from,
    )
    return x_train, y_train, x_test, y_test


@NodeDecorator(
    node_id="tensorflow.keras.datasets.reuters ",
    name="reuters ",
    outputs=[
        {"name": "x_train"},
        {"name": "y_train"},
        {"name": "x_test"},
        {"name": "y_test"},
    ],
)
def _reuters(
    num_words: Optional[int] = None,
    skip_top: int = 0,
    maxlen: Optional[int] = None,
    test_split: float = 0.2,
    seed: int = 113,
    start_char: int = 1,
    oov_char: int = 2,
    index_from: int = 3,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if not 0 <= test_split < 1:
        raise ValueError("test_split must be between 0 and 1")
    (x_train, y_train), (x_test, y_test) = reuters.load_data(
        num_words=num_words,
        skip_top=skip_top,
        maxlen=maxlen,
        test_split=test_split,
        seed=seed,
        start_char=start_char,
        oov_char=oov_char,
        index_from=index_from,
    )
    return x_train, y_train, x_test, y_test


@NodeDecorator(
    node_id="tensorflow.keras.datasets.fashion_mnist ",
    name="fashion_mnist ",
    outputs=[
        {"name": "x_train"},
        {"name": "y_train"},
        {"name": "x_test"},
        {"name": "y_test"},
    ],
)
def _fashion_mnist() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
    return x_train, y_train, x_test, y_test


class VersionMode(Enum):
    small = "small"
    large = "large"

    @classmethod
    def default(cls):
        return cls.small.value


@NodeDecorator(
    node_id="tensorflow.keras.datasets.california_housing ",
    name="california_housing ",
    outputs=[
        {"name": "x_train"},
        {"name": "y_train"},
        {"name": "x_test"},
        {"name": "y_test"},
    ],
)
def _california_housing(
    version: VersionMode = VersionMode.default(),
    test_split: float = 0.2,
    seed: int = 113,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if isinstance(version, VersionMode):
        version = version.value
    if not 0 <= test_split < 1:
        raise ValueError("test_split must be between 0 and 1")
    (x_train, y_train), (x_test, y_test) = california_housing.load_data(
        version=version, test_split=test_split, seed=seed
    )
    return x_train, y_train, x_test, y_test


DATASETS_NODE_SHELFE = Shelf(
    nodes=[
        _mnist,
        _cifar10,
        _cifar100,
        _imdb,
        _reuters,
        _fashion_mnist,
        _california_housing,
    ],
    subshelves=[],
    name="Datasets",
    description="The keras.datasets module provide a few toy datasets (already-vectorized, in Numpy format) that can be used for debugging a model or creating simple code examples.",
)
