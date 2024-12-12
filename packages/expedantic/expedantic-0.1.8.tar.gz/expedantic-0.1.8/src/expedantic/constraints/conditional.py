from typing import Annotated, Any
from pydantic.fields import PydanticUndefined 
from pydantic.functional_validators import AfterValidator
from pydantic import Field

from .. import ConfigBase


def MutuallyExclusive(typ: type, default: Any = PydanticUndefined, ):
    def 

    return Annotated[typ, AfterValidator(...)]


if __name__ == "__main__":
    class Config(ConfigBase):
        a: bool = 
