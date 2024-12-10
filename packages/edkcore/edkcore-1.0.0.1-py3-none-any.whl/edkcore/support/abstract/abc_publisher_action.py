from abc import ABC

from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.publisher import Publisher


class AbcPublisherAction(AbcContextAction, Publisher, ABC):
    def append(self, action, is_subscriber=False, *args, **kwargs):
        super(AbcPublisherAction, self).append(action)
        if is_subscriber: self.add_subscriber(action)
