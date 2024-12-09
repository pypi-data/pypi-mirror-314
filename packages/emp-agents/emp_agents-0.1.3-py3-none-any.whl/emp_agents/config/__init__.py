import os
from contextvars import ContextVar, Token
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration for the EMP agents library"""

    # API Keys
    openai_api_key: Optional[str] = Field(
        default_factory=lambda: os.environ.get("OPENAI_API_KEY")
    )
    anthropic_api_key: Optional[str] = Field(
        default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY")
    )

    # Additional configs that can be set via yaml
    custom_settings: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_yaml(cls, yaml_path: Path | str) -> "Config":
        """Load config from a YAML file"""
        yaml_path = Path(yaml_path)
        if not yaml_path.exists():
            raise FileNotFoundError(f"YAML config file not found at {yaml_path}")

        with open(yaml_path) as f:
            yaml_config = yaml.safe_load(f)

        # Set environment variables if specified in yaml
        env_vars = yaml_config.pop("environment", {})
        for key, value in env_vars.items():
            if value is not None:
                os.environ[key] = str(value)

        # Create config instance with remaining yaml data as custom settings
        return cls(custom_settings=yaml_config)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a custom setting from the config"""
        return self.custom_settings.get(key, default)

    def update_settings(self, settings: dict[str, Any]) -> None:
        """Update custom settings"""
        self.custom_settings.update(settings)


# Context variable for config instance
_config_context: ContextVar[Optional[Config]] = ContextVar("config", default=None)


def get_config() -> Config:
    """Get the config instance from current context"""
    config = _config_context.get()
    if config is None:
        config = Config()
        _config_context.set(config)
    return config


def init_config(yaml_path: Optional[Path | str] = None) -> Config:
    """Initialize a new config instance in the current context"""
    config = Config.from_yaml(yaml_path) if yaml_path else Config()
    _config_context.set(config)
    return config


class ConfigContext:
    """Context manager for temporary config changes"""

    config: Optional[Config]
    token: Optional[Token[Config | None]]

    def __init__(self, yaml_path: Optional[Path | str] = None, **settings):
        self.config = Config.from_yaml(yaml_path) if yaml_path else Config()
        if settings:
            self.config.update_settings(settings)
        self.token = None

    def __enter__(self) -> Config:
        if self.config is None:
            raise ValueError("Config instance is None")
        self.token = _config_context.set(self.config)
        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.token is not None:
            _config_context.reset(self.token)
