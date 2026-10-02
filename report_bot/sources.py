import json
import urllib.parse
import urllib.request

from .config import Config

UA = {"User-Agent": "report-bot/1.0"}


def fetch_json(url: str, timeout: float) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def rates_block(cfg: Config) -> str:
    data = fetch_json("https://www.cbr-xml-daily.ru/daily_json.js", cfg.timeout)
    lines = []
    for code in cfg.currencies:
        v = data["Valute"][code]
        nominal = v["Nominal"]
        value, prev = v["Value"] / nominal, v["Previous"] / nominal
        diff = value - prev
        arrow = "▲" if diff > 0 else "▼" if diff < 0 else "•"
        lines.append(f"{code}: {value:.2f} ₽ {arrow} {diff:+.2f}")
    return "💱 Курсы ЦБ\n" + "\n".join(lines)


def weather_block(cfg: Config) -> str:
    qs = urllib.parse.urlencode(
        {
            "latitude": cfg.lat,
            "longitude": cfg.lon,
            "timezone": "auto",
            "forecast_days": 1,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        }
    )
    d = fetch_json(f"https://api.open-meteo.com/v1/forecast?{qs}", cfg.timeout)["daily"]
    return (
        f"🌤 Погода, {cfg.city}\n"
        f"{d['temperature_2m_min'][0]:+.0f}…{d['temperature_2m_max'][0]:+.0f} °C, "
        f"осадки {d['precipitation_probability_max'][0]}%"
    )


def github_block(cfg: Config) -> str:
    lines = []
    for repo in cfg.github_repos:
        r = fetch_json(f"https://api.github.com/repos/{repo}", cfg.timeout)
        stars, issues = (
            f"{r['stargazers_count']:,}".replace(",", " "),
            f"{r['open_issues_count']:,}".replace(",", " "),
        )
        lines.append(
            f"{repo}: ★ {stars} · issues {issues} · push {r['pushed_at'][:10]}"
        )
    return "🐙 GitHub\n" + "\n".join(lines)


# имя -> функция; порядок задаёт порядок блоков в отчёте
SOURCES = {
    "rates": rates_block,
    "weather": weather_block,
    "github": github_block,
}
