---
title: Leaderboards
sidebar:
  order: 11
---

Leaderboards feature provides an option to view the richest players of each currency through text or GUI based leaderboards.

:::note
You can remove players from the leaderboards by giving them `coinsengine.hidefromtops` [permission](../permissions).

After granting/revoking permission, the player **must** join the server for the permission to take effect.
:::

## Main Config

Leaderboards options located in the **config.yml** under the `Top` section:

* `Enabled` - Enables the feature.
* `Use_GUI` - Enables leaderboards GUI for players.
* `Update_Interval` - Sets leaderboards update interval.
* `Entries_Per_Page` - Amount of players per page in text-based leaderboards.

Leaderboards GUI config located in the `/menu/leaderboard.yml` file.

## Currency Settings

You can disable leaderboard for certain [currencies](currencies) in their config files:

```yaml
Leaderboard:
  Enabled: false
```

