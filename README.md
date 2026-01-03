# 文档汉化工具

本项目提供了一套完整的文档同步与翻译管理工具，用于自动化爬取文档并管理中文翻译进度。

## 📁 项目结构

```
MythicPrefixes Wiki/
├── scripts/
│   ├── crawl_docs.py           # 文档爬取工具
│   ├── translation_manager.py  # 翻译管理工具
│   └── version_control.py      # 版本控制模块
├── docs/                        # 原文文档目录 (自动生成)
├── docs_zh/                     # 中文翻译目录
├── version_metadata.json        # 版本元数据文件 (自动生成)
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 依赖库：`requests`

```bash
pip install requests
```

### 1. 同步官方文档

```bash
python scripts/crawl_docs.py
```

该命令会：
- 从官方 sitemap 获取所有文档页面
- 下载新文档或更新已变更的文档到 `docs/` 目录
- 自动跟踪文件版本和变更时间
- 检测已删除的文档

### 2. 查看翻译状态

```bash
python scripts/translation_manager.py status
```

显示详细状态：
```bash
python scripts/translation_manager.py status -d
```

### 3. 扫描译文目录

```bash
python scripts/translation_manager.py scan --lang-dir docs_zh
```

自动扫描 `docs_zh/` 目录，发现已有的译文并更新翻译状态。

## 📖 脚本详细说明

### crawl_docs.py - 文档爬取工具

从 MythicPrefixes 官方网站自动同步文档。

**使用方法：**
```bash
python scripts/crawl_docs.py
```

**功能特性：**
- 🆕 自动检测新增文档
- 🔄 基于 lastmod 时间检测更新
- ⏭️ 跳过未变更的文档
- 🗑️ 检测并标记已删除的文档
- 📊 显示同步统计信息

---

### translation_manager.py - 翻译管理工具

管理文档的翻译进度和状态。

**可用命令：**

| 命令 | 说明 | 示例 |
|------|------|------|
| `status` | 显示翻译状态摘要 | `python scripts/translation_manager.py status` |
| `status -d` | 显示详细状态 | `python scripts/translation_manager.py status -d` |
| `list <状态>` | 列出特定状态的文件 | `python scripts/translation_manager.py list pending` |
| `start <文件>` | 标记开始翻译 | `python scripts/translation_manager.py start docs/guide.md` |
| `complete <文件>` | 标记翻译完成 | `python scripts/translation_manager.py complete docs/guide.md` |
| `info <文件>` | 显示文件详细信息 | `python scripts/translation_manager.py info docs/guide.md` |
| `note <文件> <备注>` | 添加备注 | `python scripts/translation_manager.py note docs/guide.md "需要校对"` |
| `scan` | 扫描译文目录 | `python scripts/translation_manager.py scan --lang-dir docs_zh` |
| `check` | 检查一致性 | `python scripts/translation_manager.py check` |

**翻译状态说明：**

| 状态 | 说明 |
|------|------|
| `pending` | ⏳ 待翻译 - 新文档，尚未开始翻译 |
| `in_progress` | 🔄 翻译中 - 正在进行翻译 |
| `completed` | ✅ 已完成 - 翻译已完成 |
| `outdated` | ⚠️ 需更新 - 原文已更新，译文需要同步 |

---

### version_control.py - 版本控制模块

核心版本控制模块，被其他脚本调用。

**跟踪的信息：**
- `original_created` - 原文首次获取时间
- `original_modified` - 原文最后变更时间
- `original_hash` - 原文内容 MD5 哈希
- `translated_at` - 汉化完成时间
- `translated_hash` - 译文内容哈希
- `translation_status` - 翻译状态

## 📋 典型工作流程

### 1. 初始化项目

```bash
# 首次同步所有文档
python scripts/crawl_docs.py
```

### 2. 开始翻译

```bash
# 查看待翻译文件
python scripts/translation_manager.py list pending

# 标记开始翻译某个文件
python scripts/translation_manager.py start docs/welcome.md

# 在 docs_zh/ 目录创建对应的翻译文件并翻译
# 翻译完成后，标记为已完成
python scripts/translation_manager.py complete docs/welcome.md
```

### 3. 定期同步更新

```bash
# 同步官方文档更新
python scripts/crawl_docs.py

# 检查是否有需要更新的译文
python scripts/translation_manager.py list outdated

# 检查整体一致性
python scripts/translation_manager.py check
```

### 4. 批量扫描译文

如果已有 `docs_zh/` 目录中的译文，可以批量扫描更新状态：

```bash
python scripts/translation_manager.py scan --lang-dir docs_zh
```

## 📊 查看进度

```bash
# 简要摘要
python scripts/translation_manager.py status

# 输出示例：
# ============================================================
# 📊 翻译进度摘要
# ============================================================
#   📁 总文件数:     25
#   ⏳ 待翻译:       10
#   🔄 翻译中:       3
#   ✅ 已完成:       10
#   ⚠️  需要更新:     2
# ============================================================
```

## 🔧 配置说明

脚本中的关键配置（位于 `crawl_docs.py`）：

```python
SITEMAP_URL = "https://mythicprefixes.superiormc.cn/sitemap-pages.xml"
BASE_URL = "https://mythicprefixes.superiormc.cn"
OUTPUT_DIR = "docs"  # 原文保存目录
```

## 📝 注意事项

1. **版本元数据**：`version_metadata.json` 文件保存了所有文档的版本信息，请勿手动删除
2. **目录结构**：译文应放在 `docs_zh/` 目录，保持与 `docs/` 相同的目录结构
3. **文件编码**：所有文件使用 UTF-8 编码
4. **定期同步**：建议定期运行 `crawl_docs.py` 以获取官方文档更新

## 📄 License

MIT License
