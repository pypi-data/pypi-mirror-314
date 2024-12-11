import ctypes
from collections.abc import Iterable
from typing import Generic
from typing import Self
from typing import TypeVar
import numpy as np
from pyautd3.derive import datagram
from pyautd3.derive import modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.modulation.cache import Cache
from pyautd3.modulation.radiation_pressure import RadiationPressure
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment

M = TypeVar("M", bound=Modulation)

class Fir(Modulation, Generic[M]):
    _m: M
    _coef: np.ndarray
    def __init__(self: Fir[M], m: M, iterable: Iterable[float]) -> None: ...
    def _modulation_ptr(self: Fir[M], ) -> ModulationPtr: ...
    def with_cache(self: Fir[M], ) -> Cache[Fir[M]]: ...
    def with_radiation_pressure(self: Fir[M], ) -> RadiationPressure[Fir[M]]: ...
    def with_timeout(self: Fir[M], timeout: Duration | None) -> DatagramWithTimeout[Fir[M]]: ...
    def with_parallel_threshold(self: Fir[M], threshold: int | None) -> DatagramWithParallelThreshold[Fir[M]]: ...
    def with_segment(self: Fir[M], segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Fir[M]]: ...
