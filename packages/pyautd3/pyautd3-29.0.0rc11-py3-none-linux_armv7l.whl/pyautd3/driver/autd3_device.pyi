from typing import Self
import numpy as np
from numpy.typing import ArrayLike
import pyautd3.native_methods.autd3capi_driver as consts
from pyautd3.derive import builder



class AUTD3():
    TRANS_SPACING: float
    DEVICE_WIDTH: float
    DEVICE_HEIGHT: float
    NUM_TRANS_IN_X: int
    NUM_TRANS_IN_Y: int
    NUM_TRANS_IN_UNIT: int
    def __init__(self: AUTD3, pos: ArrayLike) -> None: ...
    def with_rotation(self: AUTD3, rotation: np.ndarray) -> AUTD3: ...
    @property
    def position(self: AUTD3) -> np.ndarray: ...
    @property
    def rotation(self: AUTD3) -> np.ndarray: ...
