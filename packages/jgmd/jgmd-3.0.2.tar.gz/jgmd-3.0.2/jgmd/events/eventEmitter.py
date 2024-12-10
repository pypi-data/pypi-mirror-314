from __future__ import annotations
import asyncio
from collections import defaultdict
from typing import Callable, List, Dict
from ..util import exceptionToStr

_emitter: EventEmitter = None


def getEmitter(onError: Callable = None) -> EventEmitter:
    global _emitter
    if _emitter is None:
        _emitter = EventEmitter(onError)
        if not onError:
            raise Exception(
                "getEmitter() must be called with onError callable as an argument on first call!"
            )
    return _emitter


class EventEmitter:
    def __init__(self, onError: Callable):
        if _emitter is not None:
            raise Exception(
                "EventEmitter must be a singleton! Use getEmitter() to create/get the instance."
            )
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self.onError: Callable[[str], None] = onError

    def on(self, event, listener):
        """Subscribe a listener to an event."""
        if not callable(listener):
            raise TypeError("Listener must be a callable (sync or async function)")
        self._listeners[event].append(listener)

    def off(self, event, listener):
        """Unsubscribe a listener from an event."""
        if listener in self._listeners[event]:
            self._listeners[event].remove(listener)

    def emit(self, event, *args, **kwargs):
        """Emit an event and handle all listeners (sync or async)."""
        if event not in self._listeners:
            return

        errorStrs = []

        for listener in self._listeners[event]:
            if asyncio.iscoroutinefunction(listener):
                # Async listener
                task = asyncio.create_task(listener(event, *args, **kwargs))
                task.add_done_callback(
                    lambda task: self._handle_task_exception(task, event)
                )
            else:
                # Sync listener - execute it directly
                try:
                    listener(event, *args, **kwargs)
                except Exception as e:
                    errorStrs.append(exceptionToStr(e))
        if errorStrs:
            self.onError(event, *errorStrs)

    def _handle_task_exception(self, task: asyncio.Task, event: str):
        """Handle task exceptions."""
        try:
            task.result()  # This will raise the exception if the task failed
        except Exception as e:
            self.onError(event, exceptionToStr(e))
