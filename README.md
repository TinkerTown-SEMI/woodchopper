# ![Woodchopper](https://github.com/TinkerTown-SEMI/woodchopper/raw/main/assets/icons/woodchopper_with_log.png)

*A lightweight logging package*

[![build](https://img.shields.io/github/actions/workflow/status/TinkerTown-SEMI/woodchopper/python-package.yml?style=for-the-badge)](https://github.com/TinkerTown-SEMI/woodchopper/actions/workflows/python-package.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/woodchopper?style=for-the-badge&logo=pypi)](https://pypi.org/project/woodchopper)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/woodchopper?style=for-the-badge)](https://pypi.org/project/woodchopper)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json&style=for-the-badge)](https://python-poetry.org/)
[![GitHub License](https://img.shields.io/github/license/TinkerTown-SEMI/woodchopper?style=for-the-badge)](https://www.gnu.org/licenses/lgpl-3.0.en.html)


### Table of contents
[Back to Top](#woodchopper)

[Table of contents](#table-of-contents)

[Installation](#installation)
- [Using `pip`](#using-pip)
	- [Unix/mac/linux](#unixmaclinux)
	- [Windows](#windows)
- [Building from source](#building-from-source)
	- [Unix/mac/linux](#unixmaclinux-1)
	- [Windows](#windows-1)

[Usage](#usage)
- [Creating a log](#creating-a-log)
- [Logging plaintext](#logging-plaintext)
- [Logging debug information](#logging-debug-information)
- [Logging information](#logging-information)
- [Logging warnings](#logging-warnings)
- [Logging errors](#logging-errors)

[Getting help](#getting-help)

## Installation

### Using `pip`
To install this package using pip, simply run the following command:

#### Unix/mac/linux
```bash
pip3 install woodchopper
```


#### Windows
```cmd
pip install woodchopper
```

### Building from source

#### Unix/mac/linux
##### Requirements:
- Python >=3.8.1
- Git
- Poetry >=1.5.1

Run the following in the terminal:
```bash
git clone https://github.com/TinkerTown-SEMI/woodchopper.git
cd woodchopper

make install-dev
make lint test
make -j4 all
```

#### Windows
##### Requirements:
- Python >=3.8.1
- Git
- Poetry >=1.5.1
- [w64devkit](https://github.com/skeeto/w64devkit) (GNU binaries for windows, including `make`). When you extract the folder, add the folder to the path.

Run the following in the terminal:
```cmd
git clone https://github.com/TinkerTown-SEMI/woodchopper.git
cd woodchopper

make install-dev
make lint test
make -j4 all
```


## Usage
### Creating a log
To use woodchopper, you first have to create a log.
```py
from woodchopper import Logging_Levels, DateTime_Defaults, Styles, Logger
from pathlib import Path

log = Logger(
	Path("./spam.log").resolve(),  # Path to log file
	show_datetime=DateTime_Defaults.DO_NOT_SHOW,  # Don't show date and time. Other options: DateTime_Defaults.DATE_AND_TIME, DateTime_Defaults.DATE_ONLY, DateTime_Defaults.TIME_ONLY
	logging_level=Logging_Levels.DEBUG,  # Allow all logging operations. Other options: Logging_Levels.DEFAULT, Logging_Levels.WARNING, Logging_Levels.ERROR, Logging_Levels.SILENT.
	quiet=True  # Suppress log messages on creation and deletion.
)
```

### Logging plaintext
```py
log.log("Hello, world!")
```
##### Output:
<pre>Hello, world!</pre>

### Logging debug information
```py
log.debug("Ate 1 can of spam. Cans of spam remaining: 25.")
```
##### Output[^1]:
<pre><span style="color: orange; font-weight: bold;">DEBUG: </span>Ate 1 can of spam. Cans of spam remaining: 25.</pre>

### Logging information
```py
log.info("Sent order for 50 cans of spam.")
```
##### Output[^1]:
<pre><span style="color: blue; font-weight: bold;">INFO: </span>Sent order for 50 cans of spam.</pre>

### Logging warnings
```py
log.warn("Running low on spam: 7 cans left.")
```
##### Output[^1]:
<pre><span style="color: yellow; font-weight: bold;">WARNING: </span>Running low on spam: 7 cans left.</pre>

### Logging errors
```py
log.error("Houston, we have a problem: cans of spam left: 0.")
```
##### Output[^1]:
<pre><span style="color: red; font-weight: bold;">ERROR: </span> Houston, we have a problem: cans of spam left: 0.</pre>

## Getting help

You can get help regarding this package in many ways. If you need help with syntax, your first stop should always be help manuals, so you could use python's [built-in help function](https://docs.python.org/3.11/library/functions.html#help), as we do not yet have full documentation published(sorry). For errors, it should be the [bug tracker](https://github.com/TinkerTown-SEMI/woodchopper/issues), and for more generic python errors, you could go over to [StackOverflow](https://stackoverflow.com).

## Happy logging, folks!

![Log](https://github.com/TinkerTown-SEMI/woodchopper/raw/main/assets/icons/log.png)
[^1]: Sorry, colored/styled text isn't available in github markdown.
