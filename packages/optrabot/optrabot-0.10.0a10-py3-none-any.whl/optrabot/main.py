import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from loguru import logger
import optrabot.config as optrabotcfg
from .optrabot import OptraBot
import uvicorn
import sys
import argparse

ValidLogLevels = ['DEBUG', 'INFO', 'WARN', 'ERROR']

@asynccontextmanager
async def lifespan(app: FastAPI):
	await app.optraBot.startup()
	yield
	await app.optraBot.shutdown()

"""fix yelling at me error"""
from functools import wraps
 
from asyncio.proactor_events import _ProactorBasePipeTransport
 
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper
 
_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
"""fix yelling at me error end"""

app = FastAPI(lifespan=lifespan)
app.optraBot = OptraBot(app)

@app.get("/")
async def root():
	return "Welcome to OptraBot"

def configureLogging(requestedLogLevel):
	loglevel = 'INFO'
	if requestedLogLevel not in ValidLogLevels and requestedLogLevel != None:
		print(f'Log Level {requestedLogLevel} is not valid!')
	elif requestedLogLevel != None:
		loglevel = requestedLogLevel
	
	logFormat = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> |"
	if loglevel == 'DEBUG':
		logFormat += "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
	logFormat += "<level>{message}</level>"

	logger.remove()
	logger.add(sys.stderr, level=loglevel, format = logFormat)
	logger.add("optrabot.log", level='DEBUG', format = logFormat, rotation="5 MB", retention="10 days")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--loglevel", help="Log Level", choices=ValidLogLevels)
	args = parser.parse_args()
	configureLogging(args.loglevel)
	
	if optrabotcfg.ensureInitialConfig()	== True:
		# Get web port from config
		configuration = optrabotcfg.Config("config.yaml")
		webPort: int
		try:
			webPort = configuration.get('general.port')
		except KeyError as keyErr:
			webPort = 8080
		uvicorn.run("optrabot.main:app", port=int(webPort), log_level="info")
	else:
		print("Configuration error. Unable to run OptraBot!")