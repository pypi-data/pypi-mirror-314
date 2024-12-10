from edkcore.support.enums.state_enum import StateEnum


class ActionState:
    def __init__(self):
        self._state_path: list[StateEnum] = list()
        self._pre: StateEnum = None
        self._cur: StateEnum = None

    def change_to(self, new_state: StateEnum):
        self._pre = self._cur
        self._cur = new_state
        self._state_path.append(new_state)

    @property
    def path(self): return self._state_path

    @property
    def current(self) -> StateEnum: return self._cur

    @property
    def prev(self) -> StateEnum: return self._pre

    def fail(self) -> bool:
        return StateEnum.error in self._state_path
