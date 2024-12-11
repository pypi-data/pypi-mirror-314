from unittest import TestCase

from bitcoinlib.transactions import Transaction

from bitcoin.tests.data.transactions import batch_airdrop_tx_hex, tx_hex, non_reveal_tx_hex, tx_hex_2
from bitcoin.utils.bitcoin_utils import is_reveal_tx, count_reveal_inputs


class Test(TestCase):
    def test_is_reveal_tx(self):
        tx = Transaction.parse_hex(tx_hex, strict=False)
        self.assertTrue(is_reveal_tx(tx))

    def test_tx_hex_deserialization(self):
        tx=Transaction.parse_hex(tx_hex_2, strict=False)
        self.assertEqual(tx.txid, "8ca9bdedffbdf7c763dc41ec313f337b92c033530a546cb9cb2be5f486c9573a")

    def test_is_reveal_tx_in_second_input(self):
        tx = Transaction.parse_hex(batch_airdrop_tx_hex, strict=False)
        self.assertTrue(is_reveal_tx(tx))

    def test_is_not_reveal_tx(self):
        tx = Transaction.parse_hex(non_reveal_tx_hex, strict=False)
        self.assertFalse(is_reveal_tx(tx))

    def test_count_reveal_inputs(self):
        tx = Transaction.parse_hex(tx_hex, strict=False)
        self.assertEqual(count_reveal_inputs(tx), 1)

    def test_count_reveal_inputs_not_reveal(self):
        tx = Transaction.parse_hex(non_reveal_tx_hex, strict=False)
        self.assertEqual(count_reveal_inputs(tx), 0)

    def test_count_reveal_in_airdrop_tx(self):
        tx = Transaction.parse_hex(batch_airdrop_tx_hex, strict=False)
        self.assertEqual(count_reveal_inputs(tx), 1420)
