---
name: git-push-remote
description: >-
  Stages, commits, and pushes this Obsidian Vault to GitHub via a project Python
  script. Use when the user asks to push to remote, sync to GitHub, 推送到远端,
  提交并推送, or publish vault changes.
---

# Git Push to Remote（Obsidian Vault 专用）

本 Skill 仅用于当前项目（Obsidian Vault）。通过项目内脚本提交并推送到 `origin`。

**自动同步**：Vault 有文件变更时，Agent 应同时遵循 [@.cursor/skills/auto-sync-remote.md](../auto-sync-remote.md) 与 `.cursor/rules/auto-sync-remote.mdc`。

## 规则

1. **工作目录**：在 Vault 根目录执行（即包含 `.git` 与 `.cursor` 的目录）。
2. **脚本路径**：`.cursor/skills/git-push-remote/scripts/git_push.py`（相对 Vault 根目录）。
3. **默认仓库**：不传 `--repo` 时以当前目录为 Git 根；在 Vault 根执行即可，无需写绝对路径。
4. **不要**在未获用户明确要求时使用 `--force`。
5. 推送失败时根据 stderr 说明原因，不要盲目 `git push --force`。

## 常用命令

在 Vault 根目录执行：

```bash
# 有变更则 add + commit，再 push
python3 .cursor/skills/git-push-remote/scripts/git_push.py -m "docs: update vault"

# 仅推送（工作区须已干净）
python3 .cursor/skills/git-push-remote/scripts/git_push.py --no-commit

# 预览
python3 .cursor/skills/git-push-remote/scripts/git_push.py --dry-run
```

## 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--repo` | Git 仓库路径 | 当前目录 |
| `-m`, `--message` | 提交说明 | `chore: sync local changes` |
| `--remote` | 远端名称 | `origin` |
| `--branch` | 分支 | 当前分支（`main`） |
| `--no-commit` | 只 push | 关闭 |
| `--dry-run` | 预览 | 关闭 |
| `--force` | 强制推送 | 关闭（慎用） |

## Agent 工作流

1. `cd` 到 Vault 根目录（工作区根路径）。
2. 根据用户意图选择 `-m` 或 `--no-commit`。
3. 运行上述 `python3` 命令，将退出码与输出反馈给用户。

## 远端信息

- Remote: `origin` → `git@github.com:chaseh82/obsdian.git`
- 默认分支: `main`
