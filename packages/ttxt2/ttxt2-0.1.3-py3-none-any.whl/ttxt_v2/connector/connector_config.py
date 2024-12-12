from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import List, Optional

from ttxt_v2.core.api import KlineTime, TradingPair


@dataclass
class OrderbookStreamConfig:
    """
    Configuration for the order book stream.

    Attributes:
        tickers (List[str]): List of ticker symbols to subscribe to.
        depth (int): Depth of the order book to fetch. Default is 50.
    """

    tickers: List[TradingPair]
    depth: int = 50
    on: bool = True


@dataclass
class MarketTradeStreamConfig:
    """
    Configuration for the market trade stream.

    Attributes:
        tickers (List[str]): List of ticker symbols to subscribe to.
    """

    tickers: List[TradingPair]
    on: bool = True


@dataclass
class KLineStreamConfig:
    """
    Configuration for the Kline stream.

    Attributes:
        tickers (List[str]): List of ticker symbols to subscribe to.
        timeframe (KlineTime): Timeframe for the Kline data. Default is 1 minute.
    """

    tickers: List[TradingPair]
    timeframes: List[KlineTime] = field(default_factory=lambda: [KlineTime.ONE_MIN])
    on: bool = True


class StorageType(StrEnum):
    NONE = "none"
    LOCAL = "local"


@dataclass
class StorageConfig:
    enable: bool = False
    storage_type: Optional[StorageType] = None


class OperationMode(Enum):
    SPOT = 0
    FUTURES = 1


class TradingMode(StrEnum):
    NONE = "None"
    TRADE = "trade"
    TEST = "test"


@dataclass
class ConnectorConfig:
    """
    Configuration for the connector.

    Attributes:
        exchange (str): Name of the exchange.
        ob_config (Optional[OrderbookStreamConfig]): Configuration for the order book stream.
        mt_config (Optional[MarketTradeStreamConfig]): Configuration for the market trade stream.
        kl_config (Optional[KLineStreamConfig]): Configuration for the Kline stream.
    """

    exchange: str
    trading_mode: TradingMode
    recording_config: StorageConfig
    ob_config: OrderbookStreamConfig
    mt_config: MarketTradeStreamConfig
    kl_config: KLineStreamConfig
    operation_mode: OperationMode = OperationMode.SPOT
