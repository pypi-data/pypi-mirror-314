from .hook import set_hook as set_hook
from .load import load_hud
from .logging import internal_logger as internal_logger
from .version import version as __version__
from .worker.worker import init_hud_thread as init

load_hud()

del internal_logger

__all__ = ["__version__", "set_hook", "init"]
