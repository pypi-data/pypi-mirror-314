from loguru import logger
from optrabot.broker.order import Order
from optrabot.config import Config
import optrabot.config as optrabotcfg
from optrabot.signaldata import SignalData
from optrabot.tradetemplate.templatefactory import Template
from optrabot.trademanager import ManagedTrade
#from optrabot.tradetemplate.template import Template

"""
Base class for all template processors
"""
class TemplateProcessorBase:

	def __init__(self, template: Template):
		"""
		Initializes the template processor with the given template
		"""
		self._template = template
		self._config: Config = optrabotcfg.appConfig

	def composeEntryOrder(self, signalData: SignalData = None) -> Order:
		"""
		Composes the entry order based on the template and the optional signal data
		"""
		logger.debug('Creating entry order for template {}', self._template.name)

	def composeTakeProfitOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the take profit order based on the template and the given fill price
		"""
		logger.debug('Creating take profit order for trade {}', managedTrade.trade.id)

	def composeStopLossOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the stop loss order based on the template and the given fill price
		"""
		logger.debug('Creating stop loss order for trade {}', managedTrade.trade.id)

	def hasTakeProfit(self) -> bool:
		"""
		Returns True if the template has a take profit defined
		"""
		return self._template.hasTakeProfit()
