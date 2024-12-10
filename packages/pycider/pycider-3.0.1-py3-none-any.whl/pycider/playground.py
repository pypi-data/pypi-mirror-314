from typing import Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def single_generic(a: A) -> A:
    return a


should_be_int = single_generic(1)


def double_generic(a: A, b: B) -> tuple[A, B]:
    return (a, b)


should_be_int_float = double_generic(1, 1.0)


def tripple_generic(a: A, b: B, c: C) -> list[A | B | C]:
    return [a, b, c]


should_be_list_of_int_tuple_int_float_str = tripple_generic(
    should_be_int, should_be_int_float, "test"
)


# # This works but the value is inferred. Complains about A and B not being used twice
# def do_something(a: A, b: B, c: C) -> C | None:
#     if a or b:
#         return c
#     return None


# class_value = do_something(
#     should_be_int_float, should_be_list_of_int_tuple_int_float_str, should_be_int
# )


# # Invalid Syntax
# class TestClass:
#     def do_something(self, a: A, b: B, c: C) -> C | None:
#         if a or b:
#             return c
#         return None

# # Doesn't work, unknown unknown unknown
# class TestClass(Generic[A, B, C]):
#     def do_something(self, a: A, b: B, c: C) -> C | None:
#         if a or b:
#             return C
#         return None

# test_class = TestClass()
# class_value = test_class.do_something(
#     should_be_int_float, should_be_list_of_int_tuple_int_float_str, should_be_int
# )

# Doesn't work, unknown unknown unknown
# class TestClass(Generic[A, B, C]):
#     @classmethod
#     def do_something(cls, a: A, b: B, c: C) -> C | None:
#         if a or b:
#             return c
#         return None


# class_value = TestClass.do_something(
#     1, 1.5, [2]
# )


# # This works!
# class TestClass(Generic[A, B, C]):
#     def __init__(self, a: A, b: B, c: C):
#         self.a = a
#         self.b = b
#         self.c = c

#     def do_something(self) -> C | None:
#         if self.a or self.b:  # Check truthiness of `a` and `b`
#             return self.c
#         return None

#     def another_method(self) -> tuple[A, B]:
#         """An example method that uses `A` and `B`."""
#         return self.a, self.b


# # Example usage
# instance = TestClass(
#     1, 1.5, [2]
# )  # Type variables are inferred as A=int, B=float, C=list[int]

# result = instance.do_something()  # Inferred type: list[int] | None
# other_result = instance.another_method()  # Inferred type: tuple[int, float]


# class TestClass(Generic[A, B, C]):
#     def __init__(self, pair: tuple[A, B], c: C):
#         self.pair = pair
#         self.c = c

#     def do_something(self) -> C | None:
#         if self.pair[0] or self.pair[1]:  # Check truthiness of the tuple elements
#             return self.c
#         return None

#     def another_method(self) -> tuple[A, B]:
#         """Returns the pair."""
#         return self.pair


# # Example usage
# instance = TestClass(
#     (1, 1.5), [2]
# )  # Type variables are inferred as A=int, B=float, C=list[int]

# result = instance.do_something()  # Inferred type: list[int] | None
# other_result = instance.another_method()  # Inferred type: tuple[int, float]


class TestClassA(Generic[A]):
    def create(self):
        InnerA = TypeVar("InnerA")

        class TestClassB(Generic[InnerA, B]):
            pass

            def __init__(self, b: B) -> None:
                self.b = b

        return TestClassB
