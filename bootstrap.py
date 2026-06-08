class Bootstrap:

    def __init__(self):
        self.modules = {}

    def register(self, name, obj):
        self.modules[name] = obj

    def get(self, name):
        return self.modules.get(name)
