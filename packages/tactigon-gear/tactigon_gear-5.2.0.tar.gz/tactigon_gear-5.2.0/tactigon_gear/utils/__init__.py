from queue import Full, Empty
from multiprocessing import get_context
from multiprocessing.queues import Queue

from typing import Optional

class RollingQueue(Queue):
    def __init__(self, maxsize: int = 0):
        ctx = get_context()
        Queue.__init__(self, maxsize=maxsize, ctx=ctx)

    def put(self, obj, block: bool = True, timeout: Optional[float] = None):
        try:
            Queue.put(self, obj, block, timeout)
        except Full as e:
            Queue.get_nowait(self)
            Queue.put(self, obj, block, timeout)