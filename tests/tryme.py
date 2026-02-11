class Foo:
    def __init__(self, a: int) -> None:
        self.a: int = a

    def whatisme(self) -> None:
        print(type(self))

    def dual(self) -> type:
        return float

    @property
    def dual_type(self) -> type:
        return self.dual()

    def print_dual(self) -> None:
        print(self.dual_type)


class FooBar(Foo):
    def __init__(self, a: int) -> None:
        Foo.__init__(self, a)

    def dual(self) -> type:
        return bool


if __name__ == "__main__":
    foobar = FooBar(12)
    foobar.whatisme()
    foobar.print_dual()
