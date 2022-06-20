from dataclasses import dataclass

from environs import Env


@dataclass
class AliConfig:
    login: str
    password: str


@dataclass
class Config:
    aliexpress: AliConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        aliexpress=AliConfig(
            login=env.str('LOGIN'),
            password=env.str('PASSWORD')
        )
    )
