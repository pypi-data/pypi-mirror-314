import ctypes
from collections.abc import Callable
from typing import Self
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Device
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import GeometryPtr
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class ReadsFPGAState(Datagram):
    def __init__(self: ReadsFPGAState, f: Callable[[Device], bool]) -> None: ...
    def _datagram_ptr(self: ReadsFPGAState, geometry: Geometry) -> DatagramPtr: ...
    def with_timeout(self: ReadsFPGAState, timeout: Duration | None) -> DatagramWithTimeout[ReadsFPGAState]: ...
    def with_parallel_threshold(self: ReadsFPGAState, threshold: int | None) -> DatagramWithParallelThreshold[ReadsFPGAState]: ...
