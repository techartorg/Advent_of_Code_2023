class A(object):
    SOME_VAR = 'a'

    def a(self):
        print(self.SOME_VAR)

a = A()
a.a()
A.SOME_VAR = 'b'
a.a()