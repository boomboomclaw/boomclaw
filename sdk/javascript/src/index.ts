import { createHmac, timingSafeEqual } from "node:crypto";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface BoomclawSDKOptions {
  /** 64-character hex HMAC key issued to the game developer. */
  gameSecret: string;
  /** Base URL of the Boomclaw platform, e.g. "https://boomclaw.com". */
  baseUrl: string;
  /** Per-request timeout in milliseconds. Default: 10 000. */
  timeout?: number;
  /** Maximum number of retry attempts on 5xx errors. Default: 3. */
  maxRetries?: number;
}

// -- Session ----------------------------------------------------------------

export interface PlayerInfo {
  id: string;
  name: string;
  coins: number;
}

export interface LobsterInfo {
  id: string;
  name: string;
  level: number;
  stats: Record<string, unknown>;
}

export interface SessionInfo {
  session_id: string;
  game_id: string;
  player: PlayerInfo;
  lobster: LobsterInfo | null;
}

// -- Charge -----------------------------------------------------------------

export interface ChargeParams {
  amount: number;
  itemKey: string;
  description?: string;
}

export interface ChargeResult {
  success: boolean;
  balance?: number;
  developer_share?: number;
  platform_burn?: number;
  reason?: string;
}

// -- Save / Load ------------------------------------------------------------

export interface SaveResult {
  success: true;
}

export interface LoadResult {
  key: string;
  value: unknown | null;
}

// -- End Game ---------------------------------------------------------------

export interface EndGameResult {
  success: true;
  session_id: string;
}

// -- Leaderboard ------------------------------------------------------------

export interface SubmitScoreParams {
  score: number;
  metadata?: Record<string, unknown>;
}

export interface SubmitScoreResult {
  success: boolean;
  rank: number;
  is_personal_best: boolean;
  previous_best: number | null;
}

export type LeaderboardPeriod = "all_time" | "weekly" | "daily";

export interface LeaderboardParams {
  period?: LeaderboardPeriod;
  limit?: number;
  offset?: number;
}

export interface LeaderboardEntry {
  rank: number;
  player_id: string;
  player_name: string;
  score: number;
  achieved_at: string;
}

export interface LeaderboardResult {
  period: LeaderboardPeriod;
  period_key: string;
  entries: LeaderboardEntry[];
  my_rank: number | null;
  my_score: number | null;
  total_players: number;
}

// -- Achievements -----------------------------------------------------------

export interface AchievementDef {
  key: string;
  name: string;
  description: string;
  points?: number;
  hidden?: boolean;
}

export interface UnlockResult {
  success: boolean;
  achievement: string;
  already_unlocked: boolean;
  total_points: number;
}

export interface AchievementStatus {
  key: string;
  name: string;
  description: string;
  points: number;
  hidden: boolean;
  unlocked: boolean;
  unlocked_at: string | null;
}

export interface AchievementsResult {
  achievements: AchievementStatus[];
  total_points: number;
  total_unlocked: number;
  total_available: number;
}

export interface RegisterAchievementsResult {
  success: true;
  count: number;
}

// -- Webhook ----------------------------------------------------------------

export interface WebhookHeaders {
  "x-boomclaw-event": string;
  "x-boomclaw-timestamp": string;
  "x-boomclaw-signature": string;
}

// ---------------------------------------------------------------------------
// SDK Errors
// ---------------------------------------------------------------------------

export class BoomclawError extends Error {
  public readonly status: number;
  public readonly body: unknown;

  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = "BoomclawError";
    this.status = status;
    this.body = body;
  }
}

export class BoomclawTimeoutError extends Error {
  constructor(url: string, timeoutMs: number) {
    super(`Request to ${url} timed out after ${timeoutMs}ms`);
    this.name = "BoomclawTimeoutError";
  }
}

// ---------------------------------------------------------------------------
// BoomclawSDK
// ---------------------------------------------------------------------------

export class BoomclawSDK {
  private readonly gameSecret: string;
  private readonly baseUrl: string;
  private readonly timeout: number;
  private readonly maxRetries: number;

  constructor(options: BoomclawSDKOptions) {
    if (!options.gameSecret || options.gameSecret.length !== 64) {
      throw new Error("gameSecret must be a 64-character hex string");
    }
    if (!options.baseUrl) {
      throw new Error("baseUrl is required");
    }

    this.gameSecret = options.gameSecret;
    this.baseUrl = options.baseUrl.replace(/\/+$/, "");
    this.timeout = options.timeout ?? 10_000;
    this.maxRetries = options.maxRetries ?? 3;
  }

  // ---- Core endpoints -----------------------------------------------------

  async getSession(token: string): Promise<SessionInfo> {
    return this.request<SessionInfo>("GET", "/api/sdk/session", token);
  }

  async charge(token: string, params: ChargeParams): Promise<ChargeResult> {
    return this.request<ChargeResult>("POST", "/api/sdk/charge", token, {
      amount: params.amount,
      item_key: params.itemKey,
      description: params.description,
    });
  }

  async save(
    token: string,
    key: string,
    value: Record<string, unknown>,
  ): Promise<SaveResult> {
    return this.request<SaveResult>("POST", "/api/sdk/save", token, {
      key,
      value,
    });
  }

  async load(token: string, key: string): Promise<LoadResult> {
    return this.request<LoadResult>(
      "GET",
      `/api/sdk/load?key=${encodeURIComponent(key)}`,
      token,
    );
  }

  async endGame(
    token: string,
    result?: Record<string, unknown>,
  ): Promise<EndGameResult> {
    return this.request<EndGameResult>("POST", "/api/sdk/end", token, {
      result: result ?? {},
    });
  }

