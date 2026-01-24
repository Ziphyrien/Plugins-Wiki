---
title: Prefixes
sidebar:
  order: 8
---

Each currency in CoinsEngine can have it's own prefix. This is a great customization tool to help you differentiate one currency from the others.

## Setup

First of all, enable the feature in the **config.yml** -> `Prefix` -> `Enabled: true`

You'll see the `Format` setting there, that defines global prefix format for **all** currencies:

```yaml
Format: '<gray>[<white>%currency_prefix%</white>]</gray> <gray>'
```

To set currency prefix, edit the `Prefix` value in [currency config](currencies). This value is used to replace the `%currency_prefix%` placeholder in the format above.

:::note
If you want your currencies to have completely different prefixes, make `Format` option to have only `%currency_prefix%` placeholder and set the entire prefix format in currency files.
:::

