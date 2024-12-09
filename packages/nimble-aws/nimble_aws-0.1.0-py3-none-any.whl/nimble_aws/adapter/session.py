from aiobotocore.session import get_session


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Session(metaclass=Singleton):
    
    def __init__(self):
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = get_session()
        return self._session