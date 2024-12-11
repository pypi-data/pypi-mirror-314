from typing import OrderedDict
from datetime import datetime
import pytz

from loguru import logger
class TriggerType:
	External: str = 'external'
	Time: str = 'time'

class TemplateTrigger:
	def __init__(self, triggerdata: OrderedDict) -> None:
		type = triggerdata['type']
		assert type in [TriggerType.External, TriggerType.Time]
		self.type = type
		self.value = triggerdata['value']
		assert self.value != '' and self.value != None
		
		try:
			timefrom = triggerdata['timefrom']
			self.fromTimeUTC = self.parseTimeWithTimezone(timefrom).astimezone(pytz.utc)
		except KeyError:
			self.fromTimeUTC = None
		except ValueError as valError:
			logger.error(f'Invalid time format for parameter "timefrom"!')

		try:
			timeto = triggerdata['timeto']
			self.toTimeUTC = self.parseTimeWithTimezone(timeto).astimezone(pytz.utc)
		except KeyError:
			self.toTimeUTC = None
		except ValueError as valError:
			logger.error(f'Invalid time format for parameter "timeto"!')

		try:
			excludeTimeFrom = triggerdata['excludetimefrom']
			self.excludeFromTimeUTC = self.parseTimeWithTimezone(excludeTimeFrom).astimezone(pytz.utc)
		except KeyError:
			self.excludeFromTimeUTC = None
		except ValueError as valError:
			logger.error(f'Invalid time format for parameter "excludetimefrom"!')

		try:
			excludeTimeTo = triggerdata['excludetimeto']
			self.excludeToTimeUTC = self.parseTimeWithTimezone(excludeTimeTo).astimezone(pytz.utc)
		except KeyError:
			self.excludeToTimeUTC = None
		except ValueError as valError:
			logger.error(f'Invalid time format for parameter "excludetimeto"!')
		
	def parseTimeWithTimezone(self, timeStr: str) -> datetime.time:
		""" 
		Parses a time string like 11:00 EST to a datetime.time object
		"""
		if timeStr == None:
			return None
		
		parts = timeStr.split(' ')
		try:
			naive_time = datetime.strptime(parts[0], '%H:%M')
			if len(parts) > 1:
				tzstr = parts[1]
			else:
				tzstr = 'EST'
			tz = pytz.timezone(tzstr)
			localized_time = tz.localize(naive_time)
			return localized_time
		except ValueError and AttributeError as error:
			logger.error(f'Invalid time format: {timeStr} - Expecting HH:MM <Timezone>')
			return None

	def toDict(self):
		""" Returns a dictionary representation of the Trigger which is used for
		the config file.
		"""
		returnDict = {'type': self.type, 'value': self.value}
		return returnDict