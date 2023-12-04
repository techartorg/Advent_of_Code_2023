



class A(int):
    def __new__(cls, v, l):
        return  super(A, cls).__new__(cls, v)

    def __init__(self, v, l):
        super(A, self).__init__()
        self.l = l  

l = ['a', 'b']
a = A(1, l)

print(a + 1)