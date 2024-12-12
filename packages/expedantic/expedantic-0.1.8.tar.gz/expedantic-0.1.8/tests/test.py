# import unittest
# from typing import Any, Literal
#
# from expedantic import ConfigBase, Field
#
#
# class TestInnerConfig(ConfigBase):
#     a: int = -1
#     b: float = -2.0
#     # req: str
#
#
# class Obj: ...
#
#
# class TestConfig(ConfigBase):
#     a: int = 1
#     b: float = 2.0
#     c: str = "3.0"
#     d: list[float] = Field(default_factory=lambda: [1.0, 2.0, 3.0])
#     e: TestInnerConfig = TestInnerConfig()
#     f: Any = "asdf"
#     g: Literal["A", "B", "C"]
#     h: list[int]
#     file: str
#     obj: Obj = Obj()
#
#
# class TestBase(ConfigBase):
#     a: int = 1
#     b: float = 2.0
#
#
# class TestChild(TestBase):
#     c: str = "c"
#
#
# # class TestSaveLoad(unittest.TestCase):
# # def test_save(self):
# # TestConfig.model_dump()
#
#
# if __name__ == "__main__":
#     # t = TestConfig()
#     # tapified = TestConfig.tapify()
#     # c = TestConfig.parse_args()
#     c = TestConfig(g="A", h=[1, 2, 3], file="test.png")
#     # TestConfig.generate_schema("test_schema.json")
#
#     from pathlib import Path
#
#     c.save_as_yaml("test.yaml")
#
#     print(c)
