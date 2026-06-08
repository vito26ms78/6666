class TranslationLock:

    def __init__(self):
        self.locked = {}

    def get(self, source):

        return self.locked.get(source)

    def set(self, source, translated):

        self.locked[source] = translated

    def resolve(self, source):

        return self.locked.get(source)
