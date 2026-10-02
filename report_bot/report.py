from datetime import datetime

from .config import Config
from .sources import SOURCES


def build_report(cfg: Config, now: datetime | None = None, sources=SOURCES) -> str:
    now = now or datetime.now()
    blocks, failed = [], []
    for name, fn in sources.items():
        try:
            blocks.append(fn(cfg))
        except Exception as e:  # сеть, формат ответа — не важно, отчёт идёт дальше
            failed.append(f"{name}: {type(e).__name__}")
    text = f"📊 Сводка за {now:%d.%m.%Y}\n\n" + "\n\n".join(blocks)
    if failed:
        text += "\n\n⚠️ Не получилось: " + ", ".join(failed)
    return text
