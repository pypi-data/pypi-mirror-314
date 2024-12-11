import dataclasses
from enum import Enum


class AddressTxType(Enum):
    INPUT = "input"
    OUTPUT = "output"


class AddressTxSource(Enum):
    MEMPOOL = "mempool"
    DEFAULT = "default"


class TransactionStatus(Enum):
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"


@dataclasses.dataclass
class AddressTxData:
    tx_id: str
    address: str
    type: AddressTxType
    # figure out the way to get amount in vin
    _amount: int = 0
    is_confirmed: bool = False
    is_reveal_tx: bool = False

    def get_amount(self):
        return self._amount

    def amount_in_btc(self):
        if self.type == AddressTxType.INPUT:
            return "Amount is not supported for input type, yet"
        return self._amount / 100000000
