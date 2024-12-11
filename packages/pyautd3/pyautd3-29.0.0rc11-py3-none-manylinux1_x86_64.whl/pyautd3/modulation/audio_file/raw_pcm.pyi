from pathlib import Path
from typing import Self
from pyautd3.derive import datagram
from pyautd3.derive import modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from pyautd3.native_methods.utils import _to_null_terminated_utf8
from pyautd3.native_methods.utils import _validate_ptr
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



class RawPCM(Modulation):
    _path: Path
    _config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]
    _sample_rate: Freq[int]
    def __private_init__(self: RawPCM, path: Path, config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]) -> None: ...
    def __init__(self: RawPCM, path: Path, config: SamplingConfig | Freq[int] | Freq[float] | Duration) -> None: ...
    def _modulation_ptr(self: RawPCM, ) -> ModulationPtr: ...
    def with_cache(self: RawPCM, ) -> Cache[RawPCM]: ...
    def with_fir(self: RawPCM, iterable: Iterable[float]) -> Fir[RawPCM]: ...
    def with_radiation_pressure(self: RawPCM, ) -> RadiationPressure[RawPCM]: ...
    def with_timeout(self: RawPCM, timeout: Duration | None) -> DatagramWithTimeout[RawPCM]: ...
    def with_parallel_threshold(self: RawPCM, threshold: int | None) -> DatagramWithParallelThreshold[RawPCM]: ...
    def with_segment(self: RawPCM, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[RawPCM]: ...
    @staticmethod
    def new_with_resample(path: Path, source: Freq[float], target: SamplingConfig | Freq[int] | Freq[float] | Duration, resampler: Resampler) -> RawPCM: ...
