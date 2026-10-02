import argparse
import sys
import time

from .config import Config, load_dotenv
from .report import build_report
from .telegram import send_message


def main() -> int:
    ap = argparse.ArgumentParser(prog="report_bot", description="Сводка из нескольких источников в Telegram")
    ap.add_argument("--dry-run", action="store_true", help="напечатать отчёт, ничего не отправляя")
    ap.add_argument("--every", type=int, metavar="SEC", help="для теста: повторять каждые SEC секунд (Ctrl+C — стоп)")
    args = ap.parse_args()

    load_dotenv()
    cfg = Config.from_env()

    if not args.dry_run and (not cfg.bot_token or not cfg.chat_id):
        print("Задайте BOT_TOKEN и CHAT_ID в .env (или запустите с --dry-run)", file=sys.stderr)
        return 2

    try:
        while True:
            text = build_report(cfg)
            if args.dry_run:
                print(text)
            else:
                send_message(cfg.bot_token, cfg.chat_id, text, cfg.timeout)
                print("Отправлено", flush=True)
            if not args.every:
                return 0
            time.sleep(args.every)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
