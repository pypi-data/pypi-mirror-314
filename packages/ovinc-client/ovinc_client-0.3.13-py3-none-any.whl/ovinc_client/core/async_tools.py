import asyncio
from threading import Thread
from typing import Coroutine


class SyncRunner:
    """
    Run an async func in sync func
    """

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self._run_loop_in_thread)
        self.thread.start()

    def _run_loop_in_thread(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    # pylint: disable=C0103
    def run(self, co: Coroutine):
        try:
            future = asyncio.run_coroutine_threadsafe(co, self.loop)
            return future.result()
        finally:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join()
            self.loop.close()
