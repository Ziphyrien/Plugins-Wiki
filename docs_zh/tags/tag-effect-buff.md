# 💪称号增益效果 (Tag Effect/BUFF)

## 注意

免费版最多只能设置 3 个称号启用称号效果，付费版没有此限制。

## libreforge 效果

> [!NOTE]
> MythicPrefixes 不包含 libreforge，你必须购买任何包含 libreforge 的 Auxilor 插件，然后将其安装在你的服务器中才能使其工作！


如果你想让一个称号拥有 libreforge 效果，你需要做以下事情：

* 将 `config.yml` 中的 `libreforge-hook` 选项设置为 `true`。
* 将称号配置中的 `effects.enabled` 选项设置为 `true`。
* 在 `config.yml` 的 `libreforge-effects` 选项中添加效果。**请注意，效果 ID 必须与称号 ID 相同。**

示例：

```yaml
libreforge-effects:
  - id: default # 效果 ID
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

## 内置效果

如果你想让一个称号拥有内置效果增益，你需要做以下事情：

* 将称号配置中的 `effects.enabled` 选项设置为 `true`。
* 如果你的称号配置中不存在以下内容，请添加。
* 如果你在此处删除了 BUFF，你需要重启服务器。

### MythicLib

添加来自 MythicLib 插件的属性。（支持来自 MMOCore、MMOItems 的属性）

```yaml
effects:
  enabled: true
  1: 
    type: MythicLib
    stat: MAX_HEALTH # 属性 ID
    value: 1 # 增加的值
  2: # 更多效果...
```

### MythicMobs&#x20;

添加来自 MythicMobs 插件的属性。

> [!NOTE]
> 如果你遇到 **NoSuchMethod** 错误，这意味着你使用的是旧版本的 MythicMobs，你需要将其更新到 **最新版**。\
> 默认情况下，MythicMobs 中存在的所有属性都是禁用的，你需要在 `plugins/MythicMobs/stats.yml` 文件或其他属性配置中启用它们。


```yaml
effects:
  enabled: true
  1: 
    type: MythicMobs
    modifier-type: SET # ADD, SET, MULTIPLY, COMPOUND
    stat: HEALTH
    value: 100
  2: # 更多效果...
```

### AuraSkills&#x20;

添加来自 AuraSkills 插件的属性。

> [!NOTE]
> 由于 AuraSkills 会保存属性修饰符，所以如果你的服务器崩溃、前缀配置更改或其他情况，玩家的属性可能无法正确清除。虽然 MythicPrefixes 考虑到了这个问题，但如果它仍然在你的服务器中发生：你可以尝试重启服务器。如果这不能解决问题，你将不得不对每个玩家使用 `/skills modifier removeall` 命令。


```yaml
effects:
  enabled: false
  1:
    type: AuraSkills
    stat: HEALTH
    value: 100
  2: # 更多效果...
```

## 条件

你可以为效果设置条件。只需尝试在此处添加 `conditions` 部分。

```yaml
effects:
  enabled: true
  1:
    type: MythicLib
    stat: MAX_HEALTH
    value: 100
    bypass-condition-after-equip: true
    conditions:
      1:
        type: world
        world: lobby
```

还有一个名为 `bypass-condition-after-equip` 的选项可用，如果设置为 `false`，如果我们发现玩家不再满足效果条件，插件将自动移除效果。

## 效果限制 <mark style="color:red;">- 付费版</mark>

想要允许玩家装备多个称号，但只激活 1 个称号的效果，其他称号效果不激活？试试这个配置！

```yaml
effects:
  enabled: true
  1:
    type: MythicLib
    stat: MAX_HEALTH
    value: 100
    bypass-condition-after-equip: true # 添加这个
    conditions: # 添加这个
      1:
        type: effected_prefix_amount
        amount: 1 # 更改为你想要的限制值。
```

## 常见问题：你的效果没有正确清除？

这通常是由于服务器上的多个插件试图更改玩家的基础属性引起的。例如，你的服务器安装了 MMOItems 和 EcoEnchants（这是一种非常常见的情况），它们都有增加玩家最大生命值的功能，这可能会导致潜在的功能冲突。这不是由我们的插件引起的，MythicPrefixes 会正常清理添加的属性，但你的其他插件错误地将之前的生命值识别为玩家的真实生命值，然后将其加回来。

像 HuskSync 这样的多服务器同步插件也可能导致此问题，请尝试在这些插件中禁用属性同步。
