from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "blk-hacking-ind-micro-savings"
    version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 5477
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


settings = Settings()
