# ⌨️命令

## /mythicprefixes opengui

打开称号 GUI。仅限游戏内使用。

## /mythicprefixes opengui \<player>

为指定玩家打开称号 GUI。仅限控制台使用。

## /mythicprefixes opengui \<group>

打开称号 GUI，但仅包含指定组的称号。

## /mythicprefixes opengui \<player> \<group>

为指定玩家打开称号 GUI，但仅包含指定组的称号。仅限控制台使用。

## /mythicprefixes reload

重载插件。

## /mythicprefixes addprefix \<prefix>

为自己添加新称号。这是添加操作，意味着我们不会尝试移除玩家已经使用的称号。仅限游戏内使用。

## /mythicprefixes addprefix \<player> \<prefix>

为指定玩家添加新称号。这是添加操作，意味着我们不会尝试移除玩家已经使用的称号。

## /mythicprefixes removeprefix \<prefix>

移除自己正在使用的称号。仅限游戏内使用。

## /mythicprefixes removeprefix \<player> \<prefix>

移除指定玩家正在使用的称号。

## /mythicprefixes viewusingprefix

查看你正在使用的称号。仅限游戏内使用。

## /mythicprefixes viewusingprefix \<player>

查看指定玩家正在使用的称号。

## /mythicprefixes setprefix \<prefixes>

将你正在使用的称号设置为指定值。支持使用 `;;` 分隔每个称号。

## /mythicprefixes setprefix \<player> \<prefixes>

将指定玩家正在使用的称号设置为指定值。支持使用 `;;` 分隔每个称号。

## 命令权限

对于权限，你需要给予玩家 `mythicprefixes.<subCommand>` 才能使用相应的命令，例如 `mythicprefixes.opengui`。

## 绕过权限

你可以给予玩家 `mythicprefixes.bypass.<prefixID>` 权限，使玩家绕过插件检查。

默认情况下，OP 拥有此权限。
