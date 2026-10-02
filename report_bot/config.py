import os
from dataclasses import dataclass


def load_dotenv(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


@dataclass(frozen=True)
class Config:
    bot_token: str
    chat_id: str
    city: str
    lat: float
    lon: float
    currencies: tuple[str, ...]
    github_repos: tuple[str, ...]
    timeout: float

    @classmethod
    def from_env(cls) -> "Config":
        def csv(name: str, default: str) -> tuple[str, ...]:
            return tuple(x.strip() for x in os.getenv(name, default).split(",") if x.strip())

        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            chat_id=os.getenv("CHAT_ID", ""),
            city=os.getenv("CITY", "Москва"),
            lat=float(os.getenv("LAT", "55.75")),
            lon=float(os.getenv("LON", "37.62")),
            currencies=csv("CURRENCIES", "USD,EUR,CNY"),
            github_repos=csv("GITHUB_REPOS", "python/cpython"),
            timeout=float(os.getenv("HTTP_TIMEOUT", "10")),
        )
