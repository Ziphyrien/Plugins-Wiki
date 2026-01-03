# 🛠️配置文件

插件会生成以下配置文件，其中一些文件只有在你首次使用该功能后才会生成。

* `datas`: 存储插件数据文件的位置。仅在不使用数据库时生成。请勿修改此处的任何内容。
* `languages`: 存储语言文件的位置。你可以通过 `config.yml` 文件中的 `config-files.language` 选项设置插件使用的语言文件。你可以通过语言文件自定义插件游戏内的各种消息。不支持根据玩家客户端语言显示对应的语言文件。你只能为所有玩家显示相同的语言。
* `display_placeholders`: 显示占位符配置文件的位置。
* `prefixes`: 称号（标签）配置文件的位置。
* `config.yml` 文件: 插件的主要通用设置位置。

## Config.yml 文件内容 <a href="#config.yml-file-content" id="config.yml-file-content"></a>

```yaml
# MythicPrefixes Made by @PQguanfang
#
# Read the wiki here: mythicprefixes.superiormc.cn

debug: false

language: en_US

cache:
  # If you are facing issue when plugin load cache, try set this option to JOIN.
  load-mode: LOGIN
  # Bypass condition check when player still joining the server.
  bypass-condition-when-loading: true
  # Cache remove will delay 3 seconds after player left the server, set -1 to disable.
  remove-delay: -1

# {status} Placeholder
status-placeholder:
  unlocked: '&eClick to use'
  using: '&eClick to cancel use this prefix.'
  locked: '&cYou do not have permission to use this prefix.'
  max-reached: '&cYou can not use anymore prefix.'

circle-actions:
  period-tick: 20

max-prefixes-amount:
  default: 1
  vip: 2

max-prefixes-amount-conditions:
  vip:
    1:
      type: permission
      permission: 'group.vip'

choose-prefix-gui:
  title: 'Choose your prefix'
  size: 54
  forbid-click-outside: false
  auto-translate-item-name: true
  prefix-item-slot: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                     16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
                     31,32,33,34,35,36,37,38,39,40,41,42,43,44]
  filter-item:
    # Set to -1 to hide.
    slot: 47
    material: ANVIL
    name: '&bFilter'
    lore:
      - '&7Filter: {filter}'
    placeholder:
      all: '&aALL'
      using: '&cUSING'
      can-use: '&dCan Use'
  next-page-item:
    slot: 52
    material: ARROW
    name: '&cNext page'
    lore:
      - '&7Page: {now}/{max}'
      - '&eClick to view next page'
  previous-page-item:
    slot: 46
    material: ARROW
    name: '&cPrevious page'
    lore:
      - '&7Page: {now}/{max}'
      - '&eClick to view previous page'
  custom-item:
    49: # Mean the slot
      material: SPAWNER
      name: '&4Unequip All tags'
      lore:
        - '&cClick to unequip.'
      actions:
        1:
          type: removeall
    53: # Mean the slot
      material: BARRIER
      name: '&cClose'
      lore:
        - '&cClick to close this menu.'
      actions:
        1:
          type: close

database:
  enabled: false
  jdbc-url: "jdbc:mysql://localhost:3306/mythicprefixes?useSSL=false&autoReconnect=true"
  jdbc-class: "com.mysql.cj.jdbc.Driver"
  properties:
    user: root
    password: 123456

auto-save:
  enabled: false
  period-tick: 6000
  hide-message: false

libreforge-hook: false
libreforge-effects:
  - id: default
    effects:
      - id: bonus_health
        args:
          health: 40
      - id: damage_multiplier
        args:
          multiplier: 4.0
        triggers:
          - melee_attack
    conditions: []
```
