class pdict(dict):
    def __contains__(self, item):
        if not isinstance(item, (list, tuple)):
            return super().__contains__(item)
        else:
            if len(item) == 1:
                return super().__contains__(item[0])
            if not self.__contains__(item[0]):
                return False
            child = self[item[0]]
            if not isinstance(child, dict):
                return False
            return pdict(child).__contains__(item[1:])
    
    def __getitem__(self, *args, create=False):
        k = args[0] if len(args) == 1 else args
        if not isinstance(k, list) and not isinstance(k, tuple):
            return super().__getitem__(k)

        value = self
        for field in k:
            try:
                if isinstance(value, list):
                    field = int(field)
                value = value.__getitem__(field)
            except KeyError as e:
                if not create:
                    raise e

                v = pdict({})
                value.__setitem__(field, v)
                value = value.__getitem__(field)
        return value

    def __setitem__(self, orgPath, v):
        if not isinstance(orgPath, (list, tuple)):
            return super().__setitem__(orgPath, v)

        orgPath = list(orgPath)
        parentPath = orgPath[:-1]
        overwriteField = orgPath[-1]
        parent = self[parentPath]

        if isinstance(parent, list):
            overwriteField = int(overwriteField)
        parent[overwriteField] = v

    def setdefaults(self, defaultDict):
        for key, value in pdict(defaultDict).items():
            if key in self:
                if isinstance(self[key], dict) and bool(value):
                    self[key] = pdict(self[key])
                    self[key].setdefaults(value)
            else:
                self[key] = value

    def update(self, values, path=None):
        path = path or []
        for field in values:
            value = values[field]

            if isinstance(value, dict) and field in self:
                self[field] = pdict(self[field])
                self[field].update(value)
            else:
                self[field] = value
