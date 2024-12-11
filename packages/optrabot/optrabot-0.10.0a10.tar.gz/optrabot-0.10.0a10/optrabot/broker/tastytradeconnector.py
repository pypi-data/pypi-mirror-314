import asyncio
from dataclasses import dataclass
import datetime as dt
from decimal import Decimal
from typing import Dict, List
from optrabot.optionhelper import OptionHelper
from optrabot.broker.optionpricedata import OptionStrikeData, OptionStrikePriceData
from optrabot.broker.brokerconnector import BrokerConnector
from loguru import logger
from datetime import date, timedelta
import re
from tastytrade import Account, DXLinkStreamer, Session
from optrabot.models import Account as ModelAccount
from tastytrade.instruments import get_option_chain
from tastytrade.utils import TastytradeError
from tastytrade.dxfeed import Greeks, Quote, Candle
from tastytrade.instruments import Option, OptionType
from tastytrade.order import NewOrder, OrderTimeInForce, OrderType
import optrabot.config as optrabotcfg
from optrabot.broker.order import OptionRight, Order as BrokerOrder
from optrabot.tradetemplate.templatefactory import Template
import optrabot.symbolinfo as symbolInfo

# @dataclass
# class TastyLivePrices:
# 	quotes: dict[str, Quote]
# 	greeks: dict[str, Greeks]
# 	streamer: DXLinkStreamer
# 	puts: list[Option]
# 	calls: list[Option]

# 	@classmethod
# 	async def create(cls, session: Session, symbol: str, expiration: date):
# 		chain = get_option_chain(session, symbol)
# 		options = [o for o in chain[expiration]]
# 		# the `streamer_symbol` property is the symbol used by the streamer
# 		streamer_symbols = [o.streamer_symbol for o in options]

# 		streamer = await DXLinkStreamer.create(session)
# 		# subscribe to quotes and greeks for all options on that date
# 		await streamer.subscribe(Quote, [symbol] + streamer_symbols)
# 		await streamer.subscribe(Greeks, streamer_symbols)
# 		puts = [o for o in options if o.option_type == OptionType.PUT]
# 		calls = [o for o in options if o.option_type == OptionType.CALL]
# 		self = cls({}, {}, streamer, puts, calls)

# 		t_listen_greeks = asyncio.create_task(self._update_greeks())
# 		t_listen_quotes = asyncio.create_task(self._update_quotes())
# 		asyncio.gather(t_listen_greeks, t_listen_quotes)

# 		# wait we have quotes and greeks for each option
# 		while len(self.greeks) != len(options) or len(self.quotes) != len(options):
# 			await asyncio.sleep(0.1)

# 		return self
	
# 	async def _update_greeks(self):
# 		async for e in self.streamer.listen(Greeks):
# 			self.greeks[e.eventSymbol] = e

# 	async def _update_quotes(self):
# 		async for e in self.streamer.listen(Quote):
# 			logger.debug(f'Received Quote: {e.eventSymbol} price: {e.askPrice}')
# 			self.quotes[e.eventSymbol] = e

@dataclass
class TastySymbolData:
	def __init__(self) -> None:
		self.symbol: str = None
		self.tastySymbol: str = None
		self.noPriceDataCount: int = 0
		self.optionPriceData: Dict[dt.date, OptionStrikeData] = {}

