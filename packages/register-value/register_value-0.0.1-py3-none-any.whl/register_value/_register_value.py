class RegisterValue(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(RegisterValue, '_instance'):
            RegisterValue._instance = object.__new__(cls)
        return RegisterValue._instance

    def register(self, name, value):
        setattr(self, name, value)

    def get(self, name):
        return getattr(self, name)