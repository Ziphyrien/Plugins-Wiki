# 📝ItemFormat™ (简化版)

## 材质 (Material)

如果值为空或非法，默认为石头 (stone)。

```yaml
material: APPLE
```

## 数量 (Amount)

支持使用 PlaceholderAPI 或数学计算。例如，`%player_health% * 5`。

```yaml
amount: 5
```

## 自定义名称/显示名称 (Custom Name/Display Name)

根据您的配置文件，有两种格式：一种是 1.9 版本之前使用的旧版颜色代码，另一种是后续版本使用的文本组件 (Text Component)。前者使用我们创建的颜色代码格式，后者使用 Mini Message 格式，详见 [此处](https://docs.advntr.dev/minimessage/format.html)。Mini Message 格式要求您的服务器核心是 Paper。

```yaml
name: '&fA smart sword'
```

## 描述 (Lore)

您可以使用 `\n` 表示换行。

根据您的配置文件，有两种格式：一种是 1.9 版本之前使用的旧版颜色代码，另一种是后续版本使用的文本组件 (Text Component)。前者使用我们创建的颜色代码格式，后者使用 Mini Message 格式，详见 [此处](https://docs.advntr.dev/minimessage/format.html)。Mini Message 格式要求您的服务器核心是 Paper。

```yaml
lore:
  - '&fLine 1'
  - '&fLine 2'
```

## 标志 (Flags)

可用值：`HIDE_ENCHANTS, HIDE_ATTRIBUTES, HIDE_UNBREAKABLE, HIDE_DESTROYS, HIDE_PLACED_ON, HIDE_ADDITIONAL_TOOLTIP, HIDE_DYE, HIDE_ARMOR_TRIM`。

```yaml
flags:
  - HIDE_ENCHANTS
  - HIDE_ATTRIBUTES
  - HIDE_UNBREAKABLE
  - HIDE_DESTROYS
  - HIDE_PLACED_ON
  - HIDE_ADDITIONAL_TOOLTIP
  - HIDE_DYE
  - HIDE_ARMOR_TRIM
```

## 附魔 (Enchants)

配置部分格式为：`附魔ID: 附魔等级`。

对于附魔书：您可能需要使用 `stored-enchants` 代替 `enchants`。

对于自定义附魔：某些附魔插件未将其附魔注册到游戏中，因此这对它们不起作用。

在 1.20.5 之后，您应该使用 Minecraft 附魔 ID 而不是 Spigot 的 ID。

```yaml
enchants:
  MENDING: 1
```

## 自定义模型数据 (Custom Model Data)

```yaml
custom-model-data: 15
```

## 头颅 (Skull)

Base64：如下例所示，仅支持 1.19+。

```yaml
skull: eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZ
```

## 物品模型 (Item Model) (1.21.2+) <mark style="color:red;">- 高级版</mark> <a href="#item-model-1.21.2" id="item-model-1.21.2"></a>

```yaml
item-model: 'mycustom:itemmodel'
```

## 提示框样式 (Tooltip Style) (1.21.2+)  <mark style="color:red;">- 高级版</mark> <a href="#tooltip-style-1.21.2" id="tooltip-style-1.21.2"></a>

```yaml
tootip-style: 'mycustom:tooltip'
```
