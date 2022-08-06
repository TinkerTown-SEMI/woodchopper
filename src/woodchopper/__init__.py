import io # Not required, just for verifiyng that the logfile is indeed an instance of _io.TextIOWrapper.
from rich import print
from os.path import exists
from pathlib import Path

class Logger:
	# Logger class. Need I say more?
	file = None
	def __init__(self, logpath=None):
		if logpath != None:
			logpath = Path.resolve(Path(str(logpath)))
			self.file = open(logpath, "at" if exists(logpath) else "wt")
		self.info(f"Created log \"{self}\"")
	def __del__(self):
		self.info(f"Deleted log \"{self}\".")
		self.file.close()
	def log(self, *printargs, c="[white]", start="", end="[/white]"):
		# Barebones log function, like console.log in javascript.
		for printarg in printargs:
			if issubclass(type(self.file), io.TextIOWrapper):
				self.file.write(start + printarg + "\n")
			print(c + start + printarg + end)
		if issubclass(type(self.file), io.TextIOWrapper):
			self.file.write("\n")
	def log_list(self, printargslist, c="[white]", start="", end="[/white]"):
		# Function derived from Logger.log, but modified to log arguments passed as lists or tuples.
		for printarg in printargslist:
			self.log(printarg, c=c, start=start, end=end)
	def info(self, *printargs, start="INFO: "):
		# Used for giving verbose information, like console.info in javascript. Derived from Logger.log_list.
		self.log_list(printargs, c="[bold blue]", start=start, end="[/bold blue]")
	def warn(self, *printargs, start="WARNING: "):
		# Used for alerting user of errors that are not critical, like console.warn in javascript. Derived from Logger.log_list.
		self.log_list(printargs, c="[bold yellow]", start=start, end="[/bold yellow]")
	def error(self, *printargs, start="ERROR: "):
		# Used for alerting user of errors that are critical, like console.error in javascript. Derived from Logger.log_list.
		self.log_list(printargs, c="[bold red]", start=start, end="[/bold red]")