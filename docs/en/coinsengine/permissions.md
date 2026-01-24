---
title: Permissions
sidebar:
  order: 3
---

Giving access to parent permission will give access to all child permissions.

* `coinsengine.*` - Access to all plugin functions.
  + `coinsengine.currency.*` - Grants access to all currencies.
    - `coinsengine.currency.[currency]` - Grants access to a currency. Replace `[currency]` with a [Currency ID](features/currencies#currency-id).
  + `coinsengine.command.*` - Access to all commands.
    - `coinsengine.command.currency.balance` - Access to currency's balance command.
    - `coinsengine.command.currency.balance.others` - Access to currency's balance command on other players.
    - `coinsengine.command.currency.add` - Access to currency's give command.
    - `coinsengine.command.currency.addall` - Access to currency's giveall command.
    - `coinsengine.command.currency.set` - Access to currency's set command.
    - `coinsengine.command.currency.take` - Access to currency's take command.
    - `coinsengine.command.currency.exchange` - Access to currency's exchange command.
    - `coinsengine.command.currency.payments` - Access to currency's payments command.
    - `coinsengine.command.currency.payments.others` - Access to currency's payments command on other players.
    - `coinsengine.command.currency.send` - Access to currency's send command.
    - `coinsengine.command.currency.top` - Access to currency's top command.
    - `coinsengine.command.wallet` - Access to `/wallet` command.
    - `coinsengine.command.wallet.others` - Access to `/wallet` command on other players.
    - `coinsengine.command.create` - Access to `/coe create` command.
    - `coinsengine.command.reset` - Access to `/coe reset` command.
    - `coinsengine.command.resetall` - Access to `/coe resetall` command.
    - `coinsengine.command.migrate` - Access to `/coe migrate` command.
    - `coinsengine.command.reload` - Access to `/coe reload` command.
  + `coinsengine.hidefromtops` - Removes player from leaderboards.
