from pathlib import Path
from typing import Annotated, Literal
from expedantic import ConfigBase, Field


class Config(ConfigBase):
    algorithm: Literal["TRPO", "PPO", "SAC", "TD3"] = "TRPO"
    target_kl: Annotated[
        float,
        Field(
            title="Target Kullback-Leibler divergence between updates.",
            description="Should be small for stability. Values like 0.01, 0.05.",
            gt=0.0,
        ),
    ] = 0.01


config = Config()
Path("configs").mkdir(exist_ok=True)
config.save_as_yaml("configs/config.yaml")
Config.generate_schema("schemas/config_schema.json")
