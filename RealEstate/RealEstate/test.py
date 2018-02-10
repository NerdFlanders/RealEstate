
class test:
    def __foo(self):
        print("helper function")

    def boo(self):
        self.__foo()

t = test()
t.boo()