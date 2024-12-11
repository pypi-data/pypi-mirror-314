from datetime import datetime
from enum import Enum
from typing import Optional

class OrderAction(str, Enum):
    """
    Represents actions of an order or order le
    """

    BUY_TO_OPEN = "Buy to Open"
    BUY_TO_CLOSE = "Buy to Close"
    SELL_TO_OPEN = "Sell to Open"
    SELL_TO_CLOSE = "Sell to Close"
    BUY = "Buy"
    SELL = "Sell"

class OrderType(str, Enum):
	"""
	Represents order types
	"""
	LIMIT = "Limit"
	MARKET = "Market"
	STOP = "Stop"
	STOP_LIMIT = "Stop Limit"

class OrderStatus(str, Enum):
	"""
	Represents the status of an order
	"""
	OPEN = "Open"
	FILLED = "Filled"
	CANCELLED = "Cancelled"

class OptionRight(str, Enum):
	"""
	Represents the right of an option
	"""
	CALL = "Call"
	PUT = "Put"

class Leg():
	"""
	Represents a leg of an order.
	"""
	action: OrderAction
	quantity: Optional[int]
	symbol: str
	strike: float
	right: OptionRight
	expiration: datetime
	askPrice: float = None
	bidPrice: float = None
	midPrice: float = None
	brokerSpecific = {}
     
	def __init__(self, action: OrderAction, symbol: str, quantity: Optional[int] = 0, strike: float = None, right: OptionRight = None, expiration: datetime = None):
		self.action = action
		self.quantity = quantity
		self.symbol = symbol
		self.right = right
		self.strike = strike
		self.expiration = expiration

class Order():
	"""
	Represents an order. A order can have multiple legs
	"""
	
	def __init__(self, symbol: str = '', action: OrderAction = None, type: OrderType = None, legs: list[Leg] = None, quantity: int = 1, price: float = None):
		self.symbol = symbol
		self.action = action
		self.legs: list[Leg] = legs
		self.type = type
		self.quantity = quantity
		self.price: float = price
		self.averageFillPrice: float = None
		self.ocaGroup = None
		self.status: OrderStatus = None
		self.orderReference: str = ''
		self.brokerSpecific = {}