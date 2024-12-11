from collections.abc import Callable
from ctypes import POINTER
from ctypes import c_int32
from ctypes import c_uint16
from typing import Generic
from typing import Self
from typing import TypeVar
import numpy as np
from pyautd3.autd_error import UnknownGroupKeyError
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Device
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry import Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.utils import _validate_ptr
from pyautd3.gain.cache import Cache
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment

K = TypeVar("K")

class Group(Gain, Generic[K]):
    _map: dict[K, Gain]
    _f: Callable[[Device], Callable[[Transducer], K | None]]
    def __init__(self: Group[K], f: Callable[[Device], Callable[[Transducer], K | None]]) -> None: ...
    def set(self: Group[K], key: K, gain: Gain) -> Group[K]: ...
    def _gain_ptr(self: Group[K], geometry: Geometry) -> GainPtr: ...
    def with_cache(self: Group[K], ) -> Cache[Group[K]]: ...
    def with_timeout(self: Group[K], timeout: Duration | None) -> DatagramWithTimeout[Group[K]]: ...
    def with_parallel_threshold(self: Group[K], threshold: int | None) -> DatagramWithParallelThreshold[Group[K]]: ...
    def with_segment(self: Group[K], segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Group[K]]: ...
