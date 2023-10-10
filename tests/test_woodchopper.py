###########
# IMPORTS #
###########

from woodchopper import Logger, Logging_Levels, DateTime_Defaults, __version__

#################
# GENERAL TESTS #
#################


def test_version():
	assert __version__ == "2.0.0"


def test_datetimes():
	assert DateTime_Defaults.DATE_ONLY == "%d/%m/%Y"
	assert DateTime_Defaults.TIME_ONLY == "%H:%M:%S"
	assert DateTime_Defaults.DATE_AND_TIME == "%d/%m/%Y %H:%M:%S"
	assert DateTime_Defaults.DO_NOT_SHOW == ""


def test_logging_levels():
	assert Logging_Levels.DEBUG == 4
	assert Logging_Levels.DEFAULT == 3
	assert Logging_Levels.WARNING == 2
	assert Logging_Levels.ERROR == 1
	assert Logging_Levels.SILENT == 0


################
# OBJECT TESTS #
################


log = None


def test_init():
	global log

	log = Logger("./spam.log", logging_level=Logging_Levels.DEFAULT, show_datetime=DateTime_Defaults.DO_NOT_SHOW, quiet=True)


def test_level():
	level = log.set_logging_level(Logging_Levels.DEBUG)
	assert log.logging_level == Logging_Levels.DEBUG and level == Logging_Levels.DEBUG


def test_level_not_int_is_not_implemented():
	level = log.set_logging_level("Hello, world!")
	assert level == NotImplemented


def test_log():
	log.log("Hello, world!")


def test_debug():
	log.debug("Ate 1 can of spam. Cans of spam remaining: 25.")


def test_info():
	log.info("Sent order for 50 cans of spam.")


def test_warn():
	log.warn("Running low on spam: 7 cans left.")


def test_error():
	log.error("Houston, we have a problem: cans of spam left: 0.")


def test_del():
	global log

	log.__del__()
	try:
		assert log.file.closed
	finally:
		del log
