from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import Segment
from pyautd3.native_methods.autd3capi_driver import TransitionModeWrap
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

DS = TypeVar("DS", bound="DatagramS")
P = TypeVar("P")

class DatagramS(Generic[P]):
    def _into_segment(self: DatagramS[P], ptr: P, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr: ...
    def _raw_ptr(self: DatagramS[P], geometry: Geometry) -> P: ...

class DatagramWithSegment(Datagram, Generic[DS]):
    _datagram: DS
    _segment: Segment
    _transition_mode: TransitionModeWrap | None
    def __init__(self: DatagramWithSegment[DS], datagram: DS, segment: Segment, transition_mode: TransitionModeWrap | None) -> None: ...
    def _datagram_ptr(self: DatagramWithSegment[DS], g: Geometry) -> DatagramPtr: ...
    def with_timeout(self: DatagramWithSegment[DS], timeout: Duration | None) -> DatagramWithTimeout[DatagramWithSegment[DS]]: ...
    def with_parallel_threshold(self: DatagramWithSegment[DS], threshold: int | None) -> DatagramWithParallelThreshold[DatagramWithSegment[DS]]: ...
