from typing import Optional

from pydantic import BaseSettings
from pydantic import Field
from pydantic import validator


class Settings(BaseSettings):
    use_hosted_auth: bool = Field(default=False, env="SUPERWISE_USE_HOSTED_AUTH")
    hosted_auth_url: str = Field(default="https://auth.managed.superwise.ai", env="SUPERWISE_HOSTED_AUTH_URL")
    client_id: str = Field(..., env="SUPERWISE_CLIENT_ID")
    client_secret: str = Field(..., env="SUPERWISE_CLIENT_SECRET")
    api_host: str = Field(default="https://api.superwise.ai", env="SUPERWISE_API_HOST")
    auth_host: str = Field(default="https://authentication.superwise.ai", env="SUPERWISE_AUTH_HOST")
    auth_endpoint: str = Field(default="/identity/resources/auth/v1/api-token", env="SUPERWISE_AUTH_ENDPOINT")
    auth_url: Optional[str] = Field(default=None)

    @validator("auth_host", pre=True)
    def check_if_hosted(cls, v, values):
        if values.get("use_hosted_auth"):
            return values["hosted_auth_url"]

        return v

    @validator("auth_url")
    def build_auth_url(cls, v, values):
        return f"{values['auth_host']}{values['auth_endpoint']}"

    class Config:
        extra = "ignore"
