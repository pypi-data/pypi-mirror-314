import logging
from contextvars import ContextVar
from datetime import datetime

import pytz

logger = logging.getLogger(__name__)
root = logging.getLogger()
root.setLevel(logging.INFO)

class TimezoneFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, tz=None):
        super().__init__(fmt, datefmt)
        self.tz = tz

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.tz)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.isoformat()
        return s  # Adding blue color to the date

formatter = TimezoneFormatter(
    ' %(asctime)s %(levelname)s txid= %(tx_id)s tx_status=%(tx_status)s [%(module)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    tz=pytz.timezone('Asia/Kolkata'),
)


ctx_tx = ContextVar('tx_id', default='')
ctx_tx_status = ContextVar('tx_status', default='')

class ExcludeModuleFilter(logging.Filter):
    def filter(self, record):
        return not (record.name.startswith('bitcoinlib.transactions') or record.name.startswith('bitcoinlib.scripts'))

class TXContextFilter(logging.Filter):

    def __init__(self):
        super().__init__()

    def filter(self, record):
        tx_id = ctx_tx.get()
        record.tx_id = tx_id
        tx_status = ctx_tx_status.get()
        record.tx_status = tx_status
        return True

ch = logging.StreamHandler()
f = TXContextFilter()
ch.setFormatter(formatter)
ch.addFilter(f)
ch.addFilter(ExcludeModuleFilter())
root.addHandler(ch)

def get_logger(name):
    return logging.getLogger(name)