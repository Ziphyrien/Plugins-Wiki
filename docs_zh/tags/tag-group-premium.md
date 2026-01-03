# 👥称号组 - 付费版 (Tag Group - Premium)

## 创建新称号组

打开 `prefixes` 文件夹中的任何称号配置，你会发现以下内容：

```yaml
# Premium version only
groups:
  - chat
  - example
```

`groups` 选项决定了此称号属于哪些组。你不需要做任何事情来创建新的称号组，你只需要在这里放一个随机选择的 ID，插件会自动为你分类！

## 此功能有什么用？

* 你可以使用命令 `/prefix opengui <groupID>` 打开一个仅包含指定组称号的 GUI。更多信息请查看 [命令](../info/commands.md) 页面。
* 你可以在显示占位符配置中使用 `display-prefixes.group` 选项来决定哪个称号将显示在此显示占位符中。更多信息请查看 [显示占位符](display-placeholder.md) 页面。
* 你可以在 `config.yml` 文件中按组确定最大称号数量。更多信息请查看 [最大称号限制](maximum-tag-limit.md) 页面。
