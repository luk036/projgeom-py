class Foo:
    def __init__(self, pt_a):
        self.a = a

    def whatisme(self):
        print(type(self))

    def dual(self):
        return float

    def print_dual(self):
        print(self.dual())


class FooBar(Foo):
    def __init__(self, pt_a):
        Foo.__init__(self, pt_a)

    def dual(self):
        return bool


if __name__ == "__main__":
    foobar = FooBar(12)
    foobar.whatisme()
    foobar.print_dual()
