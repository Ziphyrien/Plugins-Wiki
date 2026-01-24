---
title: PlaceholderAPI
sidebar:
  order: 16
---

**CoinsEngine** features built-in [PlaceholderAPI](https://spigotmc.org/resources/6245/) integration. No need to install any expansions!

:::note[Tip]
You can use placeholders in currency's `Format` and `Format_Short` settings.

Make sure you have `PlaceholderAPI_For_Currency_Format: true` in the **config.yml**.
:::

## Placeholders

:::caution
Replace `[currency]` with a [Currency ID](../features/currencies#currency-id).
:::

### Player Balance

* `%coinsengine_balance_short_clean_[currency]%` - Player currency balance, [compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), no colors.
* `%coinsengine_balance_short_legacy_[currency]%` - Player currency balance, [compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), legacy colors.
* `%coinsengine_balance_short_[currency]%` - Player currency balance, [compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), plain colors.
* `%coinsengine_balance_clean_[currency]%` - Player currency balance, formatted, no colors.
* `%coinsengine_balance_legacy_[currency]%` - Player currency balance, formatted, legacy colors.
* `%coinsengine_balance_raw_[currency]%` - Player currency balance, unformatted, no colors.
* `%coinsengine_balance_[currency]%` - Player currency balance, formatted, plain colors.

### Server Balance

* `%coinsengine_server_balance_short_clean_[currency]%` - Player currency balance, [compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), no colors.
* `%coinsengine_server_balance_short_legacy_[currency]%` - Server currency balance, [compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), legacy colors.
* `%coinsengine_server_balance_short_[currency]%` - Server currency balance, [compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), plain colors.
* `%coinsengine_server_balance_clean_[currency]%` - Server currency balance, formatted, no colors.
* `%coinsengine_server_balance_legacy_[currency]%` - Server currency balance, formatted, legacy colors.
* `%coinsengine_server_balance_raw_[currency]%` - Server currency balance, unformatted, no colors.
* `%coinsengine_server_balance_[currency]%` - Server currency balance, formatted, plain colors.

### Player Data

* `%coinsengine_payments_state_[currency]%` - Player's currency payments state.

### Leaderboards

:::caution
You must enable the [Leaderboards](../features/leaderboards) for these placeholders to work.
:::

:::note
Replace `[pos]` with a position in the leaderboard.
:::

* `%coinsengine_leaderboard_position_[currency]%` - Player's current leaderboard position.
* `%coinsengine_top_balance_short_clean_[pos]_[currency]%` - Balance of a player at specific position. [Compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), no colors.
* `%coinsengine_top_balance_short_legacy_[pos]_[currency]%` - Balance of a player at specific position. [Compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), legacy colors.
* `%coinsengine_top_balance_short_[pos]_[currency]%` - Balance of a player at specific position. [Compacted](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts), plain colors.
* `%coinsengine_top_balance_clean_[pos]_[currency]%` - Balance of a player at specific position. Formatted, no colors.
* `%coinsengine_top_balance_legacy_[pos]_[currency]%` - Balance of a player at specific position. Formatted, legacy colors.
* `%coinsengine_top_balance_[pos]_[currency]%` - Balance of a player at specific position. Formatted, plain colors.
* `%coinsengine_top_player_[pos]_[currency]%` - Name of a player at specific position.
