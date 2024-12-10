import abc

from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.abstract.abc_subscriber import AbcSubscriber


class AbcSubscriberAction(AbcSubscriber, AbcContextAction, abc.ABC): ...
