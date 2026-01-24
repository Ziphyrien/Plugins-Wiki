---
title: Vault
sidebar:
  order: 4
---

CoinsEngine can be used as a primary economy provider for your server if you have the [Vault](https://spigotmc.org/resources/34315/) plugin installed.

:::danger
This feature is not compatible with the following plugins:

* **EssentialsX** - Essentials economy can not be disabled. It's recommended to use a modern alternative.
* **Towny** - Towny uses 'fake' economy accounts for towns with 'fake' UUIDs, which is not supported in CoinsEngine.
* **MMOProfiles** - Same as Towny.
:::

## Link Currency

:::note[Data Migration]
Before setting CoinsEngine as your economy, you can [import](../features/migration) data into it from your current economy plugin.
:::

1. Open the `config.yml` file.
2. Go to the `Integration` -> `Vault` section.
3. Set `Enabled` to `true`.
4. Enter the correct currency ID in the `EconomyCurrency` setting.
5. Reboot the server to apply changes.

config.yml

```yaml
Integration:
  Vault:
    Enabled: true
    EconomyCurrency: money # Your currency ID
```

## Unlink Currency

1. Open the `config.yml` file.
2. Go to the `Integration` -> `Vault` section.
3. Set `Enabled` to `false`.
4. Reboot the server to apply changes.

config.yml

```yaml
Integration:
  Vault:
    Enabled: false
    EconomyCurrency: money # Does not matter if integration is disabled.
```

