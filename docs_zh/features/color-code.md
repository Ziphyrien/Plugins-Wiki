# 🎨颜色代码 (Color Code)

我们提供 2 种颜色代码格式。插件会自动判断您使用的颜色代码格式，因此您无需对此进行任何设置。

## MiniMessage <a href="#minimessage" id="minimessage"></a>

* 您可以在 [此处](https://docs.advntr.dev/minimessage/format.html) 查看此格式。
* 需要 Paper 或其分支，且服务器版本至少为 1.17.1。
* 可以使用许多高级功能，如字体、悬停等。
* 您几乎可以在任何地方使用它。

## 内置颜色解析器 (Built-in Color Parser) <a href="#built-in-color-parser" id="built-in-color-parser"></a>

* 格式：
  * 要使用十六进制颜色，您应该使用特殊的颜色代码，格式如下：**`&#十六进制颜色代码`**
  * 例如，`&#ff0000`。
  * 要使用渐变颜色，您应该使用特殊的渐变颜色代码，格式如下：**`&<#起始颜色代码> 消息 &<#结束颜色代码>`**
  * 例如，`&<#666666>UltimateShop &<#ffffff>`。
  * 要使用普通颜色，例如 `&b`。
  * 对于 1.16 以下的版本，我们会自动将十六进制颜色转换为普通颜色。
* 支持所有版本和服务器核心。
* 仅支持有用的颜色功能。
* 您可以在任何地方使用它。
* 对于满足使用 MiniMessage 要求的 Paper 用户，我们会自动将内置颜色解析器转换为 MiniMessage 格式。
