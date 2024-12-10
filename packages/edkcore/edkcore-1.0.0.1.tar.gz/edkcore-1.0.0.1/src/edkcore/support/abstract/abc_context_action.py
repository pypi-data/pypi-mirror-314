import abc
import uuid

from edkcore.support.abstract.abc_action import AbcAction

from edkcore.support.abstract.abc_properties import AbcProperties
from edkcore.support.context.context_data import ContextData
from edkcore.support.context.context_persistent import ContextPersistent
from edkcore.support.enums.action_enum import ActionEnum


class AbcContextAction(AbcAction):
    def __init__(self, prop: AbcProperties):
        self.uid = uuid.uuid4().hex
        self.acs: list[AbcContextAction] = list()
        self._parent = None
        self._prev = None
        self._next = None
        self._contextdata = self._context_data(prop)
        super().__init__(prop)

    def _on_execute(self):
        for ac in self.acs:
            ac.execute()
            if ac.state.fail():
                # raise AssertionError()
                raise Exception(f"{ac.prop.get('description')} is fail")

    @abc.abstractmethod
    def _context_data(self, properties) -> ContextData:
        """
        指定上下文共享的数据对象，如果有父级action则会被覆盖为父级的
        :param properties:
        :type properties:
        :return:
        :rtype:
        """
        ...

    def on_mount(self, *args, **kwargs):
        """
        在添加到父 ContextAction时， 把 ContextData 设置为 父 ContextAction 的 ContextData
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        if not self._parent.prop.property_type() == ActionEnum.Scene:
            self.set_context_data(self._parent._contextdata)

    def set_context_data(self, context_data):
        self._contextdata = context_data
        for ac in self.acs:
            ac.set_context_data(self._contextdata)

    @property
    def context(self):
        return self._contextdata

    @context.setter
    def context(self, value: dict):
        self._contextdata.update({self.uid: value})

    def _on_after(self):
        super(AbcContextAction, self)._on_after()
        if self._contextdata:
            ContextPersistent.persistent(self._contextdata)

    def index(self, i):
        return self.acs[i]

    # TODO 调用 on_unmount
    def removeI(self, i: int):
        if i < 0 or i >= len(self.acs): raise Exception(f"{i} is out of range")
        r = self.acs.pop(i)

        if len(self.acs) != 0:
            if i == len(self.acs) - 1:
                self.acs[i - 1]._next = r._next
            elif i == 0:
                self.acs[i + 1]._prev = r._prev
            else:
                self.acs[i - 1]._next = r._next
                self.acs[i + 1]._prev = r._prev

    def find_byL(self, condition):
        return list(filter(condition, self.acs))[0]

    def append(self, action, *args, **kwargs):
        """
        添加子 Action
        PS, 子 Action 的 contextdata 会自动覆盖为父 Action 的 contextdata
        :param action:
        :type action:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        action._parent = self
        action.on_mount()
        if len(self.acs) > 0:
            action._prev = self.acs[-1]
            self.acs[-1]._next = action
        self.acs.append(action)

    def description(self):
        return self.prop.get('description')
