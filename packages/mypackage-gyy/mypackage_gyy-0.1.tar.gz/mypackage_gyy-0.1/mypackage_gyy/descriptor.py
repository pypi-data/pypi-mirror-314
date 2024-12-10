# mypackage/descriptor.py

import math

# ShowAccess descriptor implementation


class ShowAccess:
    def __set_name__(self, owner, name):
        # Automatically get the name of the attribute it's managing
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__.get(self.name)
        print(f"Get {self.name} = {value}")
        return value

    def __set__(self, instance, value):
        print(f"Set {self.name} = {value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        value = instance.__dict__.get(self.name)
        print(f"Delete {self.name} = {value}")
        del instance.__dict__[self.name]

# Base class for debug objects


class DebugObject:
    pass

# Circle class using the ShowAccess descriptor


class Circle(DebugObject):
    radius = ShowAccess()

    def __init__(self, radius):
        self.radius = radius  # The descriptor will handle this

    @property
    def area(self):
        return math.pi * self.radius ** 2

# Rectangle class using the ShowAccess descriptor for multiple attributes


class Rectangle(DebugObject):
    a = ShowAccess()
    b = ShowAccess()

    def __init__(self, a, b):
        self.a = a  # The descriptor will handle this
        self.b = b  # The descriptor will handle this

    @property
    def area(self):
        return self.a * self.b

    @property
    def perimeter(self):
        return 2 * (self.a + self.b)

# Square class, inheriting from Rectangle


class Square(Rectangle):
    def __init__(self, a):
        super().__init__(a, a)  # Initialize Rectangle with both a and b as 'a'


# Adding the main guard for testing the classes
if __name__ == "__main__":
    # Test with Circle
    print("Testing Circle class:")
    c = Circle(100)
    c.area  # Access the area, will use radius
    del c.radius  # Delete the radius attribute
    print("\n")

    # Test with Rectangle
    print("Testing Rectangle class:")
    r = Rectangle(10, 20)
    print('Area:', r.area)  # Calculate and print the area
    print('Perimeter:', r.perimeter)  # Calculate and print the perimeter
    del r.a  # Delete one of the attributes
    print("\n")

    # Test with Square
    print("Testing Square class:")
    s = Square(10)
    print('Area:', s.area)  # Calculate and print the area
    print('Perimeter:', s.perimeter)  # Calculate and print the perimeter
    del s.a  # Delete one of the attributes

