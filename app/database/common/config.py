"""ROBERT"""
import os


class Config:
    """Database Configuration"""

    ENV = "AUTO"
    LOCAL_URL = "sqlite:///app/database/db.db"
    PGSQL_URL = os.environ.get("DB_URL", None)

    @classmethod
    def use_auto(cls):
        """Set DB Environment to AUTO"""
        cls.ENV = "AUTO"

    @classmethod
    def use_local(cls):
        """Set DB Environment to LOCAL"""
        cls.ENV = "LOCAL"

    @classmethod
    def is_local(cls) -> bool:
        """Check if DB Environment is LOCAL"""
        return cls.ENV == "LOCAL"
