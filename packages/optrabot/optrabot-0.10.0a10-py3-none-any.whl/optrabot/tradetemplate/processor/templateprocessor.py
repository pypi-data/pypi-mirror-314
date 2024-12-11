from datetime import datetime
from typing import List

from loguru import logger
from optrabot.broker.brokerfactory import BrokerFactory
import optrabot.config as optrabotcfg
from optrabot.signaldata import SignalData
from optrabot.trademanager import TradeManager
from optrabot.tradetemplate.processor.ironflyprocessor import IronFlyProcessor
from optrabot.tradetemplate.processor.putspreadprocessor import PutSpreadProcessor
from optrabot.tradetemplate.processor.templateprocessorbase import TemplateProcessorBase
from optrabot.tradetemplate.templatefactory import Template, TemplateType
from optrabot.tradetemplate.templatetrigger import TriggerType
from optrabot.util.singletonmeta import SingletonMeta

class TemplateProcessor(metaclass=SingletonMeta):
	def __init__(self):
		pass

	async def processTemplate(self, template: Template, signalData: SignalData = None):
		"""
		Processes the signal and generates the appropriate orders
		"""
		logger.debug('Processing triggered template {}', template.name)
		
		if signalData.timestamp == None or self._isSignalOutdated(signalData.timestamp):
			logger.warning('Signal is outdated already or Signal timestamp is invalid!')
			return
		
		templateTrigger = template.getTrigger()
		if templateTrigger.type == TriggerType.External:
			if templateTrigger.fromTimeUTC != None:
				today = datetime.today().date()
				fromDateTimeUTC = datetime.combine(today, templateTrigger.fromTimeUTC.time())
				signalDateTimeUTC = datetime.combine(today, signalData.timestamp.time())
				deltaInSeconds = (signalDateTimeUTC - fromDateTimeUTC).total_seconds()
				if deltaInSeconds <= 0:
					logger.info('Signal time is before "from time" of the template. Ignoring signal.')
					return
				
			if templateTrigger.toTimeUTC != None:
				today = datetime.today().date()
				toDateTimeUTC = datetime.combine(today, templateTrigger.toTimeUTC.time())
				signalDateTimeUTC = datetime.combine(today, signalData.timestamp.time())
				deltaInSeconds = (signalDateTimeUTC - toDateTimeUTC).total_seconds()
				if deltaInSeconds >= 0:
					logger.info('Signal time is after "to time" of the template. Ignoring signal.')
					return
				
			if templateTrigger.excludeFromTimeUTC != None and templateTrigger.excludeToTimeUTC != None:
				today = datetime.today().date()
				excludeFromDateTimeUTC = datetime.combine(today, templateTrigger.excludeFromTimeUTC.time())
				excludeToDateTimeUTC = datetime.combine(today, templateTrigger.excludeToTimeUTC.time())
				signalDateTimeUTC = datetime.combine(today, signalData.timestamp.time())
				deltaFromInSeconds = (signalDateTimeUTC - excludeFromDateTimeUTC).total_seconds()
				deltaToInSeconds = (signalDateTimeUTC - excludeToDateTimeUTC).total_seconds()
				if deltaFromInSeconds >= 0 and deltaToInSeconds <= 0:
					logger.info('Signal time is excluded the template. Ignoring signal.')
					return

		try:
			templateProcessor = self.createTemplateProcessor(template)
		except ValueError as e:
			logger.error('Error creating a Template Processor: {}', e)
			return
		
		try:
			entryOrder = templateProcessor.composeEntryOrder(signalData)
		except ValueError as e:
			logger.error('Error creating entry order: {}', e)
			return

		await TradeManager().openTrade(entryOrder, template)

	def createTemplateProcessor(self, template: Template) -> TemplateProcessorBase:
		"""
		Creates a new template processor for the given template
		"""
		match template.getType():
			case TemplateType.PutSpread:
				return PutSpreadProcessor(template)
			case TemplateType.IronFly:
				return IronFlyProcessor(template)
			case _:
				raise ValueError('Unsupported template type: {}'.format(template.getType()))

	def determineTemplate(self, signalStrategy: str) -> Template:
		"""
		Determines the template to use for the given external signal strategy
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		for template in config.getTemplates():
			trigger = template.getTrigger()
			if trigger.type == TriggerType.External and trigger.value == signalStrategy:
				return template
	
	def _isSignalOutdated(self, signalTimeStamp: datetime):
		""" Checks if the time stamp of the signal is older than 10 minutes which means it's outdated.
		
		Parameters
		----------
		signalTimeStamp : datetime
    		Timestamp of the signal.

		Returns
		-------
		bool
			Returns True, if the signal is outdated
		"""
		if datetime == None:
			return True
		currentTime = datetime.now().astimezone()
		timeDelta = currentTime - signalTimeStamp
		if (timeDelta.total_seconds() / 60) > 10:
			return True
		return False
				