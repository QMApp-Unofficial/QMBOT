import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


# -----------------------------------------------------------------------------
# Storage paths
# -----------------------------------------------------------------------------

DATA_DIR = Path(os.getenv("DATA_DIR", "/data")).resolve()
BACKUP_DIR = DATA_DIR / "backups"

COINS_FILE = DATA_DIR / "coins.json"
DATA_FILE = DATA_DIR / "data.json"
WARNS_FILE = DATA_DIR / "warns.json"
MARRIAGES_FILE = DATA_DIR / "marriages.json"
SHOP_FILE = DATA_DIR / "shop.json"
MARKET_FILE = DATA_DIR / "market.json"
LOGS_FILE = DATA_DIR / "logs.json"
TASKS_FILE = DATA_DIR / "tasks.json"
CONFIG_CACHE_FILE = DATA_DIR / "config_cache.json"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def _debug_startup() -> None:
    print("[storage] =============================")
    print(f"[storage] DATA_DIR      = {DATA_DIR}")
    print(f"[storage] BACKUP_DIR    = {BACKUP_DIR}")
    print(f"[storage] COINS_FILE    = {COINS_FILE}")
    print(f"[storage] DATA_FILE     = {DATA_FILE}")
    print(f"[storage] DATA_DIR exists: {DATA_DIR.exists()}")
    if DATA_DIR.exists():
        try:
            entries = sorted(p.name for p in DATA_DIR.iterdir())
            print(f"[storage] DATA_DIR entries ({len(entries)}): {entries[:30]}")
        except Exception as e:
            print(f"[storage] Could not inspect DATA_DIR: {type(e).__name__}: {e}")
    print("[storage] =============================")


def _make_backup(path: Path) -> None:
    """
    Make a timestamped backup of an existing file before overwriting it.
    """
    try:
        if path.exists() and path.is_file():
            ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{path.stem}.{ts}.bak{path.suffix}"
            backup_path = BACKUP_DIR / backup_name
            shutil.copy2(path, backup_path)
    except Exception as e:
        print(f"[storage] Backup failed for {path.name}: {type(e).__name__}: {e}")


def _read_json(path: Path, default: Any) -> Any:
    _ensure_dirs()

    if not path.exists():
        _write_json(path, default, make_backup=False)
        return default

    try:
        with path.open("r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return default
            return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[storage] JSON decode error in {path.name}: {e}")
        bad_name = f"{path.stem}.corrupt.{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
        bad_path = BACKUP_DIR / bad_name
        try:
            shutil.copy2(path, bad_path)
            print(f"[storage] Corrupt file copied to {bad_path}")
        except Exception as copy_err:
            print(f"[storage] Failed to preserve corrupt file: {copy_err}")
        return default
    except Exception as e:
        print(f"[storage] Failed to read {path.name}: {type(e).__name__}: {e}")
        return default


def _write_json(path: Path, data: Any, make_backup: bool = True) -> None:
    """
    Atomic JSON write:
    - writes to a temp file in the same directory
    - fsyncs
    - replaces the real file in one step
    """
    _ensure_dirs()

    if make_backup:
        _make_backup(path)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(DATA_DIR),
            delete=False,
            suffix=".tmp",
        ) as tf:
            json.dump(data, tf, indent=2, ensure_ascii=False)
            tf.flush()
            os.fsync(tf.fileno())
            tmp_path = Path(tf.name)

        os.replace(tmp_path, path)
    except Exception as e:
        print(f"[storage] Failed to write {path.name}: {type(e).__name__}: {e}")
        if tmp_path and tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        raise


def _load_dict(path: Path) -> dict:
    data = _read_json(path, {})
    return data if isinstance(data, dict) else {}


def _load_list(path: Path) -> list:
    data = _read_json(path, [])
    return data if isinstance(data, list) else []


# -----------------------------------------------------------------------------
# Generic helpers
# -----------------------------------------------------------------------------

