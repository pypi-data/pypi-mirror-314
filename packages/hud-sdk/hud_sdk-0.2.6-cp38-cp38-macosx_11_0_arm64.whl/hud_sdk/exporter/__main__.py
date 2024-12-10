import asyncio

from ..utils import send_fatal_error
from .exporter import Exporter

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        exporter = Exporter()
        loop.run_until_complete(exporter.run())
    except Exception:
        try:
            send_fatal_error(message="Exporter failed")
        except Exception:
            pass
        raise
