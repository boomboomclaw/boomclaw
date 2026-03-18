"""Boomclaw External Game SDK for Python.

Quickstart::

    from boomclaw_sdk import BoomclawSDK

    sdk = BoomclawSDK(game_secret="...", base_url="https://boomclaw.com")
    session = sdk.get_session(token)
    print(session.player.name)

For async usage::

    from boomclaw_sdk import AsyncBoomclawSDK

    async with AsyncBoomclawSDK(game_secret="...", base_url="https://boomclaw.com") as sdk:
        session = await sdk.get_session(token)
"""

from .client import BoomclawSDK, BoomclawAPIError
from .types import (
    AchievementDef,
    AchievementInfo,
    AchievementsResult,
    ChargeResult,
    LeaderboardEntry,
    LeaderboardResult,
    LobsterInfo,
    PlayerInfo,
    SessionInfo,
    SubmitScoreResult,
    UnlockResult,
)

# Lazy import for async client to avoid requiring httpx at import time.
_async_loaded = False


def __getattr__(name: str):  # noqa: N807
    global _async_loaded
    if name == "AsyncBoomclawSDK" and not _async_loaded:
        from .async_client import AsyncBoomclawSDK as _Async

        globals()["AsyncBoomclawSDK"] = _Async
        _async_loaded = True
        return _Async
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # Clients
    "BoomclawSDK",
    "AsyncBoomclawSDK",
    "BoomclawAPIError",
    # Types
    "AchievementDef",
    "AchievementInfo",
    "AchievementsResult",
    "ChargeResult",
    "LeaderboardEntry",
    "LeaderboardResult",
    "LobsterInfo",
    "PlayerInfo",
    "SessionInfo",
    "SubmitScoreResult",
    "UnlockResult",
]
