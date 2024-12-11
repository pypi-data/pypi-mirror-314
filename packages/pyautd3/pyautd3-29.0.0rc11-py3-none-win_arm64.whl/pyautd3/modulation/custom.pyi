import ctypes
from collections.abc import Iterable
from typing import Self
import numpy as np
from pyautd3.derive import datagram
from pyautd3.derive import modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.utils import Duration
from pyautd3.modulation.cache import Cache
from pyautd3.modulation.fir import Fir
from collections.abc import Iterable
from pyautd3.modulation.radiation_pressure import RadiationPressure
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment



class Custom(Modulation):
    _buf: np.ndarray
    _config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]
    def __init__(self: Custom, buf: Iterable[int], config: SamplingConfig | Freq[int] | Freq[float] | Duration) -> None: ...
    def _modulation_ptr(self: Custom, ) -> ModulationPtr: ...
    def with_cache(self: Custom, ) -> Cache[Custom]: ...
    def with_fir(self: Custom, iterable: Iterable[float]) -> Fir[Custom]: ...
    def with_radiation_pressure(self: Custom, ) -> RadiationPressure[Custom]: ...
    def with_timeout(self: Custom, timeout: Duration | None) -> DatagramWithTimeout[Custom]: ...
    def with_parallel_threshold(self: Custom, threshold: int | None) -> DatagramWithParallelThreshold[Custom]: ...
    def with_segment(self: Custom, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Custom]: ...
    @staticmethod
    def new_with_resample(buf: Iterable[int], source: Freq[float], target: SamplingConfig | Freq[int] | Freq[float] | Duration, resampler: Resampler) -> Custom: ...
