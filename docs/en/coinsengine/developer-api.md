---
title: Developer API
sidebar:
  order: 19
---

You can import **CoinsEngine** to your project using Maven. Replace `{VERSION}` with the latest version below:

![](https://repo.nightexpressdev.com/api/badge/latest/releases/su/nightexpress/coinsengine/CoinsEngine?color=40c14a&name=CoinsEngine&prefix=v)

```markup
<repository>
  <id>nightexpress-releases</id>
  <url>https://repo.nightexpressdev.com/releases</url>
</repository>

<dependency>
  <groupId>su.nightexpress.coinsengine</groupId>
  <artifactId>CoinsEngine</artifactId>
  <version>{VERSION}</version>
</dependency>
```

## Events

* `ChangeBalanceEvent` - Called after the player's currency balance chagned.

## Data Access

```java
// Obtain currency object by currency ID.
Currency currency = CoinsEngineAPI.getCurrency("coins");
if (currency == null) return;

// Obtain balance.
double balance = CoinsEngineAPI.getBalance(player, currency);

// Set player's currency balance and schedule for save.
CoinsEngineAPI.setBalance(Player player, Currency currency, double amount);
CoinsEngineAPI.setBalance(UUID playerId, Currency currency, double amount);
CoinsEngineAPI.setBalance(UUID playerId, String currency, double amount);

// Add to player's currency balance and schedule for save.
CoinsEngineAPI.addBalance(Player player, Currency currency, double amount);
CoinsEngineAPI.addBalance(UUID playerId, Currency currency, double amount);
CoinsEngineAPI.addBalance(UUID playerId, String currency, double amount);

// Remove from player's currency balance and schedule for save.
CoinsEngineAPI.removeBalance(Player player, Currency currency, double amount);
CoinsEngineAPI.removeBalance(UUID playerId, Currency currency, double amount);
CoinsEngineAPI.removeBalance(UUID playerId, String currency, double amount);

// Obtain user data.
CoinsUser user = CoinsEngineAPI.getUserData(Player player); // Can't be null.
CoinsUser user = CoinsEngineAPI.getUserData(String playerName); // Nullable
CoinsUser user = CoinsEngineAPI.getUserData(UUID uuid); // Nullable

// User methods (no save schedule).
user.setBalance(currency, amount);
user.addBalance(currency, amount);.
user.removeBalance(currency, amount);

// Register custom currency.
CoinsEngineAPI.getCurrencyManager().registerCurrency(myCurrency);
```

