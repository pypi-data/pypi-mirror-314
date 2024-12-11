from loguru import logger


class OptionHelper:

	@staticmethod
	def roundToTickSize(value: float) -> float:
		""" Round a calculated options price e.g. a mid price to the closest tick value
		"""
		roundBase = 5
		return (roundBase * round(value*100/roundBase)) / 100

	@staticmethod
	def roundToStrikePrice(value: float) -> float:
		""" Round a floating value to the nearest Strike price 
		"""
		roundBase = 5
		return (roundBase * round(value/roundBase))
	
	@staticmethod
	def checkContractIsQualified(contract):
		if contract.conId == 0:
			logger.error("Contract not determined. Strike {}, Right {}", contract.strike, contract.right)
			return False
		else:
			return True
	
	@staticmethod
	def calculateMidPrice(bidPrice: float, askPrice: float) -> float:
		difference = abs(bidPrice-askPrice)
		half = difference / 2
		if bidPrice < askPrice:
			midPrice = bidPrice + half
		else:
			midPrice = bidPrice - half
		return OptionHelper.roundToTickSize(midPrice)