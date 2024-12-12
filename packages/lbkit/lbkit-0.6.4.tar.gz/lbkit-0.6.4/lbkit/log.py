import logging
import inspect
import os
from lbkit.misc import Color

class Logger(logging.getLoggerClass()):

    def __init__(self, *args, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)
        self.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        self.logenv = os.environ.get("LOG")
        if self.logenv is None:
            formatter = logging.Formatter('%(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            if self.logenv == "info":
                self.setLevel(logging.INFO)
            elif self.logenv == "warn":
                self.setLevel(logging.WARNING)
            elif self.logenv == "error":
                self.setLevel(logging.ERROR)
            else:
                self.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        self.handlers = []
        self.addHandler(handler)

    def error(self, msg, *args, **kwargs):
        if self.logenv:
            uptrace = kwargs.get("uptrace", 0)
            uptrace += 1
            stack = inspect.stack()[uptrace]
            filename = os.path.basename(stack.filename)
            msg = f"[{filename}:{stack.lineno}] " + Color.RED + msg + Color.RESET_ALL
        else:
            msg = Color.RED + msg + Color.RESET_ALL
        kwargs.pop("uptrace", None)
        super(Logger, self).error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.logenv:
            uptrace = kwargs.get("uptrace", 0)
            uptrace += 1
            stack = inspect.stack()[uptrace]
            filename = os.path.basename(stack.filename)
            msg = f"[{filename}:{stack.lineno}] " + msg
        kwargs.pop("uptrace", None)
        super(Logger, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.logenv:
            uptrace = kwargs.get("uptrace", 0)
            uptrace += 1
            stack = inspect.stack()[uptrace]
            filename = os.path.basename(stack.filename)
            msg = f"[{filename}:{stack.lineno}] " + msg
        kwargs.pop("uptrace", None)
        super(Logger, self).info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        if self.logenv:
            uptrace = kwargs.get("uptrace", 0)
            uptrace += 1
            stack = inspect.stack()[uptrace]
            filename = os.path.basename(stack.filename)
            msg = f"[{filename}:{stack.lineno}] " + Color.YELLOW + msg + Color.RESET_ALL
        else:
            msg = Color.YELLOW + msg + Color.RESET_ALL
        kwargs.pop("uptrace", None)
        super(Logger, self).warning(msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        if self.logenv:
            uptrace = kwargs.get("uptrace", 0)
            uptrace += 1
            stack = inspect.stack()[uptrace]
            filename = os.path.basename(stack.filename)
            msg = f"[{filename}:{stack.lineno}] " + Color.GREEN + msg + Color.RESET_ALL
        else:
            msg = Color.GREEN + msg + Color.RESET_ALL
        kwargs.pop("uptrace", None)
        super(Logger, self).info(msg, *args, **kwargs)

