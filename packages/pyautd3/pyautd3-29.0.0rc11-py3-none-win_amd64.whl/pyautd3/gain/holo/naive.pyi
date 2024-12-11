import ctypes
from collections.abc import Iterable
from typing import Self
import numpy as np
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.gain.holo.backend import Backend
from pyautd3.gain.holo.constraint import EmissionConstraint
from pyautd3.gain.holo.holo import HoloWithBackend
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3
from pyautd3.gain.cache import Cache
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment



class Naive(HoloWithBackend[Naive]):
    def __init__(self: Naive, backend: Backend, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None: ...
    def _gain_ptr(self: Naive, _: Geometry) -> GainPtr: ...
    def with_cache(self: Naive, ) -> Cache[Naive]: ...
    def with_timeout(self: Naive, timeout: Duration | None) -> DatagramWithTimeout[Naive]: ...
    def with_parallel_threshold(self: Naive, threshold: int | None) -> DatagramWithParallelThreshold[Naive]: ...
    def with_segment(self: Naive, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Naive]: ...
