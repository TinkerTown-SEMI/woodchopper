from datetime import datetime
import io # Not required, just for verifiyng that the logfile is indeed an instance of _io.TextIOWrapper.
from os.path import exists
from pathlib import Path
from rich import print

class Logger:
	# Logger class. Need I say more?
	
	# Class constants
	DATE_ONLY = "date"
	TIME_ONLY = "time"
	DATE_AND_TIME = "both"
	DO_NOT_SHOW = "neither"

	# Instance variables
	file = None
	show_datetime_on_del = DO_NOT_SHOW
	
	# Instance methods
	def __init__(self, logpath=None, show_datetime=DO_NOT_SHOW):
		if logpath != None:
			logpath = Path.resolve(Path(str(logpath)))
			self.file = open(logpath, "at" if exists(logpath) else "wt")
		self.show_datetime_on_del = show_datetime
		self.info(f"Created log \"{self}\"", show_datetime=show_datetime)
	def __del__(self, show_datetime=show_datetime_on_del):
		self.info(f"Deleted log \"{self}\".", show_datetime=show_datetime)
		if issubclass(type(self.file), io.TextIOWrapper):
			self.file.close()
	def log(self, *printargs, c="[white]", start="", end="[/white]", show_datetime=DO_NOT_SHOW):
		# Barebones log function, like console.log in javascript.
		match show_datetime:
			case Logger.DATE_AND_TIME:
				start = str(start) + f"{datetime.now().strftime('%b-%d-%Y %H:%M:%S')} : "
			case Logger.DATE_ONLY:
				start = str(start) + f"{datetime.now().strftime('%b-%d-%Y')} : "
			case Logger.TIME_ONLY:
				start = str(start) + f"{datetime.now().strftime('%H:%M:%S')} : "
			case _:
				start = str(start)
		for printarg in printargs:
			if issubclass(type(self.file), io.TextIOWrapper):
				self.file.write(start + printarg + "\n")
			print(c + start + printarg + end)
		if issubclass(type(self.file), io.TextIOWrapper):
			self.file.write("\n")
	def log_list(self, printargslist, c="[white]", start="", end="[/white]", show_datetime=DO_NOT_SHOW):
		# Function derived from Logger.log, but modified to log arguments passed as lists or tuples.
		for printarg in printargslist:
			self.log(printarg, c=c, start=start, end=end, show_datetime=show_datetime)
	def info(self, *printargs, start="INFO: ", show_datetime=DO_NOT_SHOW):
		# Used for giving verbose information, like console.info in javascript. Derived from Logger.log_list.
		self.log_list(printargs, c="[bold blue]", start=start, end="[/bold blue]", show_datetime=show_datetime)
	def warn(self, *printargs, start="WARNING: ", show_datetime=DO_NOT_SHOW):
		# Used for alerting user of errors that are not critical, like console.warn in javascript. Derived from Logger.log_list.
		self.log_list(printargs, c="[bold yellow]", start=start, end="[/bold yellow]", show_datetime=show_datetime)
	def error(self, *printargs, start="ERROR: ", show_datetime=DO_NOT_SHOW):
		# Used for alerting user of errors that are critical, like console.error in javascript. Derived from Logger.log_list.
		self.log_list(printargs, c="[bold red]", start=start, end="[/bold red]", show_datetime=show_datetime)