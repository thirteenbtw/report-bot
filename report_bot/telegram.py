import json
import urllib.request


def send_message(token: str, chat_id: str, text: str, timeout: float = 10) -> None:
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=json.dumps({"chat_id": chat_id, "text": text}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if not json.load(resp).get("ok"):
            raise RuntimeError("Telegram вернул ok=false")
