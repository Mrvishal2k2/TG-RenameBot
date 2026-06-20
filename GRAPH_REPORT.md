# Graph Report - .  (2026-06-20)

## Corpus Check
- Corpus is ~3,220 words - fits in a single context window. You may not need a graph.

## Summary
- 107 nodes · 132 edges · 16 communities detected
- Extraction: 77% EXTRACTED · 22% INFERRED · 1% AMBIGUOUS · INFERRED: 29 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Bot Config and README|Bot Config and README]]
- [[_COMMUNITY_Thumbnail Database Layer|Thumbnail Database Layer]]
- [[_COMMUNITY_Architecture and Dev Notes|Architecture and Dev Notes]]
- [[_COMMUNITY_Config Messages Translation|Config Messages Translation]]
- [[_COMMUNITY_Media Upload Utilities|Media Upload Utilities]]
- [[_COMMUNITY_Callback Rename Handlers|Callback Rename Handlers]]
- [[_COMMUNITY_Utility Helper Functions|Utility Helper Functions]]
- [[_COMMUNITY_Bot Client Entry|Bot Client Entry]]
- [[_COMMUNITY_Pyrogram Client Setup|Pyrogram Client Setup]]
- [[_COMMUNITY_Media Rename Filter|Media Rename Filter]]
- [[_COMMUNITY_Requests Dependency|Requests Dependency]]
- [[_COMMUNITY_Numpy Dependency|Numpy Dependency]]
- [[_COMMUNITY_Pillow Dependency|Pillow Dependency]]
- [[_COMMUNITY_Feedparser Dependency|Feedparser Dependency]]
- [[_COMMUNITY_Owner Username Env|Owner Username Env]]
- [[_COMMUNITY_Custom Caption Env|Custom Caption Env]]

## God Nodes (most connected - your core abstractions)
1. `TG-RenameBot` - 13 edges
2. `Config` - 9 edges
3. `root/config.py` - 7 edges
4. `uploader()` - 7 edges
5. `Bot` - 6 edges
6. `Plugin Auto-Discovery` - 6 edges
7. `root/plugins/cb.py` - 6 edges
8. `root/utils/database.py` - 6 edges
9. `Translation` - 5 edges
10. `Thumbnail` - 5 edges

## Surprising Connections (you probably didn't know these)
- `RenameBot This file is a part of mrvishal2k2 rename repo  Dont kang !!! © Mrvish` --uses--> `Config`  [INFERRED]
  bot.py → root/config.py
- `Bot` --uses--> `Config`  [INFERRED]
  bot.py → root/config.py
- `root/utils/database.py` --depends_on--> `psycopg2-binary`  [INFERRED]
  CLAUDE.md → requirements.txt
- `RenameBot Thanks to Spechide Unkle as always fot the concept  ♥️ This file is a` --uses--> `Config`  [INFERRED]
  root/plugins/custom_thumb.py → root/config.py
- `TG-RenameBot` --depends_on--> `pyrogram==2.0.30`  [EXTRACTED]
  README.md → requirements.txt

## Communities

### Community 0 - "Bot Config and README"
Cohesion: 0.16
Nodes (16): root/config.py, AUTH_USERS env var, Rationale: Newbie-friendly deployment, Auto Detection, BotDunia, BotFather, Spechide, Developer Mrvishal2k2 (+8 more)

### Community 1 - "Thumbnail Database Layer"
Cohesion: 0.15
Nodes (9): BASE, delete_thumbnail(), RenameBot Thanks to Spechide Unkle as always fot the concept  ♥️ This file is a, save_photo(), show_thumbnail(), del_thumb(), df_thumb(), Thumbnail (+1 more)

### Community 2 - "Architecture and Dev Notes"
Cohesion: 0.18
Nodes (15): root/plugins/cb.py, root/plugins/custom_thumb.py, root/utils/database.py, DATABASE_URL env var, root/plugins/main_filter.py, root/messages.py, Plugin Auto-Discovery, Rationale: Fragile mode detection by design (+7 more)

