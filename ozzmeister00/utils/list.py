

class defaultlist(list):
    """
    A class that will automatically populate itself with values
    if accessing or setting indexes that are outside of its 
    current size
    """
    def __init__(self, cls, *args, **kwargs):
        """
        :param Class cls: the default class with which to instantiate new values
        """
        super(defaultlist, self).__init__(*args, **kwargs)
        self._cls = cls

    def _fill(self, index):
        while len(self) <= index:
            self.append(self._cls())

    def __getitem__(self, index):
        self._fill(index)
        return super(defaultlist, self).__getitem__(index)

    def __setitem__(self, index, value):
        self._fill(index)
        return super(defaultlist, self).__setitem__(index, value)


class DefaultIndexList(defaultlist):
    """
    Override the functionality of defaultlist to pass
    the index we're appending to the fill function
    """
    def __init__(self):
        super(DefaultIndexList, self).__init__(int)

    def _fill(self, index):
        while len(self) <= index:
            self.append(self._cls(index))
