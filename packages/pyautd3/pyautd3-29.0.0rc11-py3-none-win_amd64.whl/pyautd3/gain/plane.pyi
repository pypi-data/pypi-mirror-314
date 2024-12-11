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



class Plane(Gain):
    def __init__(self: Plane, direction: ArrayLike) -> None: ...
    def _gain_ptr(self: Plane, _: Geometry) -> GainPtr: ...
    def with_intensity(self: Plane, intensity: int | EmitIntensity) -> Plane: ...
    def with_phase_offset(self: Plane, phase_offset: int | Phase) -> Plane: ...
    def with_cache(self: Plane, ) -> Cache[Plane]: ...
    def with_timeout(self: Plane, timeout: Duration | None) -> DatagramWithTimeout[Plane]: ...
    def with_parallel_threshold(self: Plane, threshold: int | None) -> DatagramWithParallelThreshold[Plane]: ...
    def with_segment(self: Plane, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Plane]: ...
    @property
    def dir(self: Plane) -> np.ndarray: ...
    @property
    def intensity(self: Plane) -> EmitIntensity: ...
    @property
    def phase_offset(self: Plane) -> Phase: ...
