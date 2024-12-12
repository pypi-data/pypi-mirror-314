import funcnodes as fn
from .applications import APPLICATION_NODE_SHELFE
from .fit import FIT_NODE_SHELFE
from .datasets import DATASETS_NODE_SHELFE
from .metrics import METRICS_NODE_SHELFE
from .optimizers import OPTIMIZERS_NODE_SHELFE
from .losses import LOSSES_NODE_SHELFE
from .layers import LAYERS_NODE_SHELFE
from .models import MODELS_NODE_SHELFE
from .utilities import UTILS_NODE_SHELFE

__version__ = "0.1.12"

NODE_SHELF = fn.Shelf(
    name="Keras",
    description="Tensorflow-Keras for funcnodes",
    nodes=[],
    subshelves=[
        LAYERS_NODE_SHELFE,
        MODELS_NODE_SHELFE,
        FIT_NODE_SHELFE,
        OPTIMIZERS_NODE_SHELFE,
        METRICS_NODE_SHELFE,
        LOSSES_NODE_SHELFE,
        UTILS_NODE_SHELFE,
        DATASETS_NODE_SHELFE,
        APPLICATION_NODE_SHELFE,
    ],
)