def load_json_file(filename: str, default: Any = None) -> Any:
    if default is None:
        default = {}
    return _read_json(DATA_DIR / filename, default)


def save_json_file(filename: str, data: Any) -> None:
    _write_json(DATA_DIR / filename, data)


# -----------------------------------------------------------------------------
# Coins / economy
# -----------------------------------------------------------------------------

def load_coins() -> dict:
    return _load_dict(COINS_FILE)


def save_coins(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_coins expected a dict")
    _write_json(COINS_FILE, data)


# -----------------------------------------------------------------------------
# XP / message / guild-user data
# -----------------------------------------------------------------------------

def load_data() -> dict:
    return _load_dict(DATA_FILE)


def save_data(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_data expected a dict")
    _write_json(DATA_FILE, data)


# -----------------------------------------------------------------------------
# Warns / moderation
# -----------------------------------------------------------------------------

def load_warns() -> dict:
    return _load_dict(WARNS_FILE)


def save_warns(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_warns expected a dict")
    _write_json(WARNS_FILE, data)


# -----------------------------------------------------------------------------
# Marriage / relationships
# -----------------------------------------------------------------------------

def load_marriages() -> dict:
    return _load_dict(MARRIAGES_FILE)


def save_marriages(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_marriages expected a dict")
    _write_json(MARRIAGES_FILE, data)


# -----------------------------------------------------------------------------
# Shop / market
# -----------------------------------------------------------------------------

def load_shop() -> dict:
    return _load_dict(SHOP_FILE)


def save_shop(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_shop expected a dict")
    _write_json(SHOP_FILE, data)


def load_market() -> dict:
    return _load_dict(MARKET_FILE)


def save_market(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_market expected a dict")
    _write_json(MARKET_FILE, data)


# -----------------------------------------------------------------------------
# Logs
# -----------------------------------------------------------------------------

def load_logs() -> dict:
    return _load_dict(LOGS_FILE)


def save_logs(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_logs expected a dict")
    _write_json(LOGS_FILE, data)


# -----------------------------------------------------------------------------
# Tasks / reminders
# -----------------------------------------------------------------------------

def load_tasks() -> list:
    return _load_list(TASKS_FILE)


def save_tasks(data: list) -> None:
    if not isinstance(data, list):
        raise TypeError("save_tasks expected a list")
    _write_json(TASKS_FILE, data)


# -----------------------------------------------------------------------------
# Optional config cache / misc
# -----------------------------------------------------------------------------

def load_config_cache() -> dict:
    return _load_dict(CONFIG_CACHE_FILE)


def save_config_cache(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("save_config_cache expected a dict")
    _write_json(CONFIG_CACHE_FILE, data)


# -----------------------------------------------------------------------------
# User helpers
# -----------------------------------------------------------------------------

def ensure_coin_user(user_id: int | str, starting_wallet: int = 0, starting_bank: int = 0) -> dict:
    coins = load_coins()
    uid = str(user_id)

    if uid not in coins or not isinstance(coins[uid], dict):
        coins[uid] = {
            "wallet": int(starting_wallet),
            "bank": int(starting_bank),
            "debt": 0,
        }
        save_coins(coins)

    else:
        coins[uid].setdefault("wallet", int(starting_wallet))
        coins[uid].setdefault("bank", int(starting_bank))
        coins[uid].setdefault("debt", 0)
        save_coins(coins)

    return coins[uid]


def get_balance(user_id: int | str) -> dict:
    coins = load_coins()
    uid = str(user_id)
    entry = coins.get(uid, {})
    return {
        "wallet": int(entry.get("wallet", 0)),
        "bank": int(entry.get("bank", 0)),
        "debt": int(entry.get("debt", 0)),
    }


# -----------------------------------------------------------------------------
# Init
# -----------------------------------------------------------------------------

_ensure_dirs()
_debug_startup()
