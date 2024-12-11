from .loader import get_market_data
from .backtester import BackTester
from .strategy import *
from TradeTide import indicators


try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"

# -
