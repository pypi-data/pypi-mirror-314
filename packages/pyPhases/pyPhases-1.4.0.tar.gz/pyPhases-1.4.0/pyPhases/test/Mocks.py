def OverwriteConfig(*updateArgs, **updateKwargs):
    def wrapper(func):
        def inner(self, *args, **kwargs):
            for updateDict in updateArgs:
                self.project.config.update(updateDict)
            self.project.config.update(updateKwargs)
            return func(self, *args, **kwargs)

        return inner

    return wrapper
