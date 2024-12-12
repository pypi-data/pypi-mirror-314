import importlib
import inspect
from dataclasses import field, dataclass
from typing import Annotated, Any, Generic, TypeVar, Callable, ClassVar, get_args
from typing_extensions import Self
from types import ModuleType, new_class

# from pydantic.fields import

from pydantic_core import CoreSchema, core_schema
from pydantic import (
    BaseModel,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    TypeAdapter,
    Field,
    computed_field,
    model_validator,
    ValidationError,
    GetPydanticSchema,
)

# from pydantic.dataclasses import dataclass
from pydantic import InstanceOf
from pydantic.functional_validators import (
    BeforeValidator,
    PlainValidator,
    AfterValidator,
    WrapValidator,
)

from expedantic import ConfigBase

T = TypeVar("T")


# @dataclass
# class ModuleObjectModel(Generic[T]):
#     _type: type[T]
#     name: str
#     module: str
#     positional_arguments: list = field(default_factory=lambda: [])
#     keyword_arguments: dict[str, Any] = field(default_factory=lambda: {})

#     def get_instance(self) -> T:
#         module = importlib.import_module(self.module)
#         attr = getattr(module, self.name)

#         assert issubclass(type(attr), self._type)

#         if inspect.isclass(attr):
#             return attr(*self.positional_arguments, **self.keyword_arguments)
#         else:
#             return attr


# from expedantic import ConfigBase


# T = TypeVar("T", bound=ModuleType)


class ModuleObjectModel(BaseModel):
    # _type: type[T] = None
    name: str
    module: str
    positional_arguments: list = field(default_factory=lambda: [])
    keyword_arguments: dict[str, Any] = field(default_factory=lambda: {})
    # _type: type[T]

    # @computed_field
    # @classmethod
    # def _type(cls) -> type[T]:
    #     return cls.__orig_bases__[1]

    # @model_validator(mode="before")
    # @classmethod
    # def get_type(cls, values) -> type[T]:
    #     cls._type = get_args(cls.__orig_bases__[1])
    #     return values

    # def get_instance(self) -> T:
    #     module = importlib.import_module(self.module)
    #     attr = getattr(module, self.name)

    #     # assert issubclass(type(attr), _typ)

    #     if inspect.isclass(attr):
    #         return attr(*self.positional_arguments, **self.keyword_arguments)
    #     else:
    #         return attr

    # @staticmethod
    # def get_validator(_type: type):
    #     def get_instance(self) -> T:
    #         module = importlib.import_module(self.module)
    #         attr = getattr(module, self.name)

    #         assert issubclass(
    #             type(attr), _type
    #         ), f"{self.module}.{self.name} is not a type of {_type}"

    #         if inspect.isclass(attr):
    #             return attr(*self.positional_arguments, **self.keyword_arguments)
    #         else:
    #             return attr

    #     return get_instance

    @model_validator(mode="after")
    def get_instance(self):
        module = importlib.import_module(self.module)
        attr = getattr(module, self.name)

        # assert issubclass(type(attr), _typ)

        if inspect.isclass(attr):
            return attr(*self.positional_arguments, **self.keyword_arguments)
        else:
            return attr


# def ModuleObject(_type: type[T]):
#     return Annotated[
#         T | ModuleObjectModel, PlainValidator(ModuleObjectModel.get_validator(_type))
#     ]


ModuleObject = Annotated[
    T | ModuleObjectModel,
    Annotated[ModuleObjectModel, ...],
    BeforeValidator(ModuleObjectModel.get_instance),
    InstanceOf[T],
]


