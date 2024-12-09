from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Environment(BaseSettings):
    region: Optional[str] = Field(default="us-east-1", alias="REGION")


env = Environment()
