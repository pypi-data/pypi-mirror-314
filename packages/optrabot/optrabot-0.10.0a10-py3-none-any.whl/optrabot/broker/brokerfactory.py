import asyncio
from eventkit import Event
from optrabot.broker.order import Order, OrderStatus
from optrabot import crud, schemas
from optrabot.broker.brokerconnector import BrokerConnector
from optrabot.broker.ibtwsconnector import IBTWSTConnector
from optrabot.broker.tastytradeconnector import TastytradeConnector
from optrabot.database import get_db_engine
import optrabot.config as optrabotcfg
from optrabot.models import Account
from optrabot.util.singletonmeta import SingletonMeta
from sqlalchemy.orm import Session
from loguru import logger
from typing import Dict, List

class BrokerFactory(metaclass=SingletonMeta):
	def __init__(self):
		self._connectors: Dict[str, BrokerConnector] = {}
		self.orderStatusEvent = Event('orderStatusEvent')

	async def createBrokerConnectors(self):
		""" Creates broker connections from the given configuration
		"""
		twsConnector = IBTWSTConnector()
		if twsConnector.isInitialized():
			self._connectors[twsConnector.id] = twsConnector
		tastyConnector = TastytradeConnector()
		if tastyConnector.isInitialized():
			self._connectors[tastyConnector.id] = tastyConnector
		
		for value in self._connectors.values():
			connector : BrokerConnector = value
			connector.connectedEvent += self._onBrokerConnected
			connector.disconnectedEvent += self._onBrokerDisconnected
			connector.connectFailedEvent += self._onBrokerConnectFailed
			connector.orderStatusEvent += self._onOrderStatus
			await connector.connect()

	def getBrokerConnectorByAccount(self, account: str) -> BrokerConnector:
		""" Returns the broker connector for the given account
		"""
		for value in self._connectors.values():
			connector : BrokerConnector = value
			accounts = connector.getAccounts()
			for acc in accounts:
				if acc.id == account:
					return connector
		return None

	async def _onBrokerConnected(self, brokerConnector: BrokerConnector):
		""" 
		Called when a broker connection has been established
		the BrokerConnector object is passed as parameter
		"""
		logger.info('Broker {} connected successfully.', brokerConnector.id)
		accounts = brokerConnector.getAccounts()
		self._updateAccountsInDatabase(accounts)
		self._checkTradeTemplateAccounts(brokerConnector.broker, accounts)
		
		symbols = ['SPX', 'VIX']
		await brokerConnector.requestTickerData(symbols)

	def _onBrokerDisconnected(self, brokerConnector):
		""" 
		Called when a broker connection has been disconnected
		the BrokerConnector object is passed as parameter
		"""
		logger.warning('Broker {} disconnected, attempting to reconnect in 30 seconds ...', brokerConnector.id)
		asyncio.create_task(self._reconnect_broker_task(brokerConnector))

	def _onOrderStatus(self, order: Order, status: OrderStatus, filledAmount: int = 0):
		""" 
		Called when an order status has changed
		"""
		self.orderStatusEvent.emit(order, status, filledAmount)

	def _onBrokerConnectFailed(self, brokerConnector):
		""" 
		Called when a broker connection has failed to connect
		"""
		logger.error('Failed to connect to broker {}, attempting to reconnect in 30 seconds ...', brokerConnector.id)
		asyncio.create_task(self._reconnect_broker_task(brokerConnector))

	async def _reconnect_broker_task(self, brokerConnector: BrokerConnector):
		"""
		Asynchronous task to reconnect a broker after a disconnect
		"""
		await asyncio.sleep(30)
		await brokerConnector.connect()

	def _updateAccountsInDatabase(self, accounts: List[Account]):
		"""
		Updates the account information in the database if required
		"""
		with Session(get_db_engine()) as session:
			for account in accounts:
				logger.debug('Managed Account at {}: {}', account.broker, account.id)
				known_account = crud.get_account(session, account.id)
				if known_account == None:
					logger.debug('Account is new. Adding it to the Database')
					new_account = schemas.AccountCreate( id = account.id, name = account.name, broker = account.broker, pdt = account.pdt)
					crud.create_account(session, new_account)
					logger.debug('Account {} created in database.', account.id)
				else:
					if account.name != known_account.name or account.pdt != known_account.pdt:
						logger.debug('Account {} has changed. Updating it in the database.', account.id)
						known_account.name = account.name
						known_account.pdt = account.pdt
						crud.update_account(session, known_account)
	
	def _checkTradeTemplateAccounts(self, broker: str, accounts: List[Account]):
		"""
		Checks if the accounts configured in the trade template are available in the broker connection
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		tradeTemplates = config.getTemplates()	
		for template in tradeTemplates:
			if template.account:
				if template.account.startswith('U') or template.account.startswith('DU') and broker == 'IBKR':
					accountFound = False
					for account in accounts:
						if account.id == template.account:
							accountFound = True
							break
					if not accountFound:
						logger.error(f'Account {template.account} configured in Trade Template {template.name} is not available in Broker {broker}')


	def shutdownBrokerConnectors(self):
		""" Shuts down all broker connections
		"""
		for value in self._connectors.values():
			connector : BrokerConnector = value
			connector.disconnectedEvent -= self._onBrokerDisconnected
			connector.connectFailedEvent -= self._onBrokerConnectFailed
			connector.connectedEvent -= self._onBrokerConnected
			connector.orderStatusEvent -= self._onOrderStatus
			if connector.isConnected():
				connector.disconnect()
		
