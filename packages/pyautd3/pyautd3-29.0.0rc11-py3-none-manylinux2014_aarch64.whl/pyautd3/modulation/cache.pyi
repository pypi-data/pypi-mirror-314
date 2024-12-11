from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import datagram
from pyautd3.derive import modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.native_methods.autd3capi import ModulationCachePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.modulation.fir import Fir
from collections.abc import Iterable
from pyautd3.modulation.radiation_pressure import RadiationPressure
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment

M = TypeVar("M", bound=Modulation)

class Cache(Modulation, Generic[M]):
    _m: M
    _ptr: ModulationCachePtr | None
    def __init__(self: Cache[M], m: M) -> None: ...
    def _modulation_ptr(self: Cache[M], ) -> ModulationPtr: ...
    def __del__(self: Cache[M], ) -> None: ...
    def with_fir(self: Cache[M], iterable: Iterable[float]) -> Fir[Cache[M]]: ...
    def with_radiation_pressure(self: Cache[M], ) -> RadiationPressure[Cache[M]]: ...
    def with_timeout(self: Cache[M], timeout: Duration | None) -> DatagramWithTimeout[Cache[M]]: ...
    def with_parallel_threshold(self: Cache[M], threshold: int | None) -> DatagramWithParallelThreshold[Cache[M]]: ...
    def with_segment(self: Cache[M], segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Cache[M]]: ...
