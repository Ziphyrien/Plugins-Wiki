# Minecraft 插件文档翻译 Prompt

1.  **语气自然，拒绝机翻**
    *   译文要符合中文母语者的阅读习惯，语气专业且亲切。
    *   避免使用被动语态（如“被用于...”可改为“用于...”）。
    *   避免直译从句，应将其拆分为通顺的短句。
    *   **不要**使用“它”来指代插件，直接省略或使用“该插件”。

2.  **专业术语与 MC 语境**
    *   准确使用 Minecraft 服务器领域的专用术语。
    *   **保留英文的常见术语**：GUI, Lore, NBT, UUID, Tick, TPS, Placeholder (或译为变量), Hook (或译为挂钩/对接), API。
    *   **标准译名**：
        *   Configuration / Config -> 配置文件 / 配置
        *   Permission -> 权限
        *   Command -> 指令 / 命令
        *   Item -> 物品
        *   Enchantment -> 附魔
        *   Spawn -> 生成
        *   Cooldown -> 冷却
    *   **严禁**使用“中文（English）”的格式（例如：不要写“配置文件（Config）”）除非有歧义。要么直接用中文，要么（如果是专有名词）直接用英文。

3.  **链接本地化处理**
    *   识别文档中的内部链接。如果链接指向 Wiki 的其他页面，请将其转换为指向本地文件的 **相对路径** Markdown 链接。
    *   假设当前翻译的文件与目标文件在相同的目录结构下。
    *   示例：
        *   原文：`See [Commands](https://wiki.example.com/info/commands)`
        *   译文：`参阅 [指令](../info/commands.md)` (假设当前文件在 features 目录下)
    *   如果无法确定相对路径，请保留文件名并以 `.md` 结尾。

4.  **代码与配置保留**
    *   代码块（Code Block）内的所有内容原则上**不翻译**，除非是注释（`#` 开头的内容）或示例中的显示文本（Display Name/Lore）。
    *   配置文件的键（Key）、权限节点（Permission Node）、变量（%player_name%）**绝对不能翻译**。

## 示例对比

| 原文 | ❌ 糟糕的翻译 | ✅ 优秀的翻译 |
| :--- | :--- | :--- |
| This plugin is designed to help admins manage tags. | 这个插件被设计去帮助管理员管理称号（tags）。 | 该插件旨在帮助管理员管理称号。 |
| You can configure the `messages.yml` file. | 你可以配置 `messages.yml` 文件。 | 您可以配置 `messages.yml` 文件。 |
| Check the [Installation](https://wiki.site/install) page. | 检查 [安装](https://wiki.site/install) 页面。 | 请查看 [安装指南](../info/install.md) 页面。 |

