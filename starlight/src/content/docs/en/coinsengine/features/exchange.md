---
title: Exchange
sidebar:
  order: 12
---

CoinsEngine features built-in exchange system that allow players to exchange one currency for another.

## Setup

Say we want to set exchange rates for **Gems** and **Coins**, where 1 Gem = 5 Coins. In this case our exchange rates will be the following:

* Gems -> Coins = 5
* Coins -> Gems = 1 / 5 = 0.2

Let's add them in the currency configs:

gems.yml

```yaml
Exchange:
  Allowed: true # Must be enabled.
  Rates:
    coins: 5.0
```

coins.yml

```yaml
Exchange:
  Allowed: true # Must be enabled.
  Rates:
    gems: 0.2
```

Now players can exchange Gems to Coins with 1 to 5 rate, and Coins to Gems with 5 to 1 (aka 1 to 0.2) rate.

:::note
If currency's `Decimal` setting set on `false`, player can exchange only integer amount of said currency.
:::

