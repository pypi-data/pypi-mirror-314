from typing import Self
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class Clear(Datagram):
    def __init__(self: Clear, ) -> None: ...
    def _datagram_ptr(self: Clear, _: Geometry) -> DatagramPtr: ...
    def with_timeout(self: Clear, timeout: Duration | None) -> DatagramWithTimeout[Clear]: ...
    def with_parallel_threshold(self: Clear, threshold: int | None) -> DatagramWithParallelThreshold[Clear]: ...
