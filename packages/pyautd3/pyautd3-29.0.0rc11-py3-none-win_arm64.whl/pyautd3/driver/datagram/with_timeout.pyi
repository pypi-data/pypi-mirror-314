from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.utils import Duration
from pyautd3.utils import into_option_duration
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

D = TypeVar("D", bound="Datagram")

class DatagramWithTimeout(Datagram, Generic[D]):
    _datagram: D
    _timeout: Duration | None
    def __init__(self: DatagramWithTimeout[D], datagram: D, timeout: Duration | None) -> None: ...
    def _datagram_ptr(self: DatagramWithTimeout[D], g: Geometry) -> DatagramPtr: ...
    def with_parallel_threshold(self: DatagramWithTimeout[D], threshold: int | None) -> DatagramWithParallelThreshold[DatagramWithTimeout[D]]: ...
