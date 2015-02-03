# Doggy-wrapper

The wrapper for doggy application. Monitorize and relaunch the doggy process. Also, dumps the output to a log.

The applications has a rotation logger system given timers and compress the backups logs.

This wrappers execute multiple subprocess of doggy.


# Execution

## Default configuration

The default execution is:

	python doggy-wrapper.py

This execute doggy-wrapper using the default configuration in `conf.py`.

## Command line execution

The arguments for command line are:

- -c CONFIG\_FILE or --config=CONFIG\_FILE: The location of the configuration file

- -p 2 or --processes=3: number of processes to execute at the same time

- -l LOG\_FILE or --logfile=LOG\_FILE: The location of the log file

- -d DOGGY_\___PATH or --doggy=DOGGY_\___PATH: the location of doggy path

- -b s or --blocktime=m: the timer for rotation, s for seconds, m for minutes, h for hours and d for days https://docs.python.org/2/library/logging.handlers.html#timedrotatingfilehandler

- r 10 or --rotating=20: number of time for rotate the log

- --compression=gz: the compression mode gz or zip


## Config file

The config file should be like:

	[doggy-wrapper]
	num_processes=3
	rotating_timer=10
	block_time=s
	log_file=/PATH/TO/wrapper.log
	doggy_path=/PATH/TO/doggy.py
	compress_mode=gz

The arguments are:

	- num\_processes: number of doggy processes
	- rotating\_timer: time to rotate log (integer)
	- block\_time: the time interval, s for seconds, m for minutes, h for hours and d for days https://docs.python.org/2/library/logging.handlers.html#timedrotatingfilehandler
	- log\_file: path to log
	- doggy\_path: location to doggy app
	- compress\_mode: the compression for backups log: gz or zip