  // ---- Leaderboard --------------------------------------------------------

  async submitScore(
    token: string,
    params: SubmitScoreParams,
  ): Promise<SubmitScoreResult> {
    return this.request<SubmitScoreResult>(
      "POST",
      "/api/sdk/leaderboard/submit",
      token,
      {
        score: params.score,
        metadata: params.metadata,
      },
    );
  }

  async getLeaderboard(
    token: string,
    params?: LeaderboardParams,
  ): Promise<LeaderboardResult> {
    const query = new URLSearchParams();
    if (params?.period) query.set("period", params.period);
    if (params?.limit !== undefined) query.set("limit", String(params.limit));
    if (params?.offset !== undefined)
      query.set("offset", String(params.offset));

    const qs = query.toString();
    const path = "/api/sdk/leaderboard" + (qs ? `?${qs}` : "");
    return this.request<LeaderboardResult>("GET", path, token);
  }

  // ---- Achievements -------------------------------------------------------

  async registerAchievements(
    token: string,
    achievements: AchievementDef[],
  ): Promise<RegisterAchievementsResult> {
    return this.request<RegisterAchievementsResult>(
      "POST",
      "/api/sdk/achievement/register",
      token,
      { achievements },
    );
  }

  async unlockAchievement(
    token: string,
    achievementKey: string,
  ): Promise<UnlockResult> {
    return this.request<UnlockResult>(
      "POST",
      "/api/sdk/achievement/unlock",
      token,
      { achievement_key: achievementKey },
    );
  }

  async getAchievements(token: string): Promise<AchievementsResult> {
    return this.request<AchievementsResult>(
      "GET",
      "/api/sdk/achievements",
      token,
    );
  }

  // ---- Webhook verification (static) -------------------------------------

  /**
   * Verify an incoming webhook request from Boomclaw.
   *
   * Recomputes the HMAC-SHA256 signature and compares it to the value in the
   * headers using a constant-time comparison.  Returns `true` when valid.
   */
  static verifyWebhookSignature(
    secret: string,
    headers: WebhookHeaders,
    body: string,
  ): boolean {
    const timestamp = headers["x-boomclaw-timestamp"];
    const signature = headers["x-boomclaw-signature"];

    if (!timestamp || !signature) {
      return false;
    }

    const message = `POST\n/webhook\n${timestamp}\n${body}`;
    const expected = createHmac("sha256", secret)
      .update(message)
      .digest("hex");

    try {
      return timingSafeEqual(
        Buffer.from(signature, "hex"),
        Buffer.from(expected, "hex"),
      );
    } catch {
      return false;
    }
  }

  // ---- Internal -----------------------------------------------------------

  /**
   * Compute the HMAC-SHA256 signature for a request.
   *
   * ```
   * HMAC-SHA256(gameSecret, METHOD + "\n" + PATH + "\n" + TIMESTAMP + "\n" + BODY)
   * ```
   */
  private sign(
    method: string,
    path: string,
    timestamp: string,
    body: string,
  ): string {
    const message = `${method}\n${path}\n${timestamp}\n${body}`;
    return createHmac("sha256", this.gameSecret)
      .update(message)
      .digest("hex");
  }

  /**
   * Execute a signed HTTP request with automatic retry on 5xx errors.
   */
  private async request<T>(
    method: "GET" | "POST",
    path: string,
    token: string,
    body?: Record<string, unknown>,
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const bodyStr = body ? JSON.stringify(body) : "";
    const timestamp = String(Math.floor(Date.now() / 1000));

    // Extract the pathname (including query string) for signing.
    const signPath = path;
    const signature = this.sign(method, signPath, timestamp, bodyStr);

    const headers: Record<string, string> = {
      "X-Boomclaw-Token": token,
      "X-Boomclaw-Timestamp": timestamp,
      "X-Boomclaw-Signature": signature,
      Accept: "application/json",
    };

    if (method === "POST") {
      headers["Content-Type"] = "application/json";
    }

    let lastError: unknown;

    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      if (attempt > 0) {
        // Exponential backoff: 200ms, 400ms, 800ms ...
        const delay = 200 * Math.pow(2, attempt - 1);
        await this.sleep(delay);
      }

      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), this.timeout);

      try {
        const response = await fetch(url, {
          method,
          headers,
          body: method === "POST" ? bodyStr : undefined,
          signal: controller.signal,
        });

        clearTimeout(timer);

        if (response.ok) {
          return (await response.json()) as T;
        }

        // Retry on server errors
        if (response.status >= 500 && attempt < this.maxRetries - 1) {
          lastError = new BoomclawError(
            `Server error: ${response.status}`,
            response.status,
            await response.text().catch(() => null),
          );
          continue;
        }

        // Client errors (4xx) or final 5xx: throw immediately
        let errorBody: unknown;
        try {
          errorBody = await response.json();
        } catch {
          errorBody = await response.text().catch(() => null);
        }

        throw new BoomclawError(
          `HTTP ${response.status}: ${(errorBody as { error?: string })?.error ?? response.statusText}`,
          response.status,
          errorBody,
        );
      } catch (err: unknown) {
        clearTimeout(timer);

        if (err instanceof BoomclawError) {
          throw err;
        }

        if (
          err instanceof DOMException &&
          err.name === "AbortError"
        ) {
          throw new BoomclawTimeoutError(url, this.timeout);
        }

        // Network errors are retryable
        lastError = err;
        if (attempt >= this.maxRetries - 1) {
          throw err;
        }
      }
    }

    // Should be unreachable, but just in case:
    throw lastError;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

export default BoomclawSDK;
