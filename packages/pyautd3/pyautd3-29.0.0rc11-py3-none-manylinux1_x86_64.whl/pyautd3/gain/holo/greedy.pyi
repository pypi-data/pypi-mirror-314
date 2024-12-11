import ctypes
from collections.abc import Iterable
from typing import Self
import numpy as np
from pyautd3.derive import builder
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.gain.holo.constraint import EmissionConstraint
from pyautd3.gain.holo.holo import Holo
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo
from pyautd3.native_methods.structs import Vector3
from pyautd3.gain.cache import Cache
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment



class Greedy(Holo[Greedy]):
    def __init__(self: Greedy, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None: ...
    def _gain_ptr(self: Greedy, _: Geometry) -> GainPtr: ...
    def with_phase_div(self: Greedy, phase_div: int) -> Greedy: ...
    def with_cache(self: Greedy, ) -> Cache[Greedy]: ...
    def with_timeout(self: Greedy, timeout: Duration | None) -> DatagramWithTimeout[Greedy]: ...
    def with_parallel_threshold(self: Greedy, threshold: int | None) -> DatagramWithParallelThreshold[Greedy]: ...
    def with_segment(self: Greedy, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Greedy]: ...
    @property
    def phase_div(self: Greedy) -> int: ...
