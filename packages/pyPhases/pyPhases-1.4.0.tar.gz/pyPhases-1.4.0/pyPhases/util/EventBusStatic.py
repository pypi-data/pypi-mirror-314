class EventBusStatic:
    eventMap = {}

    @classmethod
    def on(cls, eventName, function):
        if eventName not in cls.eventMap:
            cls.eventMap[eventName] = []
        cls.eventMap[eventName].append(function)

    @classmethod
    def once(cls, eventName, function):
        if eventName not in cls.eventMap:
            cls.eventMap[eventName] = []

        add = True
        for cb in cls.eventMap[eventName]:
            if cb.__qualname__ == function.__qualname__:
                add = False
        if add:
            cls.eventMap[eventName].append(function)

    @classmethod
    def trigger(cls, eventName, *args):
        if eventName not in cls.eventMap:
            return
        for f in cls.eventMap[eventName]:
            f(*args)
