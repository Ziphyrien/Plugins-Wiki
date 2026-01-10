# Plugins Wiki AI Instructions

You are assisting with the **Plugins Wiki** project, a documentation aggregation and translation system. This project crawls documentation from various sources (GitBook, Retype), manages their translation from English to Chinese, and transforms them for a Starlight-based frontend.

## 🏗 Architecture & Data Flow

The system operates in a 3-stage pipeline:

1.  **Crawl (`scripts/crawl.py`)**:
    - Fetches documentation based on `scripts/wiki_configs.json`.
    - Supports `gitbook` and `retype` sources.
    - **Source:** Remote URLs.
    - **Destination:** `docs/<project_name>/` (English content).

2.  **Translate (`scripts/translation_manager.py`)**:
    - Manages the lifecycle of translations.
    - Tracks file hashes to detect outdated translations.
    - **Source:** `docs/` (English).
    - **Destination:** `docs_zh/` (Chinese).
    - **Metadata:** `version_metadata.json` stores state (hashes, timestamps, status).

3.  **Transform (`scripts/transform_for_starlight.js`)**:
    - Prepares content for the Starlight documentation framework.
    - Generates frontmatter, sidebar order, and fixes links.
    - **Source:** `docs/` and `docs_zh/`.
    - **Destination:** `dist-starlight/`.

4.  **Sync & Deploy (GitHub Actions)**:
    - Syncs transformed content to the `starlight` branch.
    - Deploys the Starlight/Astro site to GitHub Pages.
    - **Trigger:** Push to `main`.
    - **Flow:** `main` -> `sync_starlight.yml` -> `starlight` -> `deploy_starlight.yml` -> GitHub Pages.

## 🌿 Branching Strategy & Local Environment

The repository is configured as a **Bare Repository** with **Git Worktrees**, allowing simultaneous access to both branches in the same workspace.

- **Workspace Root (`D:/Plugins Wiki/`)**:
    - Contains the `.git` bare repository and workspace config.
    - Open `Plugins-Wiki.code-workspace` in VS Code to see both folders.

- **`main` Folder (`D:/Plugins Wiki/main/`)**:
    - **Branch:** `main`
    - **Role:** Backend, Content Source, Transformation Logic.
    - **Content:** Markdown docs (`docs/`, `docs_zh/`), Python/JS scripts (`scripts/`).
    - **Tasks:** Crawling, Translation, running the Transformation script.

- **`starlight` Folder (`D:/Plugins Wiki/starlight/`)**:
    - **Branch:** `starlight`
    - **Role:** Frontend, Astro Application, Theme Customization.
    - **Content:** Astro project (`src/`, `astro.config.mjs`), UI components.
    - **Tasks:** CSS styling, layout changes, component development, running `npm run dev`.

**Local Workflow:**
1.  **Edit Content:** Modify `.md` files in the `main` folder.
2.  **Transform:** Run `node scripts/transform_for_starlight.js` in `main`. This outputs to `main/dist-starlight/`.
3.  **Preview:** To preview changes locally, copy contents from `main/dist-starlight/` to `starlight/src/content/docs/` (or equivalent path in the frontend app).
4.  **Edit Theme:** Modify UI code directly in the `starlight` folder.

**CI/CD Relationship:**
- The CI pipeline on GitHub handles the official sync: Pushing to `main` triggers a job that transforms content and commits it to the `starlight` branch automatically.

## 🔗 File Sync & Content Mapping Strategy

This project maintains a strict separation between **Source Content** (in `main`) and **Presentation Content** (in `starlight`). Understanding the exact file mapping is critical for development.

### 1. Conceptual Mapping
Every documentation file in the `main` branch has a single corresponding destination in the `starlight` branch, but the directory structure changes to accommodate multi-language support (i18n).

| Content Type | Source Path (`main` branch) | Destination Path (`starlight` branch) |
| :--- | :--- | :--- |
| **English Docs** | `docs/{project}/{path}` | `starlight/src/content/docs/en/{project}/{path}` |
| **Chinese Docs** | `docs_zh/{project}/{path}` | `starlight/src/content/docs/zh/{project}/{path}` |

### 2. Concrete Examples
Here is how specific files are transformed and moved during the sync process:

