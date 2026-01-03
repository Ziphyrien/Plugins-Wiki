# 🖥️显示占位符 (Display placeholder)

## 创建新的显示占位符

打开插件文件夹中的 `/display_placeholders/` 文件夹，你会找到 `chat.yml` 文件，这是显示占位符配置的示例文件。如果你想创建新的显示占位符，请复制它并将其重命名为你想要使用的显示占位符 ID。

示例文件如下：

```yaml
start-symbol: '&f['
split-symbol: '&f, '
end-symbol: '&f]'
parse-color: true
display-prefixes:
  mode: WHITE
  prefixes: 
    - tag1
    - tag2
  groups:
    - example
display-amount: 2
empty-display: ''
default-prefixes:
 - 'default'
always-display-default-prefixes: false
```

这是一个显示占位符的示例，文件名（即 `chat`）是它的 ID。你可以使用此格式创建无限的显示占位符。

* start-symbol: 占位符的起始内容。
* split-symbol: 每个称号之间的间隔内容。
* end-symbol: 占位符的结束内容。
* display-prefixes:&#x20;
  * mode: 支持的值：**BLACK**（黑名单）和 **WHITE**（白名单）。（免费版仅支持 **BLACK**）
  * prefixes: 此占位符中将显示哪些称号。
  * groups: 是否在占位符中显示对应组的称号。<mark style="color:red;">(付费版)</mark>
* display-amount: 显示的最大称号数量，设置为 -1 表示无限制。
* parse-color: 一些插件可能已经支持 MiniMessage 格式的颜色。如果是这种情况，你可以考虑禁用此选项，这样 MythicPrefixes 就不会解析占位符中存在的颜色代码，从而允许你使用 MiniMessage 格式支持的更多功能。
* empty-display: 如果没有要显示的称号，将显示的文本。这将替换 `start-symbol` 和 `end-symbol` 选项提供的内容。
* default-prefixes: 如果此占位符中没有要显示的称号，我们将使用默认称号代替，我们将从上到下按顺序找到玩家可以使用的第一个称号。它只会显示，不会执行任何动作或效果。<mark style="color:red;">(付费版)</mark>
* always-display-default-prefixes: 如果设置为 true，即使玩家装备了任何称号，我们仍然会自动装备在 default-prefixes 选项中设置的默认称号。<mark style="color:red;">(付费版)</mark>

## 使用显示占位符

你可以在任何其他支持 PlaceholderAPI 的插件中使用 PlaceholderAPI 来使用显示占位符，更多信息请查看 [此页面](../info/compatibility.md)。
