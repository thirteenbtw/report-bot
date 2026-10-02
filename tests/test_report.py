from datetime import datetime

from report_bot import sources
from report_bot.config import Config
from report_bot.report import build_report

CFG = Config("", "", "Москва", 55.75, 37.62, ("USD",), ("a/b",), 5)
NOW = datetime(2026, 10, 2)


def test_all_sources_ok():
    text = build_report(CFG, NOW, {"a": lambda c: "A", "b": lambda c: "B"})
    assert text == "📊 Сводка за 02.10.2026\n\nA\n\nB"


def test_failed_source_does_not_break_report():
    def boom(c):
        raise TimeoutError

    text = build_report(CFG, NOW, {"a": lambda c: "A", "b": boom})
    assert "A" in text and "⚠️ Не получилось: b: TimeoutError" in text


def test_rates_block(monkeypatch):
    fake = {"Valute": {"USD": {"Nominal": 1, "Value": 80.0, "Previous": 79.5}}}
    monkeypatch.setattr(sources, "fetch_json", lambda url, t: fake)
    assert sources.rates_block(CFG) == "💱 Курсы ЦБ\nUSD: 80.00 ₽ ▲ +0.50"


def test_github_block(monkeypatch):
    fake = {"stargazers_count": 1234, "open_issues_count": 5, "pushed_at": "2026-10-01T10:00:00Z"}
    monkeypatch.setattr(sources, "fetch_json", lambda url, t: fake)
    assert "★ 1 234" in sources.github_block(CFG)
