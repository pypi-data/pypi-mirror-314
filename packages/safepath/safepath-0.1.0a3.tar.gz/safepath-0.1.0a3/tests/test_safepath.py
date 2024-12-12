"""Tests for the safepath package."""

import unittest
from safepath import sp, SafePath

class TestSafePath(unittest.TestCase):
    def test_basic_value_access(self):
        # Test direct value access
        self.assertEqual(sp(42)(), 42)
        self.assertIsNone(sp(None)())

    def test_attribute_access(self):
        # Test attribute access on objects
        class Person:
            def __init__(self):
                self.name = "John"
                self.age = 30

        person = Person()
        self.assertEqual(sp(person).name(), "John")
        self.assertEqual(sp(person).age(), 30)
        self.assertIsNone(sp(person).unknown_attr())
        self.assertIsNone(sp(None).any_attr())

    def test_item_access(self):
        # Test dictionary access
        data = {"name": "John", "age": 30}
        self.assertEqual(sp(data)["name"](), "John")
        self.assertEqual(sp(data)["age"](), 30)
        self.assertIsNone(sp(data)["unknown_key"]())
        self.assertIsNone(sp(None)["any_key"]())

        # Test list access
        lst = [1, 2, 3]
        self.assertEqual(sp(lst)[0](), 1)
        self.assertIsNone(sp(lst)[10]())
        self.assertIsNone(sp(None)[0]())

    def test_chaining(self):
        # Test chaining of attribute and item access
        data = {
            "user": {
                "profile": {
                    "address": {
                        "city": "New York"
                    }
                }
            }
        }
        self.assertEqual(
            sp(data)["user"]["profile"]["address"]["city"](),
            "New York"
        )
        self.assertIsNone(
            sp(data)["user"]["profile"]["nonexistent"]["field"]()
        )

    def test_nested_none(self):
        # Test handling of None in nested structures
        data = {
            "user": None
        }
        self.assertIsNone(sp(data)["user"]["any"]["path"]())

    def test_immutability(self):
        # Test that SafePath objects are immutable
        wrapper = sp(42)
        with self.assertRaises(AttributeError):
            wrapper.new_attr = "value"

    def test_repr(self):
        # Test string representation
        self.assertEqual(repr(sp(42)), "SafePath(42)")
        self.assertEqual(repr(sp(None)), "SafePath(None)")
        self.assertEqual(repr(sp("test")), "SafePath('test')")

if __name__ == '__main__':
    unittest.main()
