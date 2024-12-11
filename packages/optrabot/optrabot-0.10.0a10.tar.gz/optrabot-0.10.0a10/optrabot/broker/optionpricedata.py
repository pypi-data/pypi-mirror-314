from typing import Dict


class OptionStrikePriceData:
	def __init__(self) -> None:
		self.callBid: float = None
		self.callAsk: float = None
		self.callDelta: float = None
		self.putBid: float = None
		self.putAsk: float = None
		self.putDelta: float = None

	def getPutMidPrice(self) -> float:
		"""
		Returns the mid price of the put option
		"""
		if self.putBid == None:
			bidPrice = 0
		else:
			bidPrice = self.putBid
		
		if self.putAsk == None:
			askPrice = 0
		else:
			askPrice = self.putAsk
		return (bidPrice + askPrice) / 2
	
	def getCallMidPrice(self) -> float:
		"""
		Returns the mid price of the call option
		"""
		if self.callBid == None:
			bidPrice = 0
		else:
			bidPrice = self.callBid
		
		if self.callAsk == None:
			askPrice = 0
		else:
			askPrice = self.callAsk
		return (bidPrice + askPrice) / 2

class OptionStrikeData:
	def __init__(self) -> None:
		pass
		self.strikeData: Dict[float, OptionStrikePriceData] = {}