from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import GainCachePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment

G = TypeVar("G", bound=Gain)

class Cache(Gain, Generic[G]):
    _g: G
    _ptr: GainCachePtr | None
    def __init__(self: Cache[G], g: G) -> None: ...
    def _gain_ptr(self: Cache[G], geometry: Geometry) -> GainPtr: ...
    def __del__(self: Cache[G], ) -> None: ...
    def with_timeout(self: Cache[G], timeout: Duration | None) -> DatagramWithTimeout[Cache[G]]: ...
    def with_parallel_threshold(self: Cache[G], threshold: int | None) -> DatagramWithParallelThreshold[Cache[G]]: ...
    def with_segment(self: Cache[G], segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Cache[G]]: ...
