# ⏰ Process Time Killer

process-time-killer is a Python utility to run subprocesses and terminate them after a specified timeout. This package helps in controlling processes by running commands for a limited time and ensuring they are terminated gracefully or forcefully.

## Features

- Run any subprocess for a specified duration.
- Automatically terminate the subprocess after a given timeout.
- Graceful termination or forced killing if the process does not exit on time.
- Logs all steps, including the start, termination attempt, and any errors.

## Installation

You can install process-time-killer via pip:


```bash
pip install process-time-killer
```

## Usage

Command-line Interface (CLI)

Run the utility from the command line by specifying the command and an optional timeout:

```bash
timekiller "ping google.com" --timeout 10
```


### Arguments:

- command: The command to run in the subprocess (default: "ping google.com").
- --timeout: Time in seconds before the subprocess is terminated (default: 12 seconds).

### Example:

Run the echo command for 5 seconds:

```bash
timekiller "echo Hello World" --timeout 5
```


### Programmatic Usage

You can also use this utility in your Python code by calling the run_subprocess function:

```python

from timekiller import run_subprocess

command = "echo Hello World"
timeout = 10

run_subprocess(command, timeout)

```

## Functions

run_subprocess(command: str, seconds: int)

Runs a subprocess with the specified command and terminates it after the given number of seconds.

### Arguments:

- command (str): The command to execute in the subprocess.
- seconds (int): Number of seconds to run the subprocess before terminating.

### Raises:

- ValueError: If the command or seconds parameter is invalid.
- RuntimeError: If there is an issue with starting or terminating the subprocess.

#### main()

The main function that serves as the entry point for the command-line interface (CLI). It parses the arguments and calls run_subprocess.

## Logging

This package uses Python’s built-in logging module to log:
	•	The start of the subprocess.
	•	The attempt to terminate the subprocess after the timeout.
	•	Any errors that occur during execution.

## License

This project is licensed under the MIT License.


