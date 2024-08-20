# -*- coding: utf-8 -*-

###########
# IMPORTS #
###########

from datetime import datetime
from io import TextIOWrapper
from os import PathLike, fsync
from pathlib import Path
from typing import Any

from rich import print
from spacename import Namespace


#########
# SETUP #
#########

__version__ = "2.0.3"

# Logging levels

Logging_Levels = Namespace(
	DEBUG=4,
	DEFAULT=3,
	WARNING=2,
	ERROR=1,
	SILENT=0,
	__doc__="""
Logging Level options.
         Name          | Val |                   Allow
-----------------------+-----+------------------------------------------
Logging_Levels.DEBUG   | >=4 | [debug, info, warn, error, log, log_list]
Logging_Levels.DEFAULT |  3  | [info, warn, error, log, log_list]
Logging_Levels.WARNING |  2  | [warn, error, log, log_list]
Logging_Levels.ERROR   |  1  | [error, log, log_list]
Logging_Levels.SILENT  |  0  | [log, log_list]
""" # noqa
)

# Datetime options

DateTime_Defaults = Namespace(
	DATE_ONLY="%d/%m/%Y",
	TIME_ONLY="%H:%M:%S",
	DATE_AND_TIME="%d/%m/%Y %H:%M:%S",
	DO_NOT_SHOW="",
	__doc__="""
Date format for strftime().
     Name     |         Val         |    Function
--------------+---------------------+----------------
DATE_ONLY     |     "%d/%m/%Y"      | Show date only
TIME_ONLY     |     "%H:%M:%S"      | Show time only
DATE_AND_TIME | "%d/%m/%Y %H:%M:%S" | Show both
DO_NOT_SHOW   |         ""          | Show neither
""" # noqa
)

# Styles

Styles = Namespace(
	default="[default]",
	white="[white]",
	pink="[pink1]",
	red="[red]",
	orange="[orange3]",
	yellow="[yellow]",
	green="[green]",
	blue="[blue]",
	purple="[purple3]",
	black="[black]",
	bold="[bold]",
	italic="[italic]",
	debug="[bold orange3]",
	info="[bold blue]",
	warn="[bold yellow]",
	error="[bold red]",
	success="[bold green]",
	__doc__="""
Style in rich [style][/] format.
  Name  |  Color  | Emphasis
--------+---------+----------
default | default | default
bold    | default | bold
italic  | default | italic
white   | white   | default
pink    | pink1   | default
red     | red     | default
orange  | orange3 | default
yellow  | yellow  | default
green   | green   | default
blue    | blue    | default
purple  | purple3 | default
black   | black   | default
debug   | orange3 | bold
info    | blue    | bold
warn    | yellow  | bold
error   | red     | bold
success | green   | bold
""" # noqa
)

##########
# LOGGER #
##########


