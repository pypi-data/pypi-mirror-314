def data_getter_root(self, name, default=None):
    try:
        return self.data[name]
    except KeyError:
        self.data[name] = default
        return self.data[name]


def data_setter_root(self, name, value):
    self.data[name] = value
