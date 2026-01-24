---
title: Logs
sidebar:
  order: 14
---

CoinsEngine can log all currency-related operations to both console and dedicated log file.

Log file can be found inside the CoinsEngine directory: `operations.log`

## Config

You can toggle logging in the config:

config.yml

```yaml
Enabled:
  Console: true
  File: true
```

Additionally, you can adjust the `Write_Interval` setting to reduce disk usage. This will not affect the operation timestamps.

