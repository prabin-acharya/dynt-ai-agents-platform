class BaseAgent:
    def __init__(self, name):
        self.name = name

    def run(self, **kwargs):
        raise NotImplementedError("Agent must implement run()")
