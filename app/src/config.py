from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    アプリケーション設定。
    環境変数または .env.local ファイルから値を読み込む。
    """

    # DynamoDB
    dynamodb_endpoint_url: str | None = None

    # AWS
    aws_default_region: str = "us-east-1"
    aws_access_key_id: str = "dummy"
    aws_secret_access_key: str = "dummy"

    # App
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env.local", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    設定オブジェクトのシングルトンを取得する。
    lru_cacheにより、一度読み込んだ設定はキャッシュされる。
    """
    return Settings()
