from typing import Optional
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from tensorflow.keras.optimizers import (
    Optimizer,
    SGD,
    RMSprop,
    Adam,
    AdamW,
    Adadelta,
    Adagrad,
    Adamax,
    Adafactor,
    Nadam,
    Ftrl,
    Lion,
)


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.SGD",
    name="SGD",
)
@controlled_wrapper(SGD, wrapper_attribute="__fnwrapped__")
def _SGD(
    learning_rate: float = 0.01,
    momentum: float = 0.0,
    nesterov: bool = False,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return SGD(
        learning_rate=learning_rate,
        momentum=momentum,
        nesterov=nesterov,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.RMSprop",
    name="RMSprop",
)
@controlled_wrapper(RMSprop, wrapper_attribute="__fnwrapped__")
def _RMSprop(
    learning_rate: float = 0.001,
    rho: float = 0.9,
    momentum: float = 0.0,
    epsilon: float = 1e-07,
    centered: bool = False,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return RMSprop(
        learning_rate=learning_rate,
        momentum=momentum,
        rho=rho,
        epsilon=epsilon,
        centered=centered,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Adam",
    name="Adam",
)
@controlled_wrapper(Adam, wrapper_attribute="__fnwrapped__")
def _Adam(
    learning_rate: float = 0.001,
    beta_1: float = 0.9,
    beta_2: float = 0.999,
    epsilon: float = 1e-07,
    amsgrad: bool = False,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Adam(
        learning_rate=learning_rate,
        beta_1=beta_1,
        beta_2=beta_2,
        epsilon=epsilon,
        amsgrad=amsgrad,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.AdamW",
    name="AdamW",
)
@controlled_wrapper(AdamW, wrapper_attribute="__fnwrapped__")
def _AdamW(
    learning_rate: float = 0.001,
    weight_decay: float = 0.004,
    beta_1: float = 0.9,
    beta_2: float = 0.999,
    epsilon: float = 1e-07,
    amsgrad: bool = False,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return AdamW(
        learning_rate=learning_rate,
        beta_1=beta_1,
        beta_2=beta_2,
        epsilon=epsilon,
        amsgrad=amsgrad,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Adadelta",
    name="Adadelta",
)
@controlled_wrapper(Adadelta, wrapper_attribute="__fnwrapped__")
def _Adadelta(
    learning_rate: float = 0.001,
    rho: float = 0.95,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Adadelta(
        learning_rate=learning_rate,
        rho=rho,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Adagrad",
    name="Adagrad",
)
@controlled_wrapper(Adagrad, wrapper_attribute="__fnwrapped__")
def _Adagrad(
    learning_rate: float = 0.001,
    initial_accumulator_value: float = 0.1,
    epsilon: float = 1e-07,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Adagrad(
        learning_rate=learning_rate,
        initial_accumulator_value=initial_accumulator_value,
        epsilon=epsilon,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Adamax",
    name="Adamax",
)
@controlled_wrapper(Adamax, wrapper_attribute="__fnwrapped__")
def _Adamax(
    learning_rate: float = 0.001,
    beta_1: float = 0.9,
    beta_2: float = 0.999,
    epsilon: float = 1e-07,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Adamax(
        learning_rate=learning_rate,
        beta_1=beta_1,
        beta_2=beta_2,
        epsilon=epsilon,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Adafactor",
    name="Adafactor",
)
@controlled_wrapper(Adafactor, wrapper_attribute="__fnwrapped__")
def _Adafactor(
    learning_rate: float = 0.001,
    beta_2_decay: float = -0.8,
    epsilon_1: float = 1e-30,
    epsilon_2: float = 0.001,
    clip_threshold: float = 1.0,
    relative_step: bool = True,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Adafactor(
        learning_rate=learning_rate,
        beta_2_decay=beta_2_decay,
        epsilon_1=epsilon_1,
        epsilon_2=epsilon_2,
        clip_threshold=clip_threshold,
        relative_step=relative_step,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Nadam",
    name="Nadam",
)
@controlled_wrapper(Nadam, wrapper_attribute="__fnwrapped__")
def _Nadam(
    learning_rate: float = 0.001,
    beta_1: float = 0.9,
    beta_2: float = 0.999,
    epsilon: float = 1e-07,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Nadam(
        learning_rate=learning_rate,
        beta_1=beta_1,
        beta_2=beta_2,
        epsilon=epsilon,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Ftrl",
    name="Ftrl",
)
@controlled_wrapper(Ftrl, wrapper_attribute="__fnwrapped__")
def _Ftrl(
    learning_rate: float = 0.001,
    learning_rate_power: float = -0.5,
    initial_accumulator_value: float = 0.1,
    l1_regularization_strength: float = 0.0,
    l2_regularization_strength: float = 0.0,
    l2_shrinkage_regularization_strength: float = 0.0,
    beta: float = 0.0,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Ftrl(
        learning_rate=learning_rate,
        learning_rate_power=learning_rate_power,
        initial_accumulator_value=initial_accumulator_value,
        l1_regularization_strength=l1_regularization_strength,
        l2_regularization_strength=l2_regularization_strength,
        l2_shrinkage_regularization_strength=l2_shrinkage_regularization_strength,
        beta=beta,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


@NodeDecorator(
    node_id="tensorflow.keras.optimizers.Lion",
    name="Lion",
)
@controlled_wrapper(Lion, wrapper_attribute="__fnwrapped__")
def _Lion(
    learning_rate: float = 0.001,
    beta_1: float = 0.9,
    beta_2: float = 0.999,
    weight_decay: Optional[float] = None,
    clipnorm: Optional[float] = None,
    clipvalue: Optional[float] = None,
    global_clipnorm: Optional[float] = None,
    use_ema: bool = False,
    ema_momentum: float = 0.99,
    ema_overwrite_frequency: Optional[int] = None,
    loss_scale_factor: Optional[float] = None,
    gradient_accumulation_steps: Optional[int] = None,
) -> Optimizer:
    return Lion(
        learning_rate=learning_rate,
        beta_1=beta_1,
        beta_2=beta_2,
        weight_decay=weight_decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue,
        global_clipnorm=global_clipnorm,
        use_ema=use_ema,
        ema_momentum=ema_momentum,
        ema_overwrite_frequency=ema_overwrite_frequency,
        loss_scale_factor=loss_scale_factor,
        gradient_accumulation_steps=gradient_accumulation_steps,
    )


OPTIMIZERS_NODE_SHELFE = Shelf(
    nodes=[
        _SGD,
        _RMSprop,
        _Adagrad,
        _Adadelta,
        _Adam,
        _Adamax,
        _Nadam,
        _Ftrl,
        _Lion,
    ],
    subshelves=[],
    name="Optimizers",
    description="An optimizer is one of the two arguments required for compiling a Keras model:",
)
