class ServiceContainer:

    def __init__(self):
        self.services = {}

    def add(self, name, service):
        self.services[name] = service

    def get(self, name):
        return self.services.get(name)
