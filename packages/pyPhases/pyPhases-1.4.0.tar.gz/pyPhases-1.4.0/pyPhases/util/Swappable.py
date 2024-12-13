class Swappable:
    useClass: "Swappable" = None
    
    @classmethod
    def getInstance(cls, *args, **kwargs):
        if cls.useClass is None:
            return cls(*args, **kwargs)
        return cls.useClass(*args, **kwargs)
    
    @classmethod
    def setClass(cls, dataManipulationClass):
        cls.useClass = dataManipulationClass