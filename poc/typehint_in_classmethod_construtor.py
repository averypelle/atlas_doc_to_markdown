# -*- coding: utf-8 -*-

"""
This script demonstrates the correct way to type hint class methods that serve as constructors
in an inheritance hierarchy. The goal is to ensure that the `new` class method in the base class
and its subclasses correctly return an instance of the class itself while maintaining accurate type hints.

By leveraging `TypeVar` and `Type` from the `typing` module:
1. The base class `Base` defines a generic class method `new` that uses a type variable `T_BASE` bound to `Base`.
2. Subclasses like `Model1` and `Model2` inherit this type hint, ensuring that calling `new` on a subclass
   will return an instance of that subclass.
3. This setup provides proper static type inference and IDE autocompletion for methods specific to each subclass.

For example:
- `Model1.new()` correctly returns an instance of `Model1`, enabling access to `model1_method`.
- `Model2.new()` correctly returns an instance of `Model2`, enabling access to `model2_method`.

This pattern is ideal for scenarios where a base class provides a generic constructor-like class method
and subclasses need to customize or override it while retaining accurate type inference.
"""

import typing as T
import dataclasses

# Define a TypeVar bound to the Base class
# This ensures that the type variable represents Base or any subclass of Base
T_BASE = T.TypeVar("T_BASE", bound="Base")


@dataclasses.dataclass
class Base:
    """
    Base class with a class method `new` that acts as a constructor.

    The `new` method is type-hinted to return an instance of the calling class. This is achieved
    using the `T_BASE` type variable, which allows the return type to adapt to subclasses.
    """

    def base_method(self):
        """
        Example instance method for the base class. Subclasses can override or extend this.
        """
        pass

    @classmethod
    def new(cls: T.Type[T_BASE]) -> T_BASE:
        """
        Class method that creates a new instance of the class.

        The return type is dynamically inferred based on the subclass that calls this method,
        ensuring accurate type checking for subclass-specific methods and attributes.

        Returns:
            T_BASE: An instance of the calling class (Base or its subclass).
        """
        return cls()


@dataclasses.dataclass
class Model1(Base):
    """
    Subclass of Base that represents a specific model.

    Includes a `model1_method` to demonstrate subclass-specific functionality.
    """

    def model1_method(self):
        """
        Example instance method for Model1.
        """
        pass

    @classmethod
    def new(cls: T.Type[T_BASE]) -> T_BASE:
        """
        Overrides the `new` method from the Base class.

        This method ensures that `Model1.new()` returns an instance of `Model1`
        while preserving accurate type inference.
        """
        return super().new()


@dataclasses.dataclass
class Model2(Base):
    """
    Subclass of Base that represents another specific model.

    Includes a `model2_method` to demonstrate subclass-specific functionality.
    """

    def model2_method(self):
        """
        Example instance method for Model2.
        """
        pass

    @classmethod
    def new(cls: T.Type[T_BASE]) -> T_BASE:
        """
        Overrides the `new` method from the Base class.

        This method ensures that `Model2.new()` returns an instance of `Model2`
        while preserving accurate type inference.
        """
        return super().new()


# Example usage to demonstrate the effectiveness of type hints
model1 = Model1.new()
model1.model1_method()  # IDE and type checkers will recognize this as valid

model2 = Model2.new()
model2.model2_method()  # IDE and type checkers will recognize this as valid
