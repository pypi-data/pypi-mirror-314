from typing import Self
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.gain.cache import Cache
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment



class Null(Gain):
    def __init__(self: Null, ) -> None: ...
    def _gain_ptr(self: Null, _: Geometry) -> GainPtr: ...
    def with_cache(self: Null, ) -> Cache[Null]: ...
    def with_timeout(self: Null, timeout: Duration | None) -> DatagramWithTimeout[Null]: ...
    def with_parallel_threshold(self: Null, threshold: int | None) -> DatagramWithParallelThreshold[Null]: ...
    def with_segment(self: Null, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Null]: ...
