# TODO: Make session a dict of class names and session...
# TODO: Make sessions a dict of dict of classname and sessions
# TODO: Test to make sure session and sessions aren't shared between Subclasses

class SessionManagerHook(type):
    #
    def __init__(cls, name, bases, clsdict):
        cls.session = None
        cls.sessions = {}
        super(SessionManagerHook, cls).__init__(name, bases, clsdict)

    def __getattr__(cls, item):
        sessions = cls.sessions
        if item in sessions:
            cls.set(item)
        else:
            return getattr(cls, item)


class SessionManager(object, metaclass=SessionManagerHook):
    """ Session manager """

    session = None
    sessions = {}

    @classmethod
    def create(cls, api_connector, *args, name=None, **kwargs):
        cls.session = api_connector(*args, **kwargs)
        cls._add_session(cls.session, name)

    @classmethod
    def _add_session(cls, api_connector, name):
        cls.sessions[name] = api_connector

    @classmethod
    def set(cls, name):
        sessions = cls.sessions
        cls.session = sessions[name]

    @classmethod
    def session_name(cls):
        for name, session in cls.sessions.items():
            if cls.session == session:
                return name

    @classmethod
    def close(cls):
        cls.session = None