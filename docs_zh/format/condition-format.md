# ⚖️条件格式 (Condition Format)

## 可用占位符

* {world}
* {amount}
* {player\_x}
* {player\_y}
* {player\_z}
* {player\_pitch}
* {player\_yaw}
* {player}

## 生物群系 (Biome)

玩家必须在这些生物群系中。

```yaml
  conditions:
    1:
      type: biome
      biome: oraxen
```

## 权限 (Permission)

玩家必须拥有所有这些权限。

**请记住，OP 玩家将始终拥有所有权限，除非插件默认设置为不拥有，所以如果你想测试此条件，你必须取消自己的 OP 权限。**

```yaml
  conditions:
    1:
      type: permission
      permission: 'group.vip'
```

## 占位符 (Placeholder)

玩家必须满足占位符条件。

规则可以设置为：

* \>=
* <=
* \>
* <
* \== (字符串)
* \= (数字)
* != (数字或字符串)
* !\*= (数字或字符串) 不包含。
* \*= (字符串) 包含，例如，str \*= string 为真，但 example \*= ple 为假。

```yaml
  conditions:
    1:
      type: placeholder
      placeholder: '%player_health%'
      rule: '<='
      value: 5
```

## 任意 (Any) <mark style="color:red;">- 付费版</mark>

```yaml
  conditions:
    1:
      type: any
      conditions:
        1:
          type: placeholder
          placeholder: '%eco_balance%'
          rule: '>='
          value: 200
        2:
          type: placeholder
          placeholder: '%player_points%'
          rule: '>='
          value: 400
```

## 非 (Not) <mark style="color:red;">- 付费版</mark> <a href="#not" id="not"></a>

```yaml
  conditions:
    1:
      type: not
      conditions:
        1:
          type: placeholder
          placeholder: '%eco_balance%'
          rule: '>='
          value: 200
```

## 已装备称号 (Equipped Prefix) <mark style="color:red;">- 付费版</mark>

```yaml
  conditions:
    1:
      type: equipped_prefix
      prefixes:
        - tag1
        - tag2
      require-all: false
```

## 已装备称号数量 (Equipped Prefix Amount) <mark style="color:red;">- 付费版</mark>

```yaml
  conditions:
    1:
      type: equipped_prefix_amount
      amount: 2
```

## 生效称号数量 (Effected Prefix Amount) <mark style="color:red;">- 付费版</mark>

```yaml
  conditions:
    1:
      type: effected_prefix_amount
      amount: 2
```
