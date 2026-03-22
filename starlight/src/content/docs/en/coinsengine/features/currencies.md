---
title: Currencies
sidebar:
  order: 7
---

CoinsEngine allow you to create **unlimited** amount of highly **customizable** virtual currencies through configuration files.

Currency files located in the `/currencies/` directory.

## Currency ID

The **Currency ID** is a unique internal name that identifies a specific currency. The Currency ID is used in configuration files, commands, placeholders, and other places.

Finding the Currency ID is very simple: it is the same as the currency file name, but without the `.yml` extension.

For example, if your currency file is named `coins.yml`, the Currency ID will be `coins`.

## Creation

Creating currencies in CoinsEngine is very simple!

Run the `/coe create <name> <symbol> [decimals]` command, where:

* `name` is currency name (identifier). Only latin letters, digits and underscore are allowed. You can change currency display name later.
* `symbol` is currency symbol.
* `decimals` is whether decimals are allowed for this currency.

That's it! The following guides may help you in further currency configuration:

* [Cross-Server Setup](cross-server)
* [Vault Integration](../hooks/vault)
* [Exchange](exchange)
* Leaderboards

:::caution
Server reboot may be required to properly register new currency commands.
:::

## Removal

To remove a currency, simply delete it's config file from the `/currencies/` directory and [reload](../commands) the plugin.

:::note
Database column will retain after currency removal. Players can get their balances back if said column is assigned to some other currency.
:::

