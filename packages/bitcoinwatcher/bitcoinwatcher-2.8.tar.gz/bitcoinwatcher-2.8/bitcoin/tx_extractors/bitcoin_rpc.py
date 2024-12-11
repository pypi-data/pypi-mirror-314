import os
from multiprocessing.pool import ThreadPool

from bitcoinlib.transactions import Transaction

from bitcoin.address_listener.address_listener import AddressTxData
from bitcoin.models.address_tx_data import AddressTxType
from bitcoin.utils.bitcoin_rpc import BitcoinRPC
from bitcoin.tx_extractors.abstract_extractor import AbstractTxAddressDataExtractor
from bitcoin.utils.context_aware_logging import logger, ctx_tx_status


class BitcoinRPCAddressDataExtractor(AbstractTxAddressDataExtractor):
    bitcoinrpc: BitcoinRPC
    thread_pool = ThreadPool(processes=os.environ.get("THREAD_POOL_SIZE", 5))

    def __init__(self):
        self.bitcoinrpc = BitcoinRPC()

    def fetch_all_inputs(self, inputs):
        rpc_calls = [["getrawtransaction", input.prev_txid.hex(), True] for input in inputs]
        data = self.bitcoinrpc.rpc_connection.batch_(rpc_calls)
        list_of_vouts = []
        for input in inputs:
            vout = data.pop(0)["vout"][input.output_n_int]
            list_of_vouts.append(vout)
        return list_of_vouts

    def get_address_tx_from_inputdata(self, tx_id, tx_status, input_data):
        address = input_data["scriptPubKey"]["address"]
        amount = int(input_data.get("value", 0).real * 100000000)
        return AddressTxData(tx_id=tx_id, is_confirmed=tx_status, address=address, _amount=amount,
                             type=AddressTxType.INPUT)

    def extract(self, tx: Transaction) -> [AddressTxData]:
        logger.info("Extracting rpc tx data")
        outputs = tx.outputs
        tx_id = tx.txid
        address_tx_data = []
        inputs = tx.inputs
        # bulk get all the inputs from BitcoinRPC using thread pool
        inputs_data = self.fetch_all_inputs(inputs)
        is_confirmed = self.bitcoinrpc.is_confirmed(tx_id)
        ctx_tx_status.set(is_confirmed)
        logger.info("Transaction is_confirmed: %s", is_confirmed)
        for input in inputs:
            address = input.address
            amount = 0
            if len(inputs_data) > 0:
                input_data = inputs_data.pop(0)
                input_tx_data = self.get_address_tx_from_inputdata(tx_id, is_confirmed, input_data)
                address_tx_data.append(input_tx_data)
            else:
                address_tx_data.append(AddressTxData(is_confirmed=is_confirmed,
                                                     address=address,
                                                     type=AddressTxType.INPUT,
                                                     _amount=amount,
                                                     tx_id=tx.txid))
        for output in outputs:
            amount = output.value
            address_tx_data.append(AddressTxData(is_confirmed=is_confirmed,
                                                 address=output.address,
                                                 _amount=amount,
                                                 type=AddressTxType.OUTPUT,
                                                 tx_id=tx.txid))
        return address_tx_data
