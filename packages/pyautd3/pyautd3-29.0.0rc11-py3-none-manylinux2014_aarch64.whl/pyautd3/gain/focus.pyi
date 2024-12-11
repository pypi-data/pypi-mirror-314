from typing import Self
import numpy as np
from numpy.typing import ArrayLike
from pyautd3.derive import builder
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3
from pyautd3.gain.cache import Cache
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment



class Focus(Gain):
    def __init__(self: Focus, pos: ArrayLike) -> None: ...
    def _gain_ptr(self: Focus, _: Geometry) -> GainPtr: ...
    def with_intensity(self: Focus, intensity: int | EmitIntensity) -> Focus: ...
    def with_phase_offset(self: Focus, phase_offset: int | Phase) -> Focus: ...
    def with_cache(self: Focus, ) -> Cache[Focus]: ...
    def with_timeout(self: Focus, timeout: Duration | None) -> DatagramWithTimeout[Focus]: ...
    def with_parallel_threshold(self: Focus, threshold: int | None) -> DatagramWithParallelThreshold[Focus]: ...
    def with_segment(self: Focus, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Focus]: ...
    @property
    def pos(self: Focus) -> np.ndarray: ...
    @property
    def intensity(self: Focus) -> EmitIntensity: ...
    @property
    def phase_offset(self: Focus) -> Phase: ...
