import dataclasses

from mach_client import Chain, Token
from mach_client.client.event import Trade, TradeError, TransactionError
from mach_client.client.types import GasResponse

from .destination_policy import DestinationPolicy


@dataclasses.dataclass(frozen=True, slots=True)
class NoViableDestination:
    destination_policy: DestinationPolicy


@dataclasses.dataclass(frozen=True, slots=True)
class GasEstimateFailed:
    chain: Chain
    exception: Exception


@dataclasses.dataclass(frozen=True, slots=True)
class InsufficientDestinationGas:
    destination: Token
    gas_estimate: GasResponse
    gas_available: int


TestError = (
    TradeError
    | TransactionError
    | NoViableDestination
    | GasEstimateFailed
    | InsufficientDestinationGas
)

TestEvent = Trade | TestError
