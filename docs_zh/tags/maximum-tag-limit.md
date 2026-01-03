# 🪄最大称号限制 (Maximum Tag Limit)

默认情况下，普通玩家只能装备 **1** 个称号，拥有 `group.vip` 权限的玩家可以额外装备 1 个称号。这可以在 `config.yml` 文件中更改。

```yaml
max-prefixes-amount:
  default:
    default: 1
    vip: 2
  scoreboard:
    deafult: 1
    vip: 2
  # Group ID
  # chat:
  #   default: 1
  #   vip: 1

max-prefixes-amount-conditions:
  vip:
    1:
      type: permission
      permission: 'group.vip'
```

`default` 部分的意思是：默认情况下，所有称号共享的最大限制，这并不代表一个名为 `default` 的组，并且此部分不能删除。

`default` 下面的部分是针对不同组的。关于 **称号组** 的信息，请查看 [此页面](tag-group-premium.md)。在这个例子中，`scoreboard` 是组 ID。你可以在 [称号](tags.md) 配置中将称号添加到组。组部分下的配置意味着玩家在该组中最多可以使用多少个称号。

> [!NOTE]
> 称号组功能仅适用于 <mark style="color:red;">**付费**</mark> 版用户。


这是一个例子：

```yaml
max-prefixes-amount:
  default:
    default: 5
  scoreboard:
    deafult: 3
  chat:
    deafult: 3
```

在这个例子中，玩家最多可以装备 5 个称号。在这 5 个称号中，最多 3 个属于 `chat` 组，最多 3 个属于 `scoreboard` 组。

比如你的服务器有属于 `chat` 组的称号 `A, B, C, D`，以及属于 `scoreboard` 组的称号 `E, F, G, H`。如果你没有装备任何称号，你现在可以装备任何称号，比如我选择了称号 `A, B, C`，选择这 3 个称号后，我不能再装备称号 `D` 了，因为我已经达到了 `chat` 组的限制。但是，我可以尝试装备称号 `E, F, G, H`，因为 `scoreboard` 组的称号没有达到限制，也没有达到 5 个称号的默认限制。此时，我还可以从 `scoreboard` 组中选择两个称号。

## 效果限制 <mark style="color:red;">- 付费版</mark>

想要允许玩家装备多个称号，但只激活 1 个称号的效果，其他称号效果不激活？试试这个配置！你应该把它们放在你的 [称号](tags.md) 配置中。

```yaml
# 称号配置中的其他称号选项...

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
