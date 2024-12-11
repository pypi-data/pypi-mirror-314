from typing import OrderedDict
from loguru import logger
#from optrabot.tradetemplate.putspread import PutSpread
#from optrabot.tradetemplate.template import Template, TemplateType
from optrabot.optionhelper import OptionHelper
from optrabot.stoplossadjuster import StopLossAdjuster
from optrabot.tradetemplate.templatedata import LongStrikeData, ShortStrikeData
from optrabot.tradetemplate.templatetrigger import TemplateTrigger

class TemplateType:
	IronFly = "Iron Fly"
	PutSpread = "Put Spread"

class Template:
	def __init__(self, name: str) -> None:
		self._type = None
		self.name = name
		self._trigger = None
		self.account = None
		self.takeProfit = None
		self.stopLoss = None
		self.amount = 1
		self.minPremium = None
		self.adjustmentStep = 0.05
		self.stopLossAdjuster = None
		self.strategy = ''
		self.wing = None
		self.symbol = 'SPX'
		self.maxOpenTrades = 0

	def getType(self) -> str:
		""" Returns the type of the template
		"""
		return self._type

	def setTrigger(self, trigger: TemplateTrigger):
		""" Defines the trigger for this template
		"""
		self._trigger = trigger

	def getTrigger(self) -> TemplateTrigger:
		""" Returns the trigger of the template
		"""
		return self._trigger
	
	def setAccount(self, account: str):
		""" Sets the account which the template is traded on 
		"""
		self.account = account
	
	def setTakeProfit(self, takeprofit: int):
		""" Sets the take profit level in % of the template
		"""
		self.takeProfit = takeprofit

	def setStopLoss(self, stoploss: int):
		""" Sets the stop loss level in % of the template
		"""
		self.stopLoss = stoploss

	def setAmount(self, amount: int):
		""" Sets the amount of contracts to be traded with this template
		"""
		self.amount = amount
	
	def setMinPremium(self, minPremium: float):
		""" Sets the minimum premium which must be received from broker in order to execute a trade
		of this template.
		"""
		self.minPremium = minPremium

	def setAdjustmentStep(self, adjustmentStep: float):
		""" Sets the price adjustment step size for the entry order adjustment
		"""
		self.adjustmentStep = adjustmentStep
	
	def setStopLossAdjuster(self, stopLossAdjuster: StopLossAdjuster):
		""" Sets the Stop Loss Adjuster for this strategy, if configured
		"""
		self.stopLossAdjuster = stopLossAdjuster
	
	def setStrategy(self, strategy: str):
		""" Sets the strategy name of this template
		"""
		self.strategy = strategy
	
	def setWing(self, wing: int):
		""" Set the wing size for Iron Fly strategies
		"""
		self.wing = wing
	
	def resetStopLossAdjuster(self):
		"""
		Resets the Stop Loss Adjuster if there is one defined
		"""
		if self.stopLossAdjuster:
			self.stopLossAdjuster.resetTrigger()

	def toDict(self):
		""" Returns a dictionary representation of the Template which is used for
		the config file.
		"""
		returnDict = {'type': self._type, 'strategy': self.strategy, 'adjustmentstep': self.adjustmentStep, 'wing': self.wing,
				'account': self.account, 'takeprofit': self.takeProfit, 'stoploss': self.stopLoss, 'amount': self.amount,
				'minpremium': self.minPremium}
		returnDict.update({'trigger':self._trigger.toDict()})
		if self.stopLossAdjuster:
			returnDict.update({'adjuststop':self.stopLossAdjuster.toDict()})
		return returnDict
	
	def setShortStikeData(self, shortStrikeData: ShortStrikeData):
		"""
		This is just a dummy method which is implemented in the derived classes
		"""
		raise NotImplementedError('Method setShortStikeData not implemented in this class')
	
	def setLongStikeData(self, longStrikeData: LongStrikeData):
		"""
		This is just a dummy method which is implemented in the derived classes
		"""
		raise NotImplementedError('Method setLongStikeData not implemented in this class')
	
	def setMaxOpenTrades(self, maxOpenTrades: int):
		""" Sets the maximum number of open trades for this template
		"""
		self.maxOpenTrades = maxOpenTrades

	def __str__(self) -> str:
		""" Returns a string representation of the strategy
		"""
		templateString = ('Name: ' + self.name + ' Type: ' + self._type + ' Trigger: (' + self._trigger.type + ', ' + str(self._trigger.value) + ')' +
		' Account: ' + self.account + ' Amount: ' + str(self.amount) + ' Take Profit (%): ' + str(self.takeProfit) + ' Stop Loss (%): ' + str(self.stopLoss) +
		' Min. Premium: ' + str(self.minPremium) + ' Entry Adjustment Step: ' + str(self.adjustmentStep) + ' Wing size: ' + str(self.wing) + ' Stop Loss Adjuster: ()' + 
		str(self.stopLossAdjuster) + ')')
		return templateString
	
	def meetsMinimumPremium(self, premium: float) -> bool:
		""" Returns True if the given premium meets the minimum premium requirement
		"""
		if self.minPremium == None:
			return True
		if premium > (self.minPremium * -1):
			return False
		return True
	
	def calculateTakeProfitPrice(self, fillPrice: float) -> float:
		""" Calculates the take profit price based on the fill price of the entry order
		"""
		logger.debug('Calculating take profit price for fill price {} and take profit {}%', fillPrice, self.takeProfit)
		return OptionHelper.roundToTickSize(fillPrice + (abs(fillPrice) * (self.takeProfit / 100)))
	
	def calculateStopLossPrice(self, fillPrice: float) -> float:
		""" Calculates the stop loss price based on the fill price of the entry order
		"""
		logger.debug('Calculating stop loss price for fill price {} and stop loss {}%', fillPrice, self.stopLoss)
		return OptionHelper.roundToTickSize(fillPrice - (abs(fillPrice) * (self.stopLoss / 100)))
	
	def hasTakeProfit(self) -> bool:
		""" Returns True if the template has a take profit defined
		"""
		return self.takeProfit != None