- **Example 1 (English Feature):**
  - **Source:** `main/docs/coinsengine/features/wallet.md`
  - **Transform:** Adds frontmatter (`title: Wallet`, `sidebar: ...`)
  - **Intermediate:** `main/dist-starlight/en/coinsengine/features/wallet.md`
  - **Final:** `starlight/src/content/docs/en/coinsengine/features/wallet.md`

- **Example 2 (Chinese Translation):**
  - **Source:** `main/docs_zh/mythicprefixes/welcome.md`
  - **Transform:** Adds frontmatter (`title: 欢迎`, `sidebar: ...`)
  - **Intermediate:** `main/dist-starlight/zh/mythicprefixes/welcome.md`
  - **Final:** `starlight/src/content/docs/zh/mythicprefixes/welcome.md`

### 3. The Transformation Bridge
The directory `main/dist-starlight/` acts as the bridge.
- When you run `node scripts/transform_for_starlight.js`, it clears `dist-starlight/` and rebuilds it from `docs/` and `docs_zh/`.
- It automatically creates the `en/` and `zh/` folders.
- It is this `dist-starlight` folder that must be copied to `starlight/src/content/docs/` to see changes.

### 4. Rule of Thumb for Editors
- **IF** you want to change the text of a page -> Edit `main/docs/...` or `main/docs_zh/...`.
- **IF** you want to change the visual layout or CSS -> Edit `starlight/src/...` (but NOT `content/docs`).
- **IF** you edit a file in `starlight/src/content/docs/` -> Your changes **WILL BE LOST** on the next sync.

## 📂 Directory Structure

- `docs/`: Raw English documentation (crawled).
- `docs_zh/`: Translated Chinese documentation.
- `dist-starlight/`: Final output ready for Starlight build.
- `scripts/`:
    - `core/`: Shared logic (`crawler_*.py`, `version_control.py`).
    - `crawl.py`: Entry point for crawling.
    - `translation_manager.py`: CLI for translation tracking.
    - `transform_for_starlight.js`: Node.js build script.
    - `wiki_configs.json`: Configuration for wiki sources.

## 🛠 Critical Workflows

### 1. Crawling Documentation
To update the raw English documentation:
```bash
# Crawl all configured wikis
python scripts/crawl.py all

# Crawl a specific wiki (e.g., coinsengine)
python scripts/crawl.py coinsengine
```

### 2. Managing Translations
Use the translation manager to track progress:
```bash
# Check overall status
python scripts/translation_manager.py status

# List files needing translation
python scripts/translation_manager.py list pending

# Mark a file as completed (updates hash in metadata)
python scripts/translation_manager.py complete docs/path/to/file.md
```

### 3. Building/Transforming
To generate the Starlight-ready content:
```bash
npm run transform
# OR
node scripts/transform_for_starlight.js
```

## 🧩 Configuration & Conventions

- **Wiki Configs (`scripts/wiki_configs.json`)**:
    - Defines `type` (`gitbook` or `retype`), `base_url`, and `output_dir`.
    - Add new documentation sources here.

- **Translation Metadata (`version_metadata.json`)**:
    - **DO NOT EDIT MANUALLY.** Use `translation_manager.py`.
    - Tracks `original_hash` vs `translated_hash` to determine `outdated` status.
    - **Fields**:
        - `crawled_at`: Last time the original file was crawled.
        - `source_hash`: MD5 of original content.
        - `translated_at`: Last time translation was updated.
        - `translation_hash`: MD5 of translated content.
        - `translation_status`: `pending`, `in_progress`, `completed`, `outdated`.

### Metadata Sync for Frontend
- `version_metadata.json` is synced to `starlight/src/assets/` during deployment and local transformation.
- **Purpose**: It is used by the `PageTitle.astro` component to display "Last Updated" dates on the documentation pages.
    - English pages show `crawled_at`.
    - Chinese pages show `translated_at`.

## 🚀 Development Tips

- **Python Environment**: Used for crawling and translation management. Ensure dependencies are installed (standard libs + `requests` likely used in core).
- **Node Environment**: Used for the final build step.
- **Path Handling**: The system handles both Windows and Linux paths, but prefer forward slashes `/` in configuration and relative paths.
- **Adding a New Wiki**:
    1.  Add entry to `scripts/wiki_configs.json`.
    2.  Run `python scripts/crawl.py <name>`.
    3.  Run `npm run transform` to verify output.
