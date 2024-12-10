from enum import Enum


class StateEnum(Enum):
    initing = 0
    inited = 1
    mounting = 2
    mounted = 3
    beforing = 4
    befored = 5
    executing = 6
    executed = 7
    finializing = 8
    finialized = 9
    afering = 10
    afered = 11
    success_calling = 12
    success_called = 13
    error = -1
    fail_calling = -12
    fail_called = -13
