from edkcore.support.abstract.abc_subscriber import AbcSubscriber


class Publisher:
    def __init__(self):
        self.subscribers: list[AbcSubscriber] = list()

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def notify_all(self, *args, **kwargs):
        """
        通知所有的 Subscriber
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        for sub in self.subscribers:
            sub.update(*args, **kwargs)

    def notify(self, condition, *args, **kwargs):
        """
        指定满足条件的 subscriber 更新
        :param condition: lambda 表达式
        :type condition:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        for s in filter(condition, self.subscribers):
            s.update(*args, **kwargs)
