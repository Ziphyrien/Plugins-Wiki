# 🏷️称号 (Tags)

打开插件文件夹中的 `/prefixes/` 文件夹，你会找到 `default.yml` 文件，这是称号配置的示例文件。如果你想创建新称号，请复制它并将其重命名为你想要使用的称号 ID。前缀 ID 与文件名相同，例如，`default.yml` 文件意味着它的称号（或前缀）**ID** 是 `default`。

示例文件如下：

```yaml
# Remove whole display item section to make it hide in GUI
display-item:
  unlocked:
    material: DRAGON_EGG
    name: '{display-value}'
    lore:
      - '&7Display Value: {display-value}'
      - '&7Preview: %mythicprefixes_prefix_example_chat% %player_name%'
      - '&dOp will always can use the tag, give'
      - '&dyourself &4-mythicprefixes.bypass.*'
      - '&dpermission to avoid that.'
      - '&eClick to use!'
  using:
    material: DRAGON_EGG
    name: '{display-value}'
    lore:
      - '&7Display Value: {display-value}'
      - '&7Preview: %mythicprefixes_prefix_example_chat% %player_name%'
      - '&cYou are now using this prefix!'
      - '&eClick to cancel use this prefix!'
  locked:
    material: DRAGON_EGG
    name: '&cLocked'
    lore:
      - '&7Display Value: {display-value}'
      - '&7Preview: %mythicprefixes_prefix_example_chat% %player_name%'
      - '&cKill a dragon to unlock!'
  max-reached:
    material: DRAGON_EGG
    name: '{display-value}'
    lore:
      - '&7Preview: %mythicprefixes_prefix_example_chat% %player_name%'
      - '&cYou have reached max use of prefix!'

bedrock:
  extra-line: '&f{status}'

display-value: '&8Dragon Killer'
weight: 15
auto-hide: false

# Premium version only
groups:
  - chat
  - example

effects:
  enabled: false
  1:
    type: MythicLib
    stat: MAX_HEALTH
    value: 1
  2:
    # Premium version only
    type: MythicMobs
    stat: ATTACK_DAMAGE
    value: 1

equip-actions:
  1:
    type: message
    message: 'Start equip the tag!'
unequip-actions:
  1:
    type: message
    message: 'Not equip the tag!'
circle-actions:
  1:
    type: message
    message: 'This is default message. Default prefix has equipped so prefix effect also activated!'
# Premium version only
click-actions:
  condition-not-meet:
    1:
      type: message
      message: 'You did not unlock this prefix!'
  max-limit-reached:
    1:
      type: message
      message: 'You reached the limit of max prefix using!'

conditions:
  1:
    type: permission
    permission: 'killed.dragon'
```

`display-item` 部分用于设置 GUI 中显示的物品。如果删除该部分，此称号将不会在 GUI 中可见。

如果你觉得麻烦，可以直接在 `display-item` 键下使用 ItemFormat，这样所有四种状态都将使用相同的物品，并支持 **{status}** 占位符来显示称号的当前状态。

`{status}` 占位符显示的内容可以在 `config.yml` 中设置，如下所示：

```yaml
# {status} Placeholder
status-placeholder:
  unlocked: '&eClick to use'
  using: '&eClick to cancel use this prefix.'
  locked: '&cYou do not have permission to use this prefix.'
  max-reached: '&cYou can not use anymore prefix.'
```

其他选项：

* display-value: 此称号显示的内容，支持使用 PlaceholderAPI。
* weight: 此称号显示的权重，数值越小权重越高（排在越前面），权重相同的称号将根据其 ID 排序。
* groups: 此称号属于哪些组。<mark style="color:red;">(付费版)</mark>
* effects: 参见 [此页面](tag-effect-buff.md)。
* conditions: 此称号的解锁条件。
* equip-actions: 玩家装备此称号后执行的动作。
* unequip-actions: 玩家卸下此称号后执行的动作。
* circle-actions: 玩家使用此称号时循环执行的动作，你可以在 `config.yml` 文件中设置周期时间。
* click-actions: 如果玩家点击特定状态的称号时执行的动作，目前仅支持 `condition-not-meet`（条件不满足）和 `max-limit-reached`（达到最大限制）状态。<mark style="color:red;">(付费版)</mark>
* auto-hide: 当玩家不满足使用条件时，是否在 GUI 中自动隐藏此前缀。
* bedrock: 基岩版 UI 的设置。点击 [这里](tag-gui.md) 了解更多。

当在显示占位符配置的 `default-prefixes` 选项中使用前缀时，只有这些选项会生效。

```yaml
display-value: '&fPlayer'
weight: 1
auto-hide: false

conditions: []
```
