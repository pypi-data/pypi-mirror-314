# https://docs.pydantic.dev/latest/concepts/models/#private-model-attributes
import random
from pydantic import PrivateAttr

from expedantic import ConfigBase


class Config(ConfigBase):
    _my_private_setting: bool = False
    _private_seed: int = PrivateAttr(
        default_factory=lambda: random.randint(0, 2**32 - 1)
    )
    public_setting: str = "This is PUBLIC"


if __name__ == "__main__":
    # You can attain the private setting with the parser.
    config = Config.parse_args()

    # The private setting will not be contained in the config instance.
    print(config.model_dump())
    """
    {'public_setting': 'This is PUBLIC'}
    """
