"""Asynchronous Boomclaw SDK client using ``httpx``."""

from __future__ import annotations

import json
import asyncio
from dataclasses import asdict
from typing import Any

import httpx

from .auth import compute_signature, current_timestamp, verify_webhook_signature
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


class BoomclawAPIError(Exception):
    """Raised when the Boomclaw API returns a non-2xx response."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class AsyncBoomclawSDK:
    """Asynchronous client for the Boomclaw External Game SDK.

    Parameters
    ----------
    game_secret:
        The HMAC secret assigned to the game.
    base_url:
        Root URL of the Boomclaw platform (no trailing slash).
    timeout:
        Request timeout in seconds.
    max_retries:
        Maximum number of retry attempts for 5xx errors.
    """

    def __init__(
        self,
        game_secret: str,
        base_url: str,
        timeout: float = 10.0,
        max_retries: int = 3,
    ) -> None:
        self._secret = game_secret
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncBoomclawSDK:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self, token: str, method: str, path: str, body: str = "") -> dict[str, str]:
        ts = current_timestamp()
        sig = compute_signature(self._secret, method, path, ts, body)
        return {
            "Authorization": f"Bearer {token}",
            "X-Boomclaw-Signature": sig,
            "X-Boomclaw-Timestamp": ts,
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        path: str,
        token: str,
        *,
        json_body: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        url = f"{self._base_url}{path}"
        body_str = json.dumps(json_body, separators=(",", ":")) if json_body else ""
        headers = self._headers(token, method, path, body_str)

        last_exc: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                resp = await self._client.request(
                    method,
                    url,
                    headers=headers,
                    content=body_str.encode("utf-8") if body_str else None,
                    params=params,
                )

                if resp.status_code >= 500 and attempt < self._max_retries:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue

                if resp.status_code >= 400:
                    detail = resp.text
                    try:
                        detail = resp.json().get("detail", detail)
                    except Exception:
                        pass
                    raise BoomclawAPIError(resp.status_code, detail)

                return resp.json()

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue
                raise

        raise last_exc  # type: ignore[misc]

    # ------------------------------------------------------------------
    # Core endpoints
    # ------------------------------------------------------------------

    async def get_session(self, token: str) -> SessionInfo:
        """Retrieve the current session information."""
        data = await self._request("GET", "/api/sdk/session", token)
        player = PlayerInfo(**data["player"])
        lobster = LobsterInfo(**data["lobster"]) if data.get("lobster") else None
        return SessionInfo(
            session_id=data["session_id"],
            game_id=data["game_id"],
            player=player,
            lobster=lobster,
        )

    async def charge(
        self,
        token: str,
        amount: int,
        item_key: str,
        description: str = "",
    ) -> ChargeResult:
        """Charge coins from the player's balance."""
        data = await self._request("POST", "/api/sdk/charge", token, json_body={
            "amount": amount,
            "item_key": item_key,
            "description": description,
        })
        return ChargeResult(
            success=data["success"],
            balance=data.get("balance"),
            developer_share=data.get("developer_share"),
            platform_burn=data.get("platform_burn"),
            reason=data.get("reason"),
        )

    async def save(self, token: str, key: str, value: dict) -> dict:
        """Save game state to the platform."""
        return await self._request("POST", "/api/sdk/save", token, json_body={
            "key": key,
            "value": value,
        })

    async def load(self, token: str, key: str) -> dict:
        """Load game state from the platform."""
        return await self._request("GET", "/api/sdk/load", token, params={"key": key})

    async def end_game(self, token: str, result: dict | None = None) -> dict:
        """Signal that the game session has ended."""
        return await self._request("POST", "/api/sdk/end", token, json_body={
            "result": result,
        })

    # ------------------------------------------------------------------
    # Leaderboard
    # ------------------------------------------------------------------

    async def submit_score(
        self,
        token: str,
        score: int,
        metadata: dict | None = None,
    ) -> SubmitScoreResult:
        """Submit a score to the leaderboard."""
        data = await self._request("POST", "/api/sdk/leaderboard/submit", token, json_body={
            "score": score,
            "metadata": metadata,
        })
        return SubmitScoreResult(
            success=data["success"],
            rank=data["rank"],
            is_personal_best=data["is_personal_best"],
            previous_best=data.get("previous_best"),
        )

    async def get_leaderboard(
        self,
        token: str,
        period: str = "all_time",
        limit: int = 10,
        offset: int = 0,
    ) -> LeaderboardResult:
        """Fetch leaderboard entries."""
        data = await self._request("GET", "/api/sdk/leaderboard", token, params={
            "period": period,
            "limit": limit,
            "offset": offset,
        })
        entries = [LeaderboardEntry(**e) for e in data["entries"]]
        return LeaderboardResult(
            period=data["period"],
            period_key=data["period_key"],
            entries=entries,
            my_rank=data.get("my_rank"),
            my_score=data.get("my_score"),
            total_players=data["total_players"],
        )

    # ------------------------------------------------------------------
    # Achievements
    # ------------------------------------------------------------------

    async def register_achievements(
        self,
        token: str,
        achievements: list[AchievementDef],
    ) -> dict:
        """Register achievement definitions for the game."""
        return await self._request("POST", "/api/sdk/achievement/register", token, json_body={
            "achievements": [asdict(a) for a in achievements],
        })

    async def unlock_achievement(self, token: str, achievement_key: str) -> UnlockResult:
        """Unlock an achievement for the current player."""
        data = await self._request("POST", "/api/sdk/achievement/unlock", token, json_body={
            "achievement_key": achievement_key,
        })
        return UnlockResult(
            success=data["success"],
            achievement=data.get("achievement"),
            already_unlocked=data["already_unlocked"],
            total_points=data["total_points"],
        )

    async def get_achievements(self, token: str) -> AchievementsResult:
        """Get all achievements and their status for the current player."""
        data = await self._request("GET", "/api/sdk/achievements", token)
        achievements = [AchievementInfo(**a) for a in data["achievements"]]
        return AchievementsResult(
            achievements=achievements,
            total_points=data["total_points"],
            total_unlocked=data["total_unlocked"],
            total_available=data["total_available"],
        )

    # ------------------------------------------------------------------
    # Webhook verification
    # ------------------------------------------------------------------

    @staticmethod
    def verify_webhook_signature(secret: str, headers: dict, body: str) -> bool:
        """Verify an incoming webhook request signature.

        Parameters
        ----------
        secret:
            The webhook secret for your game.
        headers:
            Request headers (dict). Must contain ``X-Boomclaw-Signature``,
            ``X-Boomclaw-Event``, and ``X-Boomclaw-Timestamp``.
        body:
            Raw request body as a string.
        """
        return verify_webhook_signature(secret, headers, body)
