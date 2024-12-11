from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import builder
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.datagram.silencer.fixed_completion_time import FixedCompletionTime
from pyautd3.driver.datagram.silencer.fixed_update_rate import FixedUpdateRate
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import SilencerTarget
from pyautd3.utils import Duration
from pyautd3.utils import Duration
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

T = TypeVar("T", FixedCompletionTime, FixedUpdateRate)

class Silencer(Datagram, Generic[T]):
    _inner: T
    _strict_mode: bool
    def __init__(self: Silencer[T], config: T | None = None) -> None: ...
    def with_strict_mode(self: Silencer[T], mode: bool) -> Silencer[T]: ...
    def is_valid(self: Silencer[T], target: Modulation | FociSTM | GainSTM) -> bool: ...
    def _datagram_ptr(self: Silencer[T], _: Geometry) -> DatagramPtr: ...
    def with_target(self: Silencer[T], target: SilencerTarget) -> Silencer[T]: ...
    def with_timeout(self: Silencer[T], timeout: Duration | None) -> DatagramWithTimeout[Silencer[T]]: ...
    def with_parallel_threshold(self: Silencer[T], threshold: int | None) -> DatagramWithParallelThreshold[Silencer[T]]: ...
    @staticmethod
    def disable() -> Silencer[FixedCompletionTime]: ...
    @property
    def target(self: Silencer[T]) -> SilencerTarget: ...
