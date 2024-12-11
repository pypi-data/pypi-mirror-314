import ctypes
from collections.abc import Iterable
from typing import Generic
from typing import Self
from typing import TypeVar
import numpy as np
from numpy.typing import ArrayLike
from pyautd3.derive import datagram
from pyautd3.derive.derive_builder import builder
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.stm.control_point import ControlPoints1
from pyautd3.driver.datagram.stm.control_point import ControlPoints2
from pyautd3.driver.datagram.stm.control_point import ControlPoints3
from pyautd3.driver.datagram.stm.control_point import ControlPoints4
from pyautd3.driver.datagram.stm.control_point import ControlPoints5
from pyautd3.driver.datagram.stm.control_point import ControlPoints6
from pyautd3.driver.datagram.stm.control_point import ControlPoints7
from pyautd3.driver.datagram.stm.control_point import ControlPoints8
from pyautd3.driver.datagram.stm.control_point import IControlPoints
from pyautd3.driver.datagram.stm.stm_sampling_config import STMSamplingConfig
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import FociSTMPtr
from pyautd3.native_methods.autd3capi_driver import Segment
from pyautd3.native_methods.autd3capi_driver import TransitionModeWrap
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior
from pyautd3.native_methods.utils import _validate_ptr
from pyautd3.utils import Duration
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment

C = TypeVar("C", bound=IControlPoints)

class FociSTM(DatagramS[FociSTMPtr], Datagram, Generic[C]):
    _points: list[C]
    _stm_sampling_config: STMSamplingConfig
    def __private_init__(self: FociSTM[C], sampling_config: STMSamplingConfig, foci: list[ArrayLike] | list[ControlPoints1] | list[ControlPoints2] | list[ControlPoints3] | list[ControlPoints4] | list[ControlPoints5] | list[ControlPoints6] | list[ControlPoints7] | list[ControlPoints8]) -> None: ...
    def __init__(self: FociSTM, config: SamplingConfig | Freq[float] | Duration, iterable: Iterable[ArrayLike] | Iterable[ControlPoints1] | Iterable[ControlPoints2] | Iterable[ControlPoints3] | Iterable[ControlPoints4] | Iterable[ControlPoints5] | Iterable[ControlPoints6] | Iterable[ControlPoints7] | Iterable[ControlPoints8]) -> None: ...
    def _raw_ptr(self: FociSTM[C], _: Geometry) -> FociSTMPtr: ...
    def _ptr(self: FociSTM[C], ) -> FociSTMPtr: ...
    def _datagram_ptr(self: FociSTM[C], geometry: Geometry) -> DatagramPtr: ...
    def _into_segment(self: FociSTM[C], ptr: FociSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr: ...
    def _sampling_config_intensity(self: FociSTM[C], ) -> SamplingConfig: ...
    def _sampling_config_phase(self: FociSTM[C], ) -> SamplingConfig: ...
    def with_loop_behavior(self: FociSTM[C], loop_behavior: _LoopBehavior) -> FociSTM[C]: ...
    def with_timeout(self: FociSTM[C], timeout: Duration | None) -> DatagramWithTimeout[FociSTM[C]]: ...
    def with_parallel_threshold(self: FociSTM[C], threshold: int | None) -> DatagramWithParallelThreshold[FociSTM[C]]: ...
    def with_segment(self: FociSTM[C], segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[FociSTM[C]]: ...
    @classmethod
    def nearest(cls, config: Freq[float] | Duration, iterable: Iterable[ArrayLike] | Iterable[ControlPoints1] | Iterable[ControlPoints2] | Iterable[ControlPoints3] | Iterable[ControlPoints4] | Iterable[ControlPoints5] | Iterable[ControlPoints6] | Iterable[ControlPoints7] | Iterable[ControlPoints8]) -> FociSTM: ...
    @property
    def freq(self: FociSTM[C]) -> Freq[float]: ...
    @property
    def period(self: FociSTM[C]) -> Duration: ...
    @property
    def sampling_config(self: FociSTM[C]) -> SamplingConfig: ...
    @property
    def loop_behavior(self: FociSTM[C]) -> _LoopBehavior: ...
