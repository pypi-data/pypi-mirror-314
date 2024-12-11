from typing import Self
from pyautd3.derive import datagram
from pyautd3.derive import modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.modulation.cache import Cache
from pyautd3.modulation.fir import Fir
from collections.abc import Iterable
from pyautd3.modulation.radiation_pressure import RadiationPressure
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment



class Static(Modulation):
    _intensity: int
    def __init__(self: Static, intensity: int | None = None) -> None: ...
    def _modulation_ptr(self: Static, ) -> ModulationPtr: ...
    def with_cache(self: Static, ) -> Cache[Static]: ...
    def with_fir(self: Static, iterable: Iterable[float]) -> Fir[Static]: ...
    def with_radiation_pressure(self: Static, ) -> RadiationPressure[Static]: ...
    def with_timeout(self: Static, timeout: Duration | None) -> DatagramWithTimeout[Static]: ...
    def with_parallel_threshold(self: Static, threshold: int | None) -> DatagramWithParallelThreshold[Static]: ...
    def with_segment(self: Static, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Static]: ...
    @staticmethod
    def with_intensity(intensity: int) -> Static: ...
    @property
    def intensity(self: Static) -> int: ...