@dataclass
class ModuleObjectDict:
    name: str
    module: str
    positional_arguments: list = field(default_factory=lambda: [])
    keyword_arguments: dict[str, Any] = field(default_factory=lambda: {})

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ):
        def get_instance(d):
            module = importlib.import_module(d["module"])
            attr = getattr(module, d["name"])

            # assert issubclass(type(attr), _typ)

            if inspect.isclass(attr):
                return attr(*d["positional_arguments"], **d["keyword_arguments"])
            else:
                return attr

        from_dict_schema = core_schema.chain_schema(
            [
                core_schema.dataclass_schema(),
                core_schema.typed_dict_schema(
                    {
                        "name": core_schema.typed_dict_field(core_schema.str_schema()),
                        "module": core_schema.typed_dict_field(
                            core_schema.str_schema()
                        ),
                        "positional_arguments": core_schema.typed_dict_field(
                            core_schema.list_schema()
                        ),
                        "keyword_arguments": core_schema.typed_dict_field(
                            core_schema.dict_schema(
                                core_schema.str_schema(), core_schema.any_schema()
                            )
                        ),
                    }
                ),
                core_schema.no_info_plain_validator_function(
                    get_instance
                    # ModuleObjectModel.get_instance
                ),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_dict_schema,
            python_schema=core_schema.union_schema([from_dict_schema]),
        )


# class _ModuleObjectModelValidator:
#     @classmethod
#     def __get_pydantic_core_schema__(
#         cls, source_type: Any, handler: GetCoreSchemaHandler
#     ) -> CoreSchema:

#         from_dict_schema = core_schema.chain_schema(
#             [
#                 core_schema.typed_dict_schema(
#                     {
#                         "name": core_schema.typed_dict_field(core_schema.str_schema()),
#                         "module": core_schema.typed_dict_field(
#                             core_schema.str_schema()
#                         ),
#                         "positional_arguments": core_schema.typed_dict_field(
#                             core_schema.list_schema()
#                         ),
#                         "keyword_arguments": core_schema.typed_dict_field(
#                             core_schema.dict_schema(
#                                 core_schema.str_schema(), core_schema.any_schema()
#                             )
#                         ),
#                     }
#                 ),
#                 core_schema.no_info_plain_validator_function(
#                     ModuleObjectModel[T].get_instance
#                 ),
#             ]
#         )

#         return core_schema.json_or_python_schema(
#             json_schema=from_dict_schema,
#             python_schema=core_schema.union_schema(
#                 [core_schema.is_instance_schema(ModuleObjectModel[T]), from_dict_schema]
#             ),
#         )

#         return core_schema.no_info_before_validator_function(
#             self.get_instance, handler.generate_schema(source_type)
#         )

#     @classmethod
#     def __get_pydantic_json_schema__(
#         cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
#     ):
#         return handler(core_schema.any_schema())


# class _ModuleObjectAlias(type):
#     def __new__()
#     ...


# class ModuleObject(Any):
#     @staticmethod
#     def validate(cls, v):
#         if not isinstance(v, str):
#             raise TypeError("String required.")

#         if hasattr(cls._module, v):
#             attr = getattr(cls._module, v)
#             if cls._type is Any or isinstance(attr, cls._type):
#                 return attr
#             else:
#                 raise ValueError(f"{v} is not a type of {cls._type}.")
#         else:
#             raise ValueError(f"{v} is not a part of module {self._module}.")

#     def __class_getitem__(cls, key: tuple[ModuleType, Any] | ModuleType) -> type[str]:
#         if isinstance(key, tuple):
#             key, typ = key
#         else:
#             key, typ = key, Any

#         base_type = tuple() if typ is Any else (typ,)

#         def exec_body(ns: dict[str, Any]):
#             ns.__setitem__("_module", key)
#             ns.__setitem__("_type", typ)
#             ns.__setitem__("validate", classmethod(ModuleObject.validate))
#             # ns.__setitem__("_type", typ)

#         return new_class(
#             f"{cls.__name__}[{key.__name__}]",
#             (cls, str),
#             {},
#             exec_body,
#         )
#         # class ModuleObject(type):
#         #     _module: ModuleType = key

#         #     # def __new__(cls):
#         #     #     return new_class(
#         #     #         f"{cls.__name__}[{key.__name__}]",
#         #     #         (cls,),
#         #     #         {},
#         #     #         lambda ns: ns.__setitem__("_module", key),
#         #     #     )

#         # return ModuleObject


# class TestModuleObject(metaclass=ModuleObjectMeta): ...


# class ModuleObject(str, Generic[T]):
#     def __init__(self, module: ModuleType) -> None:
#         super().__init__()
#         self._module = module

#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v, field):
#         if not isinstance(v, str):
#             raise TypeError("string name required.")

#         if not


# class Config(ConfigBase): ...


if __name__ == "__main__":
    import math

    # # M = TestModuleObject[math]
    # M = ModuleObject[math, Callable]
    # print(M)
    # # print(M._module)
    # print(vars(M))

    # # m = ModuleObject["math"]

    # print(M.validate("sqrt"))

    # try:
    #     # math.pi
    #     FloatFromMath = ModuleObject[math, float]
    #     pi = FloatFromMath.validate("pi")
    #     assert isinstance(pi, float)
    #     sqrt = FloatFromMath.validate("sqrt")
    # except Exception as e:
    #     print(e)

    # class TestStr(str): ...

    # class Config(ConfigBase):
    #     a: Annotated[str, ModuleObject[math, float]] = "pi"
    #     b: ModuleObject[math, float] = "pi"

    # c = Config()
    # print(c)

    # FloatFromMath = Annotated[str, ModuleObjectModel("pi", "math", float)]
    # FloatFromMath = Annotated[float, _ModuleObjectModelValidator[float]]
    # FloatFromMath = ModuleObject[T]

    # class Config(ConfigBase):
    #     a: FloatFromMath
    #     b: ModuleObject[int]

    # try:
    #     c = Config(
    #         a=ModuleObjectModel(name="pi", module="math"),
    #         b=ModuleObjectModel(name="pi", module="math"),
    #     )
    # except ValidationError as e:
    #     print(e)

    # FloatFromMath = Annotated[float, ModuleObjectDict("pi", "math")]

    import pydantic_yaml

    # def model_object():
    #     return GetPydanticSchema(
    #         lambda tp, handler: core_schema.union_schema(
    #             core_schema.is_instance_schema()
    #         )
    #     )

    MOM = Annotated[T | ModuleObjectModel, ...]

    # def check

    # MOM = Annotated[T, WrapValidator()]

    class Config2(ConfigBase):
        # a: ModuleObject[ConfigBase]
        # a: FloatFromMath
        a: ModuleObjectModel | float
        b: float | ModuleObjectModel = ModuleObjectModel(name="pi", module="math")
        c: Annotated[
            float | ModuleObjectModel,
            Field(ModuleObjectModel(name="pi", module="math"), validate_default=True),
        ]
        d: float | ModuleObjectModel = 3.14
        e: float = ModuleObjectModel(name="pi", module="math")
        # f: Annotated[
        #     float,
        #     Field(ModuleObjectModel(name="pi", module="math"), validate_default=True),
        # ]
        g: MOM[float]
        h: Annotated[MOM[float], Field(2.78)]

    c = Config2(
        a=ModuleObjectModel(name="pi", module="math"),
        b=ModuleObjectModel(name="pi", module="math"),
        g=ModuleObjectModel(name="e", module="math"),
    )
    print(c)
    print(c.model_dump_json())

    # import numpy

    # ModuleObjectModel.model_validate_json('{"name": }')

    # c = Config2(a={"name": "pi", "module": "math"})
    # print(c)

    # class Config3(ConfigBase):
    #     # a: Annotated[float | ModuleObjectModel] = ModuleObjectModel(
    #     # name="pi", module="math"
    #     # )
    #     a: Annotated[float] = ModuleObjectModel(
    #         name="pi", module="math"
    #     )

    # c = Config3()
    # print(c)

    # c = pydantic_yaml.parse_yaml_raw_as(
    #     Config2, "a: {name: ConfigBase, module: expedantic}"
    # )