### Community 3 - "Config Messages Translation"
Cohesion: 0.18
Nodes (6): Config, © Mrvishal2k2 RenameBot This file is a part of mrvishal2k2 rename repo Dont kang, Translation, object, RenameBot Thanks to Spechide Unkle as always for the concept  ♥️ This file is a, © Mrvishal2k2 RenameBot This file is a part of mrvishal2k2 rename repo  Dont kan

### Community 4 - "Media Upload Utilities"
Cohesion: 0.2
Nodes (11): Dockerfile, DOWNLOAD_LOCATION env var, ffmpeg (system dependency), FloodWait handler (recursion), progress_for_pyrogram, renamer(), take_screen_shot, uploader() (+3 more)

### Community 5 - "Callback Rename Handlers"
Cohesion: 0.32
Nodes (5): convert_call(), RenameBot This file is a part of mrvishal2k2 rename repo  Dont kang !!! © Mrvish, renamer(), rep_rename_call(), thumb()

### Community 6 - "Utility Helper Functions"
Cohesion: 0.36
Nodes (6): uploader(), copy_file(), humanbytes(), progress_for_pyrogram(), take_screen_shot(), TimeFormatter()

### Community 7 - "Bot Client Entry"
Cohesion: 0.29
Nodes (3): Bot, RenameBot This file is a part of mrvishal2k2 rename repo  Dont kang !!! © Mrvish, Client

### Community 8 - "Pyrogram Client Setup"
Cohesion: 0.4
Nodes (5): bot.py entrypoint, lint_python.yml CI workflow, Pyrogram Client subclass, pyrogram==2.0.30, tgcrypto

### Community 9 - "Media Rename Filter"
Cohesion: 0.67
Nodes (1): RenameBot This file is a part of mrvishal2k2 rename repo  Dont kang !!! © Mrvish

### Community 10 - "Requests Dependency"
Cohesion: 1.0
Nodes (1): requests

### Community 11 - "Numpy Dependency"
Cohesion: 1.0
Nodes (1): numpy

### Community 12 - "Pillow Dependency"
Cohesion: 1.0
Nodes (1): Pillow

### Community 13 - "Feedparser Dependency"
Cohesion: 1.0
Nodes (1): feedparser

### Community 14 - "Owner Username Env"
Cohesion: 1.0
Nodes (1): OWNER_USERNAME

### Community 15 - "Custom Caption Env"
Cohesion: 1.0
Nodes (1): CUSTOM_CAPTION

## Ambiguous Edges - Review These
- `APP_ID` → `BotFather`  [AMBIGUOUS]
  README.md · relation: alternative_source

## Knowledge Gaps
- **27 isolated node(s):** `© Mrvishal2k2 RenameBot This file is a part of mrvishal2k2 rename repo Dont kang`, `RenameBot This file is a part of mrvishal2k2 rename repo  Dont kang !!! © Mrvish`, `tgcrypto`, `requests`, `hachoir` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Requests Dependency`** (1 nodes): `requests`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Numpy Dependency`** (1 nodes): `numpy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pillow Dependency`** (1 nodes): `Pillow`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Feedparser Dependency`** (1 nodes): `feedparser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Owner Username Env`** (1 nodes): `OWNER_USERNAME`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Custom Caption Env`** (1 nodes): `CUSTOM_CAPTION`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `APP_ID` and `BotFather`?**
  _Edge tagged AMBIGUOUS (relation: alternative_source) - confidence is low._
- **Why does `Config` connect `Config Messages Translation` to `Thumbnail Database Layer`, `Callback Rename Handlers`, `Bot Client Entry`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `TG-RenameBot` connect `Bot Config and README` to `Pyrogram Client Setup`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `root/config.py` connect `Bot Config and README` to `Architecture and Dev Notes`, `Media Upload Utilities`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Config` (e.g. with `Bot` and `RenameBot This file is a part of mrvishal2k2 rename repo  Dont kang !!! © Mrvish`) actually correct?**
  _`Config` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `uploader()` (e.g. with `renamer()` and `Thumbnail DB table`) actually correct?**
  _`uploader()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `© Mrvishal2k2 RenameBot This file is a part of mrvishal2k2 rename repo Dont kang`, `RenameBot This file is a part of mrvishal2k2 rename repo  Dont kang !!! © Mrvish`, `tgcrypto` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._