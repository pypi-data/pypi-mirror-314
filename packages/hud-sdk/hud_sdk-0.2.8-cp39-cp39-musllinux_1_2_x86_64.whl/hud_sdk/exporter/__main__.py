import asyncio
import sys

from ..utils import send_fatal_error
from .exporter import Exporter

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    unique_id = sys.argv[1]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        exporter = Exporter(unique_id)
        loop.run_until_complete(exporter.run())
    except Exception:
        try:
            send_fatal_error(message="Exporter failed")
        except Exception:
            pass
        raise
