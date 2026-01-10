# Plugins Wiki

Plugins Wiki 是一个自动化的文档聚合与翻译系统，旨在将来自不同源（如 GitBook, Retype）的插件文档统一抓取、管理翻译，并使用 [Starlight](https://starlight.astro.build/) 构建现代化的文档站点。

## 项目简介

本项目采用前后端分离的架构：
- **后端 (Main)**: 负责爬虫抓取、版本控制、翻译管理和内容转换。
- **前端 (Starlight)**: 基于 Astro/Starlight 的文档展示层，负责 UI 渲染和部署。

### 核心特性
- **多源爬取**: 支持 GitBook 和 Retype 类型的文档源。
- **增量更新**: 基于 MD5 哈希检测原文变动，自动标记 "需更新" (Outdated) 的翻译。
- **自动化工作流**: GitHub Actions 自动处理从内容转换到站点部署的全过程。
- **现代化 UI**: 使用 Starlight 提供优秀的多语言阅读体验。


## 分支/目录策略

推荐在本地开发时使用 **Git Worktree** 管理分支，建议的目录结构如下：
1. **`main/` (内容源)**: 包含爬虫脚本、翻译管理工具和原始 Markdown 文档 (`docs/`, `docs_zh/`)。
2. **`starlight/` (前端)**: 包含 Astro 项目源码、组件和样式。

> **注意**: **不要** 直接修改 `starlight/src/content/docs` 下的文件，因为它们会被 CI 流程覆盖。所有内容修改都应在 `main/docs_zh` 中进行。

## 环境准备

开始前，请确保您的环境已安装：
- **Python**: 3.8+ (用于爬虫和翻译管理)
- **Node.js**: v20+ (推荐 v24，用于构建脚本)
- **pnpm**: 包管理器

```bash
# 安装 Python 依赖
pip install requests beautifulsoup4

# 安装 Node.js 依赖 (在 main 目录)
cd "main"
npm install

# 安装 Node.js 依赖 (在 starlight 目录)
cd "starlight"
pnpm install
```

## 常用操作指南

### 1. 抓取文档 (Crawl)

从配置的源站抓取最新文档。

```bash
# 进入 main 目录
cd "main"

# 抓取所有配置的 Wiki
python scripts/crawl.py all

# 仅抓取特定 Wiki (例如 mythicprefixes)
python scripts/crawl.py mythicprefixes
```

### 2. 管理翻译 (Translation)

使用翻译管理器追踪进度。它会根据 `version_metadata.json` 记录文件状态。

```bash
# 查看整体翻译状态
python scripts/translation_manager.py status

# 列出所有待翻译文件
python scripts/translation_manager.py list pending

# 扫描 docs_zh 目录，自动识别已存在的文件并标记为完成
# (当你手动创建了翻译文件后，运行此命令更新元数据)
python scripts/translation_manager.py scan

# 手动标记某个文件为翻译完成
python scripts/translation_manager.py complete docs/mythicprefixes/welcome.md
```

### 3. 多语言翻译规则
- 原文位于 `main/docs/<wiki_name>/...`
- 译文请创建在 `main/docs_zh/<wiki_name>/...` (确保文件名和目录结构与原文完全一致)
- 翻译完成后，务必运行 `translation_manager.py scan` 更新状态，否则系统会认为翻译未完成。

### 4. 本地预览 (Preview)

在本地查看最终效果需要两个步骤：转换和启动服务器。

```bash
# 步骤 1: 在 main 目录执行转换
# 这会将 docs 和 docs_zh 处理成 Starlight 可识别的格式，输出到 dist-starlight
cd "main"
npm run transform

# 步骤 2: 将生成的内容复制到 starlight 内容目录
# (这一步在本地手动执行，在 GitHub 上由 Action 自动完成)
# Windows PowerShell 示例:
Copy-Item -Recurse -Force "dist-starlight\*" "..\starlight\src\content\docs\"
Copy-Item -Force "version_metadata.json" "..\starlight\src\assets\"


# 步骤 3: 启动 Starlight 开发服务器
cd "..\starlight"
pnpm run dev
```

## 项目结构说明

### Main 目录
- `docs/`: 存放爬取的英文原文（`crawled_at` 和 `source_hash` 依据）。
- `docs_zh/`: 存放人工翻译的中文文档。
- `scripts/`:
  - `crawl.py`: 爬虫入口。
  - `translation_manager.py`: 状态管理工具。
  - `transform_for_starlight.js`: 构建转换脚本。
- `version_metadata.json`: 核心数据库，记录爬取配置、文件哈希、翻译状态。

### Starlight 目录
- `src/content/config.ts`: 内容集合定义。
- `src/components/`: 自定义 Astro 组件 (如 `PageTitle.astro` 用于显示翻译时间)。
- `astro.config.mjs`: Starlight 配置文件，包含侧边栏插件配置。
- `sidebar.mjs`: 前端侧边栏导航配置，需要手动维护以匹配新添加的内容。

## 如何贡献

### 添加新的 Wiki 源
1. 编辑 `main/version_metadata.json` 中的 `configs` 部分。
2. 添加新的 Wiki 配置对象：
   ```json
   "new-plugin": {
     "type": "gitbook",
     "base_url": "https://...",
     "output_dir": "docs/new-plugin"
   }
   ```
3. 运行 `python scripts/crawl.py new-plugin` 进行首次抓取。
4. 更新 `starlight/sidebar.mjs` 以在侧边栏显示新插件。

### 修复文档错误
- **翻译错误**: 直接修改 `main/docs_zh/` 下的对应文件。
- **原文错误**: 原文由爬虫生成，请不要直接修改 `main/docs/` 下的文件，因为下次爬取会被覆盖。

## CI/CD 流程

项目包含两个主要的 GitHub Workflows：

1. **`sync_starlight.yml`**: 
   - 监听 `main` 分支的 Push。
   - 运行转换脚本。
   - 将转换后的内容自动同步并提交到 `starlight` 分支。

2. **`deploy_starlight.yml`**:
   - 监听 `starlight` 分支的 Push (通常由上面的 workflow 触发)。
   - 构建 Astro 站点并部署到 GitHub Pages。
