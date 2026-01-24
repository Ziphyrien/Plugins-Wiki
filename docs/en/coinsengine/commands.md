---
title: Commands
sidebar:
  order: 2
---

Command aliases can be changed in the **engine.yml**. By default it's `/coinsengine` or `/coe`.

## Flags

* `-s` - makes silent command execution (target player won't be notified).
* `-sf` - disables command feedback to the command sender.

## Plugin Commands

`<> Required` `[] Optional`

* `/coe [help]` - List of all plugin commands.
* `/coe reload` - Reload the plugin.
* `/coe create <name> <symbol> <decimals>` - [Creates](features/currencies#creation) a new currency.
* `/coe reset <player>` - Reset player's balance for all currencies.
* `/coe resetall [currency]` - Reset balance of all or specific currency for all players.
* `/coe migrate <plugin> <currency>` - [Migrate](features/migration) balances from specific plugin to specific currency.

## Currency Commands

Each currency has it's own command aliases defined in the [currency config](features/currencies) under `Command_Aliases` option.

Commands listed below are valid for the currency with the `coins` command alias.

`<> Required` `[] Optional`

* `/coins balance [player]` - View "coins" balance.
* `/coins pay <player> <amount>` - Pay some "coins" some player.
* `/coins payments [player] [-s]` - Toggle "coins" payments from other players.
* `/coins giveall <amount> [-s] [-sf]` - Give "coins" to all online players.
* `/coins give <player> <amount> [-s] [-sf]` - Give "coins" to a player.
* `/coins take <player> <amount> [-s] [-sf]` - Take "coins" from a player.
* `/coins set <player> <amount> [-s] [-sf]` - Set "coins" balance for a player.
* `/coins exchange <currency> <amount>` - Exchange "coins" for other currency.
* `/coins top [page]` - Top players with "coins". Requires the [Leaderboards](features/leaderboards) feature to be enabled.

:::note
[Number Shortcuts](https://nightexpressdev.com/nightcore/configuration/number-formation/#number-shortcuts) are supported in the `amount` argument!
:::

There is the `commands.yml` config file inside the CoinsEngine directory, where you can edit and disable any currency-related command.

**Command Options:**

* `Children` - Controls whether the command is available as  of the currency command. Example: `/coins balance`
* `Dedicated` - Controls whether the command is available as  command for primary currency. Example: `/balance`

## Dedicated Commands

* `/wallet [player]` - View balance of all currencies. Requires the [Wallet](features/wallet) feature to be enabled.
* `/balance [player]` - View balance of primary currency.
* `/baltop [page]` - Top players by primary currency. Requires the [Leaderboards](features/leaderboards) feature to be enabled.
* `/pay <player> <amount>` - Pay player with primary currency.
* `/paytoggle [player]` - Toggle primary currency payments from players.

:::note
Primary currency is the one that linked with [Vault](hooks/vault).
:::

