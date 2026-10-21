#!/bin/sh
# For local test run


method=$1

# If method is not specified, use 0 as default value
if [ -z "$method" ]; then
  echo "run as module ... "
  method=0
fi;

if [[ ! "$method" =~ ^[0-9]+$ ]]; then
  echo "error: method must be numeric"
  echo "usage: $0 <method>"
  echo "method (0 = run as module, 1 = run as script)"
  exit;
fi;

if [ "$method" == 0 ]; then
  # -m tells python to run the specified parameter as a module,
  # resolving path issues that occurs when running it as a script
  python3 -m app.pneumonia_app
elif [ "$method" == 1 ]; then
  # run it as a script
  PYTHONPATH=. python3 app/pneumonia_app.py
else:
  echo "usage: $0 <method>"
  echo "method (0 = run as module, 1 = run as script)"
  exit;
fi;
