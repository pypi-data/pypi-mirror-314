from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import datagram
from pyautd3.derive import modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.modulation.cache import Cache
from pyautd3.modulation.fir import Fir
from collections.abc import Iterable
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment

M = TypeVar("M", bound=Modulation)

class RadiationPressure(Modulation, Generic[M]):
    _m: M
    def __init__(self: RadiationPressure[M], m: M) -> None: ...
    def _modulation_ptr(self: RadiationPressure[M], ) -> ModulationPtr: ...
    def with_cache(self: RadiationPressure[M], ) -> Cache[RadiationPressure[M]]: ...
    def with_fir(self: RadiationPressure[M], iterable: Iterable[float]) -> Fir[RadiationPressure[M]]: ...
    def with_timeout(self: RadiationPressure[M], timeout: Duration | None) -> DatagramWithTimeout[RadiationPressure[M]]: ...
    def with_parallel_threshold(self: RadiationPressure[M], threshold: int | None) -> DatagramWithParallelThreshold[RadiationPressure[M]]: ...
    def with_segment(self: RadiationPressure[M], segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[RadiationPressure[M]]: ...
