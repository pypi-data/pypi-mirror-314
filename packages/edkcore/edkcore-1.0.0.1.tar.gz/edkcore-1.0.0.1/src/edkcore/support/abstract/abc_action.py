import abc
import traceback

from edkcore.support.abstract.abc_properties import AbcProperties
from edkcore.support.action_state import ActionState
from edkcore.support.callbacks.nothing import Nothing
from edkcore.support.enums.state_enum import StateEnum


class AbcAction(abc.ABC):
    def __init__(self, prop: AbcProperties):
        self.state = ActionState()
        self.prop = prop
        self.state.change_to(StateEnum.initing)
        self._on_init()
        self.state.change_to(StateEnum.inited)

    def _on_init(self):
        """

        :return:
        :rtype:
        """
        ...

    def on_mount(self, *args, **kwargs):
        """

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def _on_before(self):
        """

        :return:
        :rtype:
        """
        ...

    def _on_unmount(self):
        """

        :return:
        :rtype:
        """
        ...

    def _on_after(self):
        """

        :return:
        :rtype:
        """
        ...

    def _on_finalize(self):
        """

        :return:
        :rtype:
        """
        ...

    def success(self):
        return Nothing()

    def failed(self):
        return Nothing()

    def execute(self):
        try:
            self.state.change_to(StateEnum.beforing)
            self._on_before()
            self.state.change_to(StateEnum.befored)
            self.state.change_to(StateEnum.executing)
            self._on_execute()
            self.state.change_to(StateEnum.executed)
            self.state.change_to(StateEnum.afering)
            self._on_after()
            self.state.change_to(StateEnum.afered)
            if type(self.success()) != Nothing:
                self.state.change_to(StateEnum.success_calling)
                self.success().call_back()
                self.state.change_to(StateEnum.success_called)

        except Exception as e:
            self.state.change_to(StateEnum.error)

            if type(self.failed()) != Nothing:
                self.state.change_to(StateEnum.fail_calling)
                self.failed().call_back()
                self.state.change_to(StateEnum.fail_called)
            self._on_error(e)
        finally:
            self.state.change_to(StateEnum.finializing)
            self._on_finalize()
            self.state.change_to(StateEnum.finialized)

    def _on_error(self, e: Exception):
        raise e
        # print(type(e))
        # 打印错误消息
        # print(e)
        # 打印完整的异常信息，包括堆栈跟踪
        # print(traceback.format_exc())

    @abc.abstractmethod
    def _on_execute(self):
        """

        :return:
        :rtype:
        """
        ...
