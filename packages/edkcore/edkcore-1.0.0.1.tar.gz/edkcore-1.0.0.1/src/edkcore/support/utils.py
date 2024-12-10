import importlib

class_loader_cache = dict()
import threading

lock = threading.Lock()


def class_loader(class_path: str):
    """
    因为加了线程锁，为了避免速度慢，所以增加缓存，如果已经存在则直接从缓存中获取,绕过线程锁
    :param class_path:
    :type class_path:
    :return:
    :rtype:
    """
    clazz = class_loader_cache.get(class_path)
    if not clazz:
        sync_class_loader(class_path)
        return class_loader_cache.get(class_path)
    else:
        return clazz


def sync_class_loader(class_path):
    """
    为了避免多线程的时候造成数据错误
    :param class_path:
    :type class_path:
    :return:
    :rtype:
    """
    with lock:
        pkg, clazz_name = ".".join(class_path.split(".")[0:-1]), class_path.split(".")[-1]
        module = importlib.import_module(pkg)
        entry_clazz = getattr(module, clazz_name)
        class_loader_cache[class_path] = entry_clazz


def new_class(clazz, *args, **kwargs):
    if type(clazz) == str:
        return class_loader(class_path=clazz)(*args, **kwargs)
    else:
        return clazz(*args, **kwargs)
