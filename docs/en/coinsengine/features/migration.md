---
title: Migration
sidebar:
  order: 13
---

CoinsEngine supports balance data migration from the following plugins:

* [PlayerPoints](https://www.spigotmc.org/resources/80745/)
* [Vault](https://www.spigotmc.org/resources/34315/) - A compatible economy plugin is required to be installed.

:::note
You can disable the Migration feature in the **config.yml** -> `Migration` -> `Enabled` to save some RAM.
:::

## Guide

A plugin from which you plan to migrate **must be installed** on the server during migration process. You'd also need a [currency](currencies#creation) to migrate in.

Run the `/coe migrate <plugin> <currency>` command to start migration. Where:

* `plugin` - Plugin to migrate from.
* `currency` - Currency to migrate in.

Example: `/coe migrate vault money`

:::danger
Migration will override existent CoinsEngine player balances of selected currency.
:::

:::caution
If you get a currency error when migrating from Vault, ensure the currency used for migration is **not** linked with [Vault](../hooks/vault).
:::