class Logger:
	"""A class that provides logging functionality.

	Attributes:
		logging_level (int): The logging level.
		show_datetime (str): Datetime format for strftime.
		file (file-like object): The log file.
		quiet_on_del (bool): Flag indicating whether the logger should stay quiet on create and delete.

	Methods:
		__init__(self, logpath=None, show_datetime=DateTime_Defaults.DO_NOT_SHOW, logging_level=Logging_Levels.DEFAULT, quiet=False):
			Initialize a Woodchopper Logger instance.
		__del__(self):
			Perform cleanup operations when the Woodchopper Logger instance is deleted.
		set_logging_level(self, logging_level):
			Set the logging level for the Woodchopper Logger instance.
		log(self, *msgs, prefix_style=Styles.default, text_style=Styles.bold, prefix="", show_datetime=show_datetime):
			Log message(s) to stdout using rich.print().
		debug(self, *msgs, prefix="DEBUG: ", show_datetime=show_datetime):
			Log debug information.
		info(self, *msgs, prefix="INFO: ", show_datetime=show_datetime):
			Log information.
		warn(self, *msgs, prefix="WARNING: ", show_datetime=show_datetime):
			Log warnings or non-critical errors.
		error(self, *msgs, prefix="ERROR: ", show_datetime=show_datetime):
			Log critical errors.
	"""

	def __init__(
		self,
		logpath: PathLike = None,
		show_datetime: str = DateTime_Defaults.DO_NOT_SHOW,
		logging_level: int = Logging_Levels.DEFAULT,
		quiet: bool = False
	) -> None:  # sourcery skip: assign-if-exp
		"""Initialize a Woodchopper Logger instance.

		Args:
			logpath (str | Path): The path to the log file. Defaults to None.
			show_datetime (str): Determines whether to show the datetime in log messages. Defaults to DateTime_Defaults.DO_NOT_SHOW.
			logging_level (int): The logging level for the logger. Defaults to Logging_Levels.DEFAULT.
			quiet (bool): Determines whether to suppress log messages during object deletion. Defaults to False.

		Example:
			from woodchopper import Logger, DateTime_Defaults, Logging_Levels
			logger = Logger(
				logpath="./logs/app.log",
				show_datetime=DateTime_Defaults.DO_NOT_SHOW,
				logging_level=Logging_Levels.DEFAULT,
				quiet=False
			)
		"""

		if logpath:
			logpath = Path(str(logpath)).resolve()
			parent_dir = logpath.parent

			if not logpath.exists():
				mode = "wt"
				if not parent_dir.exists():
					parent_dir.mkdir(parents=True)
			elif logpath.is_file():
				mode = "at"
			else:
				raise IsADirectoryError(f"The path you provided for the logfile (\"{logpath}\") is a directory.")

			self.file = open(logpath, mode)
		else:
			self.file = None

		self.show_datetime = show_datetime
		self.logging_level = logging_level
		self.quiet_on_del = quiet
		if not quiet:
			self.info(f"Created log \"{self}\"", show_datetime=show_datetime)

	def __del__(
		self
	) -> None:
		"""Perform cleanup operations when the Woodchopper Logger instance is deleted.
		"""
		if not self.quiet_on_del:
			self.info(f"Deleted log \"{self}\".", show_datetime=self.show_datetime)
		if issubclass(type(self.file), TextIOWrapper):
			self.file.close()

	@property
	def logging_level(self) -> int:
		return self._logging_level

	@logging_level.setter
	def logging_level(self, value: int | Any) -> None:

		try:
			value = int(value)
		except ValueError:
			return

		if value < Logging_Levels.SILENT:
			value = Logging_Levels.SILENT
		elif value > Logging_Levels.DEBUG:
			value = Logging_Levels.DEBUG

		self._logging_level = value

	def log(
		self,
		*msgs,
		prefix_style=Styles.default,
		text_style=Styles.bold,
		prefix="",
		show_datetime=None
	) -> None:
		"""Log message(s) to stdout using rich.print()

		Args:
			msgs (*str): Message(s) to log.
			prefix_style (str, optional): Style of prefix in rich format. Options can be found in woodchopper.Styles namespace. Defaults to Styles.default.
			prefix (str, optional): Include as prefix of message. Defaults to "".
			show_datetime (str, optional): How to log date and time. Options can be found in woodchopper.DateTime_Options. Defaults to self.show_datetime.
		""" # noqa

		show_datetime = show_datetime or self.show_datetime
		date_prefix = f"{datetime.now().strftime(show_datetime)} : " if show_datetime else ""

		for msg in msgs:
			if isinstance(self.file, TextIOWrapper):
				self.file.write(prefix + date_prefix + msg + "\n")
			print(f"{prefix_style}{prefix}[/]{date_prefix}{text_style}{msg}[/]")
		if isinstance(self.file, TextIOWrapper):
			# self.file.write("\n")
			self.file.flush()
			fsync(self.file.fileno())

	def debug(
		self,
		*msgs,
		prefix="DEBUG: ",
		show_datetime=None
	):
		"""Log debug information.

		Args:
			msgs (*str): Message(s) to log.
			prefix (str, optional): Include as prefix of message. Defaults to "DEBUG: ".
			show_datetime (str, optional): How to log date and time. Options can be found in woodchopper.DateTime_Options. Defaults to self.show_datetime.
		""" # noqa

		if self.logging_level >= Logging_Levels.DEBUG:
			self.log(*msgs, prefix_style=Styles.debug, prefix=prefix, show_datetime=show_datetime)

	def info(
		self,
		*msgs,
		prefix="INFO: ",
		show_datetime=None
	):
		"""Log information.

		Args:
			msgs (*str): Message(s) to log.
			prefix (str, optional): Include as prefix of message. Defaults to "INFO: ".
			show_datetime (str, optional): How to log date and time. Options can be found in woodchopper.DateTime_Options. Defaults to self.show_datetime.
		""" # noqa

		if self.logging_level >= Logging_Levels.DEFAULT:
			self.log(*msgs, prefix_style=Styles.info, prefix=prefix, show_datetime=show_datetime)

	def warn(
		self,
		*msgs,
		prefix="WARNING: ",
		show_datetime=None
	):
		"""Log warnings or non-critical errors.

		Args:
			msgs (*str): Message(s) to log.
			prefix (str, optional): Include as prefix of message. Defaults to "DEBUG: ".
			show_datetime (str, optional): How to log date and time. Options can be found in woodchopper.DateTime_Options. Defaults to self.show_datetime.
		""" # noqa

		if self.logging_level >= Logging_Levels.WARNING:
			self.log(*msgs, prefix_style=Styles.warn, prefix=prefix, show_datetime=show_datetime)

	def error(
		self,
		*msgs,
		prefix="ERROR: ",
		show_datetime=None
	):
		"""Log critical errors.

		Args:
			msgs (*str): Message(s) to log.
			prefix (str, optional): Include as prefix of message. Defaults to "DEBUG: ".
			show_datetime (str, optional): How to log date and time. Options can be found in woodchopper.DateTime_Options. Defaults to self.show_datetime.
		""" # noqa

		if self.logging_level >= Logging_Levels.ERROR:
			self.log(*msgs, prefix_style=Styles.error, prefix=prefix, show_datetime=show_datetime)
