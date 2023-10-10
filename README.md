# ![Woodchopper](https://github.com/TinkerTown-SEMI/woodchopper/raw/main/assets/icons/woodchopper_with_log.png)

*A lightweight logging package*

<style>
	span.debug, span.info, span.warn, span.error {
		font-weight: bold;
	}
	span.debug {
		color: orange;
	}
	span.info {
		color: blue;
	}
	span.warn {
		color: yellow;
	}
	span.error {
		color: red;
	}
</style>
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
##### Output:
<pre><span class="debug">DEBUG: </span>Ate 1 can of spam. Cans of spam remaining: 25.</pre>

### Logging information
```py
log.info("Sent order for 50 cans of spam.")
```
##### Output:
<pre><span class="info">INFO: </span>Sent order for 50 cans of spam.</pre>

### Logging warnings
```py
log.warn("Running low on spam: 7 cans left.")
```
##### Output:
<pre><span class="warn">WARNING: </span>Running low on spam: 7 cans left.</pre>

### Logging errors
```py
log.error("Houston, we have a problem: cans of spam left: 0.")
```
##### Output:
<pre><span class="error">ERROR: </span> Houston, we have a problem: cans of spam left: 0.</pre>

## Getting help

You can get help regarding this package in many ways. If you need help with syntax, your first stop should always be help manuals, so you could use python's [built-in help function](https://docs.python.org/3.11/library/functions.html#help), as we do not yet have full documentation published(sorry). For errors, it should be the [bug tracker](https://github.com/TinkerTown-SEMI/woodchopper/issues), and for more generic python errors, you could go over to [StackOverflow](https://stackoverflow.com).

## Happy logging, folks!

![Log](https://github.com/TinkerTown-SEMI/woodchopper/raw/main/assets/icons/log.png)
