class TwoD(list):
    defaultClass = None

    def __init__(self, *argv):
        if not isinstance(argv[0], self.defaultClass):
            argv = [self.defaultClass(arg) for arg in argv]

        super(TwoD, self).__init__(argv)


class Int2(TwoD):
    defaultClass = int


a = Int2('3', '4')

print(a)