class PutSpread(Template):
	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self._type = TemplateType.PutSpread
		self._shortStrikeData = None
		self._longStrikeData = None

	def setShortStikeData(self, shortStrikeData: ShortStrikeData):
		self._shortStrikeData = shortStrikeData

	def setLongStikeData(self, longStrikeData: LongStrikeData):
		self._longStrikeData = longStrikeData

	def getShortStrikeData(self) -> ShortStrikeData:
		return self._shortStrikeData
	
	def getLongStrikeData(self) -> LongStrikeData:
		return self._longStrikeData

class IronFly(Template):
	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self._type = TemplateType.IronFly

class TemplateFactory:

	@staticmethod
	def createTemplate(name: str, data) -> Template:
		""" Creates a template object from the given template configuration of config.yaml
		"""
		template = None
		templateType = data['type']
		match templateType:
			case TemplateType.IronFly:
				logger.debug('Creating Iron Fly template from config')
				template = IronFly(name)
			case TemplateType.PutSpread:
				logger.debug('Creating Put Spread template from config')
				template = PutSpread(name)
			case _:
				logger.error('Template type {} is unknown!', templateType)
				return None

		# Strategy
		try:
			strategy = data['strategy']
			template.setStrategy(strategy)
		except KeyError:
			pass

		# Max Open Trades
		try:
			maxOpenTrades = data['maxopentrades']
			template.setMaxOpenTrades(maxOpenTrades)
		except KeyError:
			pass

		# Trigger configuration
		try:
			triggerinfo = data['trigger']
			trigger = TemplateTrigger(triggerinfo)
			template.setTrigger(trigger)
		except KeyError:
			pass

		try:
			account = data['account']
			template.setAccount(account)
		except KeyError:
			pass

		try:
			takeProfit = data['takeprofit']
			template.setTakeProfit(takeProfit)
		except KeyError:
			pass

		try:
			stopLoss = data['stoploss']
			template.setStopLoss(stopLoss)
		except KeyError:
			pass

		try:
			amount = data['amount']
			template.setAmount(amount)
		except KeyError:
			pass

		try:
			minPremium = data['minpremium']
			template.setMinPremium(minPremium)
		except KeyError:
			pass

		try:
			adjustmentStep = data['adjustmentstep']
			template.setAdjustmentStep(adjustmentStep)
		except KeyError:
			pass

		try:
			wing = data['wing']
			template.setWing(wing)
		except KeyError:
			pass

		# Short Strike
		try:
			shortstrikeConfig = data['shortstrike']
			shortStrikeData = ShortStrikeData()
			try:
				shortStrikeData.offset = shortstrikeConfig['offset']
				# Set the short strike data in the template if supported
				try:
					template.setShortStikeData(shortStrikeData)
				except AttributeError:
					pass
			except KeyError:
				pass
		except KeyError:
			pass

		# Long Strike
		try:
			longstrikeConfig = data['longstrike']
			if longstrikeConfig:
				longStrikeData = LongStrikeData()
				try:
					longStrikeData.width = longstrikeConfig['width']
					# Set the long strike data in the template if supported
					try:
						template.setLongStikeData(longStrikeData)
					except AttributeError:
						pass
				except KeyError:
					pass
		except KeyError:
			pass

		# Stop Loss Adjuster
		try:
			stoplossadjustment = OrderedDict(data['adjuststop'])
		except KeyError as keyErr:
			stoplossadjustment = None
			pass

		if stoplossadjustment:
			try:
				trigger = stoplossadjustment['trigger']
				stop = stoplossadjustment['stop']
				offset = float(stoplossadjustment['offset'])
				adjuster = StopLossAdjuster(reverse=True, trigger=trigger, stop=stop, offset=offset)
				template.setStopLossAdjuster(adjuster)
			except KeyError:
				pass

		return template
			
