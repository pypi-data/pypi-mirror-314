from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    db: str
    openai_token: str
