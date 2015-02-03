# Doggy 

Dummy application that output text, sometimes crash and you can set the proabbility that this application could crash.

# Execution

## Default execution

The default execution is:

	python doggy.py

This execute doggy using the default crashing configuration

## Command line execution

There are two arguments available

- **-p 70 or --probability=30**: the crashing probability

- **-c doggy.conf --configfile=doggy.conf: A config file where the config are setted. The config file arguments override the command line args.

## Config file

The config file is very simple:

	[doggy]
	crashing_probability=20

The only argument available is:

	- crashing\_probability: the probability that doggy should crash
