# Vault 修改后自动同步远端

本说明与项目 Skill **`git-push-remote`**（`@.cursor/skills/git-push-remote`）配合使用。

## 何时触发

在 **Obsidian Vault** 内出现以下任一情况后，**必须在同一轮对话结束前**推送到远端：

- 新建、修改或删除了笔记（`*.md`）或其他 Vault 文件
- 更新了 `.cursor/` 下的 Skill、规则或脚本
- 用户明确要求保存/同步到 GitHub

以下情况**不推送**：

- 仅回答问题、未改动任何文件
- 用户明确说「先不要 push / 不要提交」
- `--dry-run` 预览阶段

## 执行步骤（Agent 必做）

1. 确认工作目录为 Vault 根目录（含 `.git` 的目录）。
2. 根据本次变更写一句简短提交说明（中文或英文均可）。
3. 运行推送脚本：

```bash
cd "/home/mi/文档/Obsidian Vault"
python3 .cursor/skills/git-push-remote/scripts/git_push.py -m "<提交说明>"
```

4. 将脚本 **退出码** 与 **完整输出** 告知用户。
5. 若 push 失败：说明原因，**不要**擅自 `--force`，除非用户明确要求。

## 仅推送、不提交

若变更已由用户手动 `git commit`：

```bash
python3 .cursor/skills/git-push-remote/scripts/git_push.py --no-commit
```

## 预览（不写入 Git）

```bash
python3 .cursor/skills/git-push-remote/scripts/git_push.py --dry-run -m "<提交说明>"
```

## 相关资源

| 资源 | 路径 |
|------|------|
| 推送 Skill | `@.cursor/skills/git-push-remote` |
| 推送脚本 | `.cursor/skills/git-push-remote/scripts/git_push.py` |
| 自动同步规则 | `.cursor/rules/auto-sync-remote.mdc` |

## 远端

- `origin` → `git@github.com:chaseh82/obsdian.git`
- 分支：`main`
