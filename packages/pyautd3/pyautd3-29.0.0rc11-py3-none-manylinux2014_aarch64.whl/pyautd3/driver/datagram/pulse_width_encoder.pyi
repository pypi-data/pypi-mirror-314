from collections.abc import Callable
from ctypes import CFUNCTYPE
from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_void_p
from threading import Lock
from typing import Self
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry.device import Device
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import GeometryPtr
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class PulseWidthEncoder(Datagram):
    _cache: dict[int, Callable[[int], int]]
    _lock: Lock
    def __init__(self: PulseWidthEncoder, f: Callable[[Device], Callable[[int], int]] | None = None) -> None: ...
    def _datagram_ptr(self: PulseWidthEncoder, geometry: Geometry) -> DatagramPtr: ...
    def with_timeout(self: PulseWidthEncoder, timeout: Duration | None) -> DatagramWithTimeout[PulseWidthEncoder]: ...
    def with_parallel_threshold(self: PulseWidthEncoder, threshold: int | None) -> DatagramWithParallelThreshold[PulseWidthEncoder]: ...
