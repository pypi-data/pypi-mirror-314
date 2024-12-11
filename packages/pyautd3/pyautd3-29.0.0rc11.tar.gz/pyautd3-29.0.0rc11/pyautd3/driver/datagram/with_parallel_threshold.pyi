from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout

D = TypeVar("D", bound="Datagram")

class DatagramWithParallelThreshold(Datagram, Generic[D]):
    _datagram: D
    _threshold: int | None
    def __init__(self: DatagramWithParallelThreshold[D], datagram: D, threshold: int | None) -> None: ...
    def _datagram_ptr(self: DatagramWithParallelThreshold[D], g: Geometry) -> DatagramPtr: ...
    def with_timeout(self: DatagramWithParallelThreshold[D], timeout: Duration | None) -> DatagramWithTimeout[DatagramWithParallelThreshold[D]]: ...
