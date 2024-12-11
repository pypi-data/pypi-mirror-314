from unittest import TestCase
from dataclasses import dataclass, field
from typing import List, Dict, Union, Optional, Literal

from src.rtdce import enforce
from src.rtdce.exceptions import NotDataclassException


class TestEnforce(TestCase):
    def test_enforce_not_dataclass(self):
        class Test:
            pass

        t = Test()

        self.assertRaises(NotDataclassException, lambda: enforce(t))

    def test_enforce_dataclass(self):
        @dataclass
        class Test:
            test: str

        t = Test(test=1)
        self.assertRaises(TypeError, lambda: enforce(t))

    def test_enforce_complex_type(self):
        @dataclass
        class Test:
            test: List[str]
            test1: Dict[str, int]

        t = Test(test=["Hello"], test1={"test": 123})
        enforce(t)

    def test_enforce_complex_type_failing(self):
        @dataclass
        class Test:
            test: List[str]
            test1: Dict[str, int]

        t = Test(test=[True], test1={123: 0.123})
        self.assertRaises(TypeError, lambda: enforce(t))

    def test_enforce_union(self):
        @dataclass
        class Test:
            test: Union[dict, str]

        t = Test(test="test")
        enforce(t)

        t = Test(test={})
        enforce(t)

        t = Test(test=1)
        self.assertRaises(TypeError, lambda: enforce(t))

    def test_enforce_optional(self):
        @dataclass
        class Test:
            test: Optional[str] = field(default=None)

        t = Test()

        enforce(t)

        t = Test(test="test")

        enforce(t)

        t = Test(test=1)

        self.assertRaises(TypeError, lambda: enforce(t))

    def test_enforce_literal(self):
        @dataclass
        class Test:
            test: Literal["test", "test1"]

        t = Test(test="test")
        enforce(t)

        t = Test(test="test1")
        enforce(t)

        t = Test(test="test2")
        self.assertRaises(TypeError, lambda: enforce(t))

    def test_enforce_nested(self):
        @dataclass 
        class Child:
            x: int 

        @dataclass
        class Parent:
            child: Child


        t = Parent(child={"x": 123})

        enforce(t)

        t = Parent(child={"x": "123"})

        self.assertRaises(TypeError, lambda: enforce(t))