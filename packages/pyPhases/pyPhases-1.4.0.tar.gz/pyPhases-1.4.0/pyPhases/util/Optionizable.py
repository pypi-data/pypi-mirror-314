from ..util.Logger import classLogger


class MissingOption(Exception):
    pass


@classLogger
class Optionizable:
    options = {}

    def __init__(self, options=None):
        options = options or {}
        self.options = self.initialOptions()

        for key, val in options.items():
            self.options[key] = val

    def getOption(self, name):
        if name not in self.options:
            raise MissingOption("The option '" + name + "' is missing")

        return self.options[name]

    def initialOptions(self, defaultOptions=None):
        return {}
