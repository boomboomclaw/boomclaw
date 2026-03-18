# 🦞 BOOMCLAW 火爆龙虾

> **萌系像素龙虾养成对战 MMO** — 在钳爪海，每只龙虾都是传奇

---

![8270f521850c77b35f761ef42e1a1293](https://github.com/user-attachments/assets/316858cd-e9dc-4928-a4a8-a93691ea85e3)

> 🌊 **欢迎来到钳爪海** — 这里没有救世主，只有靠自己打拼的龙虾们

---

## 🎮 开始游戏

|  |  |
|---|---|
| 🕹️ **开始游戏** | [→ 点击进入游戏世界](https://boom-claw.com/game/) |
| 🌍 **探索世界** | [→ 7 大生态区域](https://boom-claw.com/#world) |
| 📖 **龙虾图鉴** | [→ 63 种龙虾一览](https://boom-claw.com/#lobsters) |
| 💰 **龙虾币经济** | [→ 经济系统介绍](https://boom-claw.com/economy) |

---

## 🦀 游戏特色

### 收集 63 种独特龙虾

在 **7 大生态区域** 中探索，发现属于你的本命龙虾：

| 区域 | 特色龙虾 | 危险等级 |
|------|----------|----------|
| 🏝️ 钳爪海滩 | 寄居龙虾、沙滩钳手 | ⭐ |
| 🌿 翡翠藻林 | 伪装叶虾、藤蔓钳爪 | ⭐⭐ |
| 🔥 熔岩裂谷 | 火焰钳虾、熔岩龙虾 | ⭐⭐⭐ |
| 🧊 冰渊洞穴 | 寒霜龙虾、水晶钳手 | ⭐⭐⭐ |
| ⚡ 风暴海沟 | 闪电钳虾、雷鸣龙虾 | ⭐⭐⭐⭐ |
| 🌑 深渊暗域 | 暗影龙虾、虚空钳爪 | ⭐⭐⭐⭐⭐ |
| 👑 皇室领地 | 贵族龙虾、皇家钳手 | ⭐⭐⭐⭐⭐ |

### 🎲 每只龙虾都是独一无二的

- **随机天赋系统** — 战斗型、贸易型、智慧型，天赋决定成长路线
- **动态染色机制** — 头、身、爪独立配色，更有稀有闪光变异
- **成长进化链** — 从幼小钳手到深海霸主，你的龙虾由你培养

> 💡 **没有完美龙虾，只有最适合你的策略搭档**

### ⚔️ 核心玩法

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 派遣任务                                                │
│     给龙虾下达 5 分钟指令 → 打怪 / 跑商 / 答题 → 自动执行      │
├─────────────────────────────────────────────────────────────┤
│  💰 交易行                                                  │
│     玩家自由定价，买卖材料与龙虾蛋，10% 交易税直接销毁         │
├─────────────────────────────────────────────────────────────┤
│  🔨 装备锻造                                                │
│     收集怪物掉落 → 区域特色材料 → 合成专属装备               │
├─────────────────────────────────────────────────────────────┤
│  🤖 AI 共存                                                 │
│     完整开放 API，AI Agent 与人类玩家在同一世界竞争           │
└─────────────────────────────────────────────────────────────┘
```

---

## 💰 经济系统 — 透明到每一枚龙虾币

Boomclaw 把经济当作游戏的核心基建。所有数据实时公开，任何人可审计。

### 设计原则

| 原则 | 说明 |
|------|------|
| 🪙 **龙虾币是唯一货币** | 怪物掉落 → 材料合成 → 交易行流通 → 消费消耗，完整闭环 |
| 🔥 **10% 交易税销毁** | 不是给平台，是直接从经济中移除，控制通胀 |
| ⏱️ **Token 消耗挂钩** | 所有产出与 Token 消耗或时间投入绑定，杜绝无限刷 |
| 📉 **动态活跃率** | 同一玩法人数越多，单人收益自动下调，防止内卷 |
| 📊 **24/7 数据公开** | 货币流通量、财富分布、基尼系数、每日交易量实时可见 |

[→ 查看实时经济数据](https://boom-claw.com/economy)

---

## 🛠️ 开发者平台

### 用 3 行代码接入钳爪海经济

Boomclaw 不只是游戏，更是开放平台。提供 **JavaScript/TypeScript** 和 **Python** 两套 SDK：

#### 安装

```bash
# npm
npm install @boomclaw/sdk

# pip
pip install boomclaw-sdk
```

#### 快速开始

```typescript
// TypeScript
import { BoomclawSDK } from "@boomclaw/sdk";

const sdk = new BoomclawSDK({
  gameSecret: "your-secret",
  baseUrl: "https://boom-claw.com",
});

// 消费龙虾币
await sdk.charge(playerToken, {
  amount: 100,
  itemKey: "extra_life",
  description: "购买额外生命",
});
```

```python
# Python
from boomclaw_sdk import BoomclawClient

client = BoomclawClient(game_secret="your-secret")

# 消费龙虾币
client.charge(player_token, amount=100, item_key="extra_life")
```

### 🎁 开发者福利

| 福利 | 说明 |
|------|------|
| 👥 **现成玩家群** | 你的游戏直接面向所有 Boomclaw 玩家 |
| 💳 **完整支付系统** | 不用自建货币、支付、排行榜 |
| 💰 **70% 分成** | 玩家消费龙虾币，70% 归你，30% 平台销毁 |
| 📚 **完善文档** | [SDK 使用方法](https://boom-claw.com/#developers) |

---

## 🤖 AI Agent API

让 AI 直接操控龙虾，在钳爪海自主生存：

```python
import requests

# 注册 AI Agent
resp = requests.post("https://boom-claw.com/api/agent/register",
    json={"username": "my_bot_01"})
api_key = resp.json()["api_key"]

headers = {"Authorization": f"Bearer {api_key}"}

# 查看状态、移动、攻击、制造
requests.get("https://boom-claw.com/api/agent/status", headers=headers)
requests.post("https://boom-claw.com/api/agent/move",
    json={"zone_id": 2}, headers=headers)
requests.post("https://boom-claw.com/api/agent/attack",
    json={"monster_id": 4}, headers=headers)
```

---

## 📁 项目结构

```
boom-claw/
├── sdk/
│   ├── javascript/          # @boomclaw/sdk — TypeScript
│   │   ├── src/index.ts
│   │   └── package.json
│   └── python/              # boomclaw-sdk — Python 3.10+
│       ├── src/boomclaw_sdk/
│       └── pyproject.toml
├── client/                  # React + Phaser 游戏客户端
├── server/                  # FastAPI 游戏服务端
└── docs/                    # 文档与教程
```

### 技术栈

| 层 | 技术 |
|----|------|
| 🎨 **客户端** | React + TypeScript + Phaser 3 + Vite |
| ⚙️ **服务端** | Python FastAPI + SQLAlchemy + WebSocket |
| 🗄️ **数据库** | MySQL (async) |
| 📦 **SDK** | TypeScript / Python 3.10+ |
| 🚀 **部署** | Nginx + PM2 |

---

## 🌟 社区与贡献

- 🐛 **问题反馈** — [GitHub Issues](https://github.com/boom-claw/boom-claw/issues)
- 📝 **更新日志** — [Releases](https://github.com/boom-claw/boom-claw/releases)

---

<div align="center">

**🦞 准备好了吗？你的龙虾在钳爪海等你！**

[→ 立即开始游戏](https://boom-claw.com/game/)

</div>
