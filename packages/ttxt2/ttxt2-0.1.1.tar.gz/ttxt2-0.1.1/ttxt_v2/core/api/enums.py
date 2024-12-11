from enum import Enum


class ESide(str, Enum):
    """
    Enumeration for the side of a trade.

    This enum represents the side of a trade, either 'BUY' or 'SELL'.
    It inherits from `str` and `Enum` to allow for string comparison.
    """

    BUY = ("BUY",)
    SELL = "SELL"


class EUpdateType(str, Enum):
    """
    Enumeration for the type of update.

    This enum represents the type of update, either 'SNAPSHOT' or 'DELTA'.
    It inherits from `str` and `Enum` to allow for string comparison.
    """

    SNAPSHOT = ("SNAPSHOT",)
    DELTA = "DELTA"


class EOrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    UNKNOWN = "UNKNOWN"


class EventType(Enum):
    """
    Enumeration for the type of event.

    This enum represents different types of events, such as 'ORDERBOOK',
    'MARKET_TRADES', and 'KLINES'.
    """

    CONNECTOR_STATUS_EVENT = "CONNECTOR_STATUS"
    OB_EVENT = "ORDERBOOK"
    MT_EVENT = "MARKET_TRADES"
    KL_EVENT = "KLINES"
    ORDER_UPDATE_EVENT = "ORDER_UPDATE"
    CREATE_ORDER_EVENT = "CREATE_ORDER"
    AMEND_ORDER_EVENT = "AMEND_ORDER"
    CANCEL_ORDER_EVENT = "CANCEL_ORDER"
    CANCEL_ALL_ORDERS_EVENT = "CANCEL_ALL_ORDERS"
    WALLET_UPDATE_EVENT = "WALLET_UPDATE"
    ORDER_ACK_EVENT = "ORDER_ACK"
    POSITION_UPDATE_EVENT = "POSITION_UPDATE"


class ETimeInForce(Enum):
    """
    Enumeration for different time-in-force policies for orders.

    Attributes:
        GTC (str): Good Till Cancelled - The order remains active until it is explicitly cancelled.
        IOC (str): Immediate Or Cancel - The order must be executed immediately, and any portion that cannot be filled is cancelled.
        FOK (str): Fill Or Kill - The order must be filled entirely immediately, or it is cancelled.
    """

    GTC = "GOOD_TILL_CANCELLED"
    IOC = "IMMEDIATE_OR_CANCEL"
    FOK = "FILL_OR_KILL"
    UNKNOWN = "UNKNOWN"


class KlineTime(str, Enum):
    """
    Enumeration for Kline time intervals.

    Attributes:
        ONE_MIN (str): 1 minute interval.
        FIVE_MIN (str): 5 minute interval.
        FIFTEEN_MIN (str): 15 minute interval.
        THIRTY_MIN (str): 30 minute interval.
    """

    ONE_MIN = "1"
    FIVE_MIN = "5"
    FIFTEEN_MIN = "15"
    THIRTY_MIN = "30"
    ONE_HOUR = "1h"
    FOUR_HOUR = "4h"
    ONE_DAY = "1d"


class EOrderCategory(Enum):
    SPOT = "SPOT"
    LINEAR = "LINEAR"
    INVERSE = "INVERSE"
    UNKNOWN = "UNKNOWN"


class EAckType(Enum):
    CREATE = "CREATE"
    CANCEL = "CANCEL"
    UNKNOWN = "UNKNOWN"


class EOrderStatus(Enum):
    """
    Enumeration for different statuses of an order.

    Attributes:
        NEW (str): The order has been created but not yet processed.
        PARTIALLY_FILLED (str): The order has been partially filled.
        FILLED (str): The order has been completely filled.
        CANCELLED (str): The order has been cancelled.
        REJECTED (str): The order has been rejected.
    """

    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class EConnectorStatus(Enum):
    DISCONNECTED = "DISCONNECTED"
    RECONNECTING = "RECONNECTING"
    CONNECTED = "CONNECTED"


class EWebSocketType(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    TRADE = "TRADE"


class EAccountType(Enum):
    SPOT = "SPOT"
    UNIFIED = "UNIFIED"
    CONTRACT = "CONTRACT"
