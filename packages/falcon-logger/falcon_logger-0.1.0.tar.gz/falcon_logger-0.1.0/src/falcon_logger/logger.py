import queue
import sys
import threading
import time
import traceback


# --------------------
## holds logging functions that replace common python logger functions
class FalconLogger:

    # --------------------
    ## constructor
    #
    # @param path        None for stdout, or full path to the logger file
    # @param max_entries (optional) maximum number of entries before a flush is done; default 10
    # @param loop_delay  (optional) time between checking queue; default 0.250 seconds
    def __init__(self, path=None, max_entries=10, loop_delay=0.250):
        ## the full path to the log file
        self._path = path

        ## the maximum entries to hold in the queue before saving to the file
        self._max_entries = max_entries
        if self._max_entries <= 0:
            raise Exception('max_entries must be greater than 0')  # pylint: disable=broad-exception-raised

        ## the delay between checking the queue for entries to save
        self._loop_delay = loop_delay
        if self._loop_delay < 0.100:
            raise Exception('loop_delay must be >= 0.100 seconds')  # pylint: disable=broad-exception-raised

        # print every second even if less than max_entries are in the queue
        ## the maximum number of loops before the queue is emptied
        self._max_count = int(round(1 / self._loop_delay, 1))

        ## the queue
        self._queue = queue.Queue()
        ## the file pointer
        if self._path is None:
            self._fp = sys.stdout
        else:
            self._fp = open(self._path, 'w', encoding='UTF-8')  # pylint: disable=consider-using-with

        ## flag to the thread to end the loop
        self._finished = False
        ## the thread pointer
        self._thread = threading.Thread(target=self._runner)
        self._thread.daemon = True
        self._thread.start()
        # wait for thread to start
        time.sleep(0.1)

    # --------------------
    ## log a debug line
    #
    # @param msg the line to print; default empty
    # @return None
    def debug(self, msg=''):
        self._queue.put(msg)

    # --------------------
    ## log an info line
    #
    # @param msg the line to print; default empty
    # @return None
    def info(self, msg=''):
        self._queue.put(msg)

    # --------------------
    ## log a warning line
    #
    # @param msg the line to print; default empty
    # @return None
    def warning(self, msg=''):
        self._queue.put(msg)

    # --------------------
    ## log an error line
    #
    # @param msg the line to print; default empty
    # @return None
    def error(self, msg=''):
        self._queue.put(msg)

    # --------------------
    ## log a critical line
    #
    # @param msg the line to print; default empty
    # @return None
    def critical(self, msg=''):
        self._queue.put(msg)

    # --------------------
    ## log an exception
    #
    # @param excp the exception to print
    # @return None
    def exception(self, excp):
        for line in traceback.format_exception(excp):
            self._queue.put(line)

    # --------------------
    ## terminate
    # stop the thread, save any remaining line in the internal queue
    #
    # @return None
    def term(self):
        self._finished = True
        if self._thread.is_alive():  # pragma: no cover
            self._thread.join(5)

    # --------------------
    ## do a save at this point
    #
    # @return None
    def save(self):
        self._save()

    # --------------------
    ## the thread runner
    # wakes periodically to check if the queue has max_entries or more in it
    # if so, the lines are written to the file
    # if not, it sleeps
    #
    # @return None
    def _runner(self):
        count = 0
        while not self._finished:
            if count < self._max_count and self._queue.qsize() < self._max_entries:
                count += 1
                time.sleep(self._loop_delay)
                continue

            count = 0
            self._save()

        self._save()
        if self._path:
            self._fp.close()
            self._fp = None

    # --------------------
    ## save any entries in the queue to the file
    #
    # @return None
    def _save(self):
        if self._fp is None:
            self._finished = True
            return

        count = self._queue.qsize()
        while count > 0:
            msg = self._queue.get_nowait()
            # TODO print(msg)
            self._fp.write(msg)
            self._fp.write('\n')
            count -= 1
        self._fp.flush()