class TastytradeConnector(BrokerConnector):
	def __init__(self) -> None:
		super().__init__()
		self._username = ''
		self._password = ''
		self._sandbox = False
		self._initialize()
		self.id = 'TASTY'
		self.broker = 'TASTY'
		self._session = None
		self._streamer: DXLinkStreamer
		self._symbolData: Dict[str, TastySymbolData] = {}
		self._symbolReverseLookup: Dict[str, str] = {}		# maps tastytrade symbol to generic symbol

	def _initialize(self):
		"""
		Initialize the Tastytrade connector from the configuration
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		try:
			config.get('tastytrade')
		except KeyError as keyErr:
			logger.debug('No Tastytrade connection configured')
			return
		
		try:
			self._username = config.get('tastytrade.username')
		except KeyError as keyErr:
			logger.error('Tastytrade username not configured')
			return
		try:
			self._password = config.get('tastytrade.password')
		except KeyError as keyErr:
			logger.error('Tastytrade password not configured')
			return
		
		try:
			self._sandbox = config.get('tastytrade.sandbox')
		except KeyError as keyErr:
			pass
		self._initialized = True

	async def connect(self):
		await super().connect()
		try:
			self._session = Session(self._username, self._password, is_test=self._sandbox)
			self._tradingEnabled = True
			self._emitConnectedEvent()
		except TastytradeError as tastyErr:
			logger.error('Failed to connect to Tastytrade: {}', tastyErr)
			self._emitConnectFailedEvent()

	def disconnect(self):
		super().disconnect()
		self._tradingEnabled = False
		if self._session != None:
			self._session.destroy()
			self._session = None
			self._emitDisconnectedEvent()

	def getAccounts(self) -> List[ModelAccount]:
		"""
		Returns the Tastytrade accounts
		"""
		if len(self._managedAccounts) == 0 and self.isConnected():
			for tastyAccount in Account.get_accounts(self._session):
				account = ModelAccount(id = tastyAccount.account_number, name = tastyAccount.nickname, broker = self.broker, pdt = not tastyAccount.day_trader_status)
				self._managedAccounts.append(account)
		return self._managedAccounts
	
	def isConnected(self) -> bool:
		if self._session != None:
			return True
		
	async def prepareOrder(self, order: BrokerOrder) -> bool:
		"""
		Prepares the given order for execution

		It returns True, if the order could be prepared successfully
		"""
		symbolData = self._symbolData[order.symbol]
		for leg in order.legs:
			optionPriceData = symbolData.optionPriceData[leg.expiration.date()]
			try:
				priceData: OptionStrikePriceData = optionPriceData.strikeData[leg.strike]
				if leg.right == OptionRight.CALL:
					leg.askPrice = float(priceData.callAsk)
					if leg.askPrice == None:
						leg.askPrice = 0
					leg.bidPrice = float(priceData.callBid)
					if leg.bidPrice == None:
						leg.bidPrice = 0
				elif leg.right == OptionRight.PUT:
					leg.askPrice = float(priceData.putAsk)
					if leg.askPrice == None:
						leg.askPrice = 0
					leg.bidPrice = float(priceData.putBid)
					if leg.bidPrice == None:
						leg.bidPrice = 0

			except KeyError as keyErr:
				# No data for strike available
				logger.error(f'No option price data for strike {leg.strike} available!')
				return False
			except Exception as excp:
				logger.error(f'Error preparing order: {excp}')
				return False
		return True

	async def placeOrder(self, order: BrokerOrder, template: Template) -> bool:
		""" 
		Places the given order
		"""
		account = Account.get_account(self._session, template.account)

		legs = []

		newOrder = NewOrder(
			time_in_force=OrderTimeInForce.DAY,
			order_type=OrderType.LIMIT,	
			legs=legs,
			price=Decimal(order.price)
		)
		try:
			response = account.place_order(self._session, newOrder, dry_run=True)
		except TastytradeError as tastyErr:
			logger.error(f'Error placing order: {tastyErr}')
			return False
		except Exception as exc:
			logger.error(f'Unexpected exception placing order: {exc}')
			return False
		
	async def adjustOrder(self, order: BrokerOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		raise NotImplementedError()
		
	async def requestTickerData(self, symbols: List[str]):
		"""
		Request ticker data for the given symbols and their options
		"""
		self._streamer = await DXLinkStreamer.create(self._session)

		quote_symbols = []
		candle_symbols = []

		for symbol in symbols:
			match symbol:
				case 'SPX':
					symbolData = TastySymbolData()
					symbolData.symbol = symbol
					symbolData.tastySymbol = 'SPX'
					quote_symbols.append('SPX')
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.tastySymbol] = symbol
				case 'VIX':
					symbolData = TastySymbolData()
					symbolData.symbol = symbol
					symbolData.tastySymbol = 'VIX'
					candle_symbols.append('VIX')
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.tastySymbol] = symbol
				case _:
					logger.error(f'Symbol {symbol} currently not supported by Tastytrade Connector!')
					continue

		# subscribe to quotes and greeks for all options on that date
		await self._streamer.subscribe(Quote, quote_symbols)
		await self._streamer.subscribe(Greeks, symbols)
		#await self._streamer.subscribe(Candle, candle_symbols)
		startTime = dt.datetime.now() - timedelta(days=1)
		await self._streamer.subscribe_candle(candle_symbols, interval='1m', start_time=startTime)

		t_listen_quotes = asyncio.create_task(self._update_quotes())
		t_listen_greeks = asyncio.create_task(self._update_greeks())
		t_listen_candle = asyncio.create_task(self._update_candle())
		self._streamerFuture = asyncio.gather(t_listen_quotes, t_listen_greeks, t_listen_candle )

		try:
			await self._streamerFuture
		except asyncio.CancelledError:
			logger.debug('Cancelled listening to quotes and greeks') 

		# wait we have quotes and greeks for each option
		#while len(self.greeks) != len(options) or len(self.quotes) != len(options):
		#	await asyncio.sleep(0.1)

		#for symbol in symbols:
		#	chain = get_option_chain(self._session, symbol)
		#	pass
		#live_prices = await TastyLivePrices.create(self._session, 'SPX', date(2024, 11, 15))

		#self._streamer = await DXLinkStreamer.create(self._session)
		#await self._streamer.subscribe(Quote, symbols)
		#while True:
		#	quote = await self._streamer.get_event(Quote)
		#	print(quote)
		#listen_quotes_task = asyncio.create_task(self._update_quotes())
		#asyncio.gather(listen_quotes_task)

	async def _update_quotes(self):
		async for e in self._streamer.listen(Quote):
			logger.trace(f'Received Quote: {e.eventSymbol} bid price: {e.bidPrice} ask price: {e.askPrice}')
			# Preisdaten speichern
			if not e.eventSymbol.startswith('.'):
				# Symbol ist ein Basiswert
				try:
					genericSymbol = self._symbolReverseLookup[e.eventSymbol]
					symbolData: TastySymbolData  = self._symbolData[genericSymbol]
					midPrice = (e.bidPrice + e.askPrice) / 2
					atmStrike = OptionHelper.roundToStrikePrice(midPrice)
					# Prüfen ob Optionsdaten für 10 Strikes vorhanden sind
					#try:
					expirationDate = dt.date.today()
					#		optionPriceDataToday = symbolData.optionPriceData[expirationDate]
					#
					#except KeyError as keyErr:
					#	# Keine Daten für den heutigen Tag vorhanden
					#	logger.debug(f'No option price data for today found for symbol {e.eventSymbol}')
					await self._requestMissingOptionData(symbolData, expirationDate, atmStrike)
				except KeyError as keyErr:
					logger.error(f'No generic symbol found for tastytrade symbol {e.eventSymbol}')
					return
			else:
				# Symbol ist eine Option
				try:
					symbol, optionType, expiration, strike = self._getOptionInfos(e.eventSymbol)
					symbolData = self._symbolData[genericSymbol]
					optionStrikeData = symbolData.optionPriceData[expiration]
					optionStrikePriceData = optionStrikeData.strikeData[strike]
					if optionType == OptionType.CALL:
						optionStrikePriceData.callBid = e.bidPrice
						optionStrikePriceData.callAsk = e.askPrice
					else:
						optionStrikePriceData.putBid = e.bidPrice
						optionStrikePriceData.putAsk = e.askPrice
					pass
				except Exception as exc:
					logger.error(f'Error getting option infos: {exc}')
					return
	
	async def _update_greeks(self):
		async for e in self._streamer.listen(Greeks):
			logger.debug(f'Received Greeks: {e.eventSymbol} delta: {e.delta}')

	async def _update_candle(self):
		async for e in self._streamer.listen(Candle):
			pass
			#logger.debug(f'Received Candle: {e.eventSymbol} close: {e.close}')

	def getFillPrice(self, order: BrokerOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		raise NotImplementedError
	
	async def _requestMissingOptionData(self, symbolData: TastySymbolData, expirationDate: dt.date, atmStrike: float):
		"""
		Request option data for the given symbol and expiration date
		"""
		chain = None
		# Bestehende gespeicherte Optionsdaten holen
		try:
			optionStrikeData = symbolData.optionPriceData[expirationDate]
		except KeyError as keyErr:

			# Wenn noch keine Optionsdaten für das Verfallsdatum vorhanden sind, dann bei Tasty anfragen ob es Optionsdaten gibt
			chain = get_option_chain(self._session, symbolData.tastySymbol)
			optionsAtExpiration = [o for o in chain[expirationDate]]
			if len(optionsAtExpiration) == 0:
				logger.error(f'No options available for symbol {symbolData.tastySymbol} and expiration date {expirationDate}')
				return

			optionStrikeData = OptionStrikeData()
			symbolData.optionPriceData[expirationDate] = optionStrikeData
		
		# Die 20 Strike um den ATM Strike herum abrufen
		symbolInformation = symbolInfo.symbol_infos[symbolData.symbol]
		strikesOfInterest = [atmStrike]
		for count in range(1, 20, 1):
			strikePriceAboveATM = atmStrike + (symbolInformation.strike_interval * count)
			strikePriceBelowATM = atmStrike - (symbolInformation.strike_interval * count)
			strikesOfInterest.append(strikePriceAboveATM)
			strikesOfInterest.append(strikePriceBelowATM)
		
		strikesToBeRequested = []
		for strikePrice in strikesOfInterest:
			try:
				optionStrikeData.strikeData[strikePrice]
			except KeyError as keyErr:
				optionStrikeData.strikeData[strikePrice] = OptionStrikePriceData()
				strikesToBeRequested.append(strikePrice)

		if len(strikesToBeRequested) > 0:
			if chain == None:
				chain = get_option_chain(self._session, symbolData.tastySymbol)
				optionsAtExpiration = [o for o in chain[expirationDate]]

			streamer_symbols = []
			for option in optionsAtExpiration:
				if option.strike_price in strikesToBeRequested:
					streamer_symbols.append(option.streamer_symbol)
			await self._streamer.subscribe(Quote, streamer_symbols)
		else:
			logger.debug(f'No new option data to be requested')
		
	def _getOptionInfos(self, tastySymbol: str) -> tuple:
		"""
		Extracts the generic symbol and expiration date, strike and option side from the tastytrade option symbol.
		If the option symbol information cannot be parsed as expected, a ValueError exception is raised.
		"""
		error = False
		pattern = r'^.(?P<optionsymbol>[A-Z]+)(?P<expiration>[0-9]+)(?P<type>[CP])(?P<strike>[0-9]+)'
		compiledPattern = re.compile(pattern)
		match = compiledPattern.match(tastySymbol)
		try:
			if match:
				optionSymbol = match.group('optionsymbol')
				for symbol, symbol_info in symbolInfo.symbol_infos.items():
					if symbol_info.symbol + symbol_info.option_symbol_suffix == optionSymbol:
						genericSymbol = symbol_info.symbol
						break
				expirationDate = dt.datetime.strptime(match.group('expiration'), '%y%m%d').date()
				strike = float(match.group('strike'))
				optionType = OptionType.CALL if match.group('type') == 'C' else OptionType.PUT
		except IndexError as indexErr:
			logger.error(f'Invalid option symbol {tastySymbol}')
			error = True
		except ValueError as valueErr:
			logger.error(f'Invalid option symbol {tastySymbol}')
			error = True
		if genericSymbol == None or error == True:
			raise ValueError(f'Invalid option symbol {tastySymbol}')
		return genericSymbol, optionType, expirationDate, strike