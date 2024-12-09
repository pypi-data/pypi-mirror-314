* website: <https://arrizza.com/python-falcon-logger>
* installation: see <https://arrizza.com/setup-common>

## Summary

This is a python module that provides a way to run a fast logger.
Peregrine Falcons are the fastest animals alive (according to Google).
They go that fast by having as minimal drag as possible.

* See [Quick Start](https://arrizza.com/user-guide-quick-start) for information on using scripts.
* See [xplat-utils submodule](https://arrizza.com/xplat-utils) for information on the submodule.

## Sample code

see sample.py for a full example

```python
from falcon_logger import FalconLogger
```

## Sample

Use doit script to run the logger and compare against other loggers.

To run the FalconLogger:

```bash
./doit falcon
./doit falcon --numlines=100000
```

To run the others loggers:

```bash
./doit stdout  # no file, just stdout
./doit normal  # use the python logger
./doit rsyslog # use the rsyslog python module
```

## Comparing Times

The overall time is very dependent on which OS you use and the speed of your computer

```text
on MSYS2 for 100,000 lines:
stdout: total time: 3170.0 ms
falcon: total time: 3623.9 ms
normal: total time: 5722.8 ms
rsyslog fails with an exception 

```
