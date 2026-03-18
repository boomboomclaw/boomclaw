"""Response models for the Boomclaw SDK."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlayerInfo:
    """Player information returned in a session."""

    id: int
    name: str
    coins: int


@dataclass
class LobsterInfo:
    """Lobster (pet) information returned in a session."""

    id: int
    name: str
    level: int
    stats: dict


@dataclass
class SessionInfo:
    """Session details returned by ``get_session``."""

    session_id: str
    game_id: int
    player: PlayerInfo
    lobster: LobsterInfo | None


@dataclass
class ChargeResult:
    """Result of a coin charge operation."""

    success: bool
    balance: int | None = None
    developer_share: int | None = None
    platform_burn: int | None = None
    reason: str | None = None


@dataclass
class SubmitScoreResult:
    """Result of submitting a leaderboard score."""

    success: bool
    rank: int
    is_personal_best: bool
    previous_best: int | None


@dataclass
class LeaderboardEntry:
    """A single row in a leaderboard."""

    rank: int
    player_id: int
    player_name: str
    score: int
    metadata: dict | None


@dataclass
class LeaderboardResult:
    """Paginated leaderboard response."""

    period: str
    period_key: str
    entries: list[LeaderboardEntry]
    my_rank: int | None
    my_score: int | None
    total_players: int


@dataclass
class AchievementDef:
    """Definition used when registering achievements."""

    key: str
    name: str
    description: str
    points: int = 10
    hidden: bool = False


@dataclass
class AchievementInfo:
    """Achievement status for a player."""

    key: str
    name: str
    description: str
    points: int
    unlocked: bool
    unlocked_at: str | None
    hidden: bool


@dataclass
class UnlockResult:
    """Result of unlocking an achievement."""

    success: bool
    achievement: dict | None
    already_unlocked: bool
    total_points: int


@dataclass
class AchievementsResult:
    """Full achievement list for a player."""

    achievements: list[AchievementInfo]
    total_points: int
    total_unlocked: int
    total_available: int
