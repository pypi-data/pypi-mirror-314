from datetime import datetime
from typing import List
from loguru import logger
from optrabot.broker.order import Leg, OptionRight, Order, OrderAction, OrderType
from optrabot.optionhelper import OptionHelper
from optrabot.signaldata import SignalData
from optrabot.tradetemplate.processor.templateprocessorbase import TemplateProcessorBase
from optrabot.tradetemplate.templatefactory import PutSpread, Template
from optrabot.trademanager import ManagedTrade


class PutSpreadProcessor(TemplateProcessorBase):
	
	def __init__(self, template: Template):
		"""
		Initializes the put spread processor with the given template
		"""
		super().__init__(template)

	def composeEntryOrder(self, signalData: SignalData = None):
		"""
		Composes the entry order for the put spread template
		"""
		super().composeEntryOrder(signalData)
		putSpreadTemplate :PutSpread = self._template
		shortStrike = None
		# Short Strike Determination
		if signalData and signalData.strike > 0:
			shortStrike = signalData.strike
		else:
			shortStrikeData = putSpreadTemplate.getShortStrikeData()
			if not shortStrikeData:
				raise ValueError('Configuration for Short Strike is missing in template!')
			if shortStrikeData.offset:
				logger.debug(f'Using Short Strike Offset: {shortStrikeData.offset}')
				shortStrike =  OptionHelper.roundToStrikePrice(signalData.close + shortStrikeData.offset)
		
		if shortStrike == None:
			raise ValueError('Short Strike could not be determined!')
			
		logger.debug(f'Using Short Strike: {shortStrike}')

		# Long Strike Determination
		longStrikeData = putSpreadTemplate.getLongStrikeData()
		if not longStrikeData:
			raise ValueError('Configuration for Long Strike is missing in template!')
		
		longStrike = OptionHelper.roundToStrikePrice(shortStrike - longStrikeData.width)
		logger.debug(f'Using Long Strike: {longStrike}')

		# Now create the entry order with its legs as all required strikes are determined
		legs: List[Leg] = []
		legs.append(Leg(action=OrderAction.SELL, strike=shortStrike, symbol=self._template.symbol, right=OptionRight.PUT, expiration=datetime.today(), quantity=1))
		legs.append(Leg(action=OrderAction.BUY, strike=longStrike, symbol=self._template.symbol, right=OptionRight.PUT, expiration=datetime.today(), quantity=1))
		
		entryOrder = Order(symbol=self._template.symbol, legs=legs, action=OrderAction.BUY_TO_OPEN, quantity=self._template.amount, type=OrderType.LIMIT)
		return entryOrder
	
	def composeTakeProfitOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the take profit order based on the template and the given fill price
		"""
		super().composeTakeProfitOrder(managedTrade, fillPrice)
		logger.debug('Creating take profit order for template {}', self._template.name)
		takeProfitPrice = self._template.calculateTakeProfitPrice(fillPrice)
		logger.debug(f'Calculated take profit price: {takeProfitPrice}')

		takeProfitOrder = Order(symbol=self._template.symbol, legs=managedTrade.entryOrder.legs, action=OrderAction.SELL_TO_CLOSE, quantity=self._template.amount, type=OrderType.LIMIT, price=takeProfitPrice)
		return takeProfitOrder
	
	def composeStopLossOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the stop loss order based on the template and the given fill price
		"""
		super().composeStopLossOrder(managedTrade, fillPrice)
		logger.debug('Creating stop loss order for template {}', self._template.name)
		stopLossPrice = self._template.calculateStopLossPrice(fillPrice)
		logger.debug(f'Calculated stop loss price: {stopLossPrice}')
		
		stopLossOrder = Order(symbol=self._template.symbol, legs=managedTrade.entryOrder.legs, action=OrderAction.SELL_TO_CLOSE, quantity=self._template.amount, type=OrderType.STOP, price=stopLossPrice)
		return stopLossOrder