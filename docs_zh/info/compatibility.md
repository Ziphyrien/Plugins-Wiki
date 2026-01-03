# 🔗兼容性

## **直接兼容**

### <mark style="color:red;">直接</mark>支持的属性插件列表

你可以将这些插件的属性添加为称号效果增益。

* MythicLib (支持来自 MMOCore 或 MMOItems 的属性)
* MythicMobs
* AuraSkills&#x20;

## PlaceholderAPI: 额外占位符

MythicPrefixes 为 PlaceholderAPI 提供了这些新占位符！

### %mythicprefixes\_\<displayPlaceholderID>%

你可以在其他插件（如聊天、计分板）中使用此 **PlaceholderAPI** 占位符来显示玩家正在使用的称号。例如：`%mythicprefixes_chat%`。

{% hint style="info" %}
如果你不知道 `displayPlaceholderID` 是什么意思，请先查看 [此页面](../tags/tags.md)。\
如果你的显示占位符 ID 或前缀 ID 包含 `_` 符号，你可以将其替换为 `-` 符号，否则插件可能无法正确解析它们。
{% endhint %}

### %mythicprefixes\_prefix\_\<prefixID>\_\<displayPlaceholderID>%

使用此占位符可以显示玩家正在使用的称号，再加上指定的称号，非常适合想要帮助玩家预览称号的情况。

### %mythicprefixes\_prefix\_\<prefixID>% <mark style="color:red;">- 付费版</mark>

仅显示称号。

### %mythicprefixes\_no\_\<displayPlaceholderID>\_\<number>% <mark style="color:red;">- 付费版</mark>

显示当前显示占位符的第 X 个称号。例如：%mythicprefixes\_no\_chat\_2% 表示 `chat` 显示占位符中显示的第二个称号。

### %mythicprefixes\_amount%

此占位符将显示玩家正在使用的称号数量。

你可以在 `config.yml` 文件中设置玩家可以同时使用的最大称号数量。

### %mythicprefixes\_status\_\<prefixID>%

此占位符将显示玩家指定称号的状态。

可能的值：<https://github.com/PQguanfang/MythicPrefixes/blob/master/src/main/java/cn/superiormc/mythicprefixes/objects/PrefixStatus.java>

### %mythicprefixes\_max%

显示玩家可以同时使用的最大称号数量。
