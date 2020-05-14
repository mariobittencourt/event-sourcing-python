from typing import List
import functools
from src.domain.models.domain_event import DomainEvent


def method_dispatch(func):
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


class Aggregate:
    def __init__(self):
        self._events = []

    @property
    def events(self) -> List[DomainEvent]:
        return self._events

    def clear_events(self):
        self._events = []

    @method_dispatch
    def apply(self, event: DomainEvent):
        raise ValueError('Unknown event!')
