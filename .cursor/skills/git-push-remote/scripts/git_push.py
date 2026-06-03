#!/usr/bin/env python3
"""Stage, commit (if needed), and push the current Git repository to remote."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

GIT = "/usr/bin/git"


def run(
    args: list[str],
    *,
    cwd: Path,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    cmd = [GIT, *args]
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        text=True,
        capture_output=capture,
    )


def git_output(args: list[str], cwd: Path) -> str:
    result = run(args, cwd=cwd, capture=True)
    return (result.stdout or "").strip()


def find_repo_root(start: Path) -> Path:
    result = run(["rev-parse", "--show-toplevel"], cwd=start, capture=True)
    return Path(result.stdout.strip())


def has_changes(cwd: Path) -> bool:
    return bool(git_output(["status", "--porcelain"], cwd))


def current_branch(cwd: Path) -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"], cwd)


def upstream_ref(cwd: Path) -> str | None:
    try:
        return git_output(
            ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            cwd,
        )
    except subprocess.CalledProcessError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Commit local changes (optional) and push to remote.",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository path (default: current directory)",
    )
    parser.add_argument(
        "-m",
        "--message",
        default="chore: sync local changes",
        help="Commit message when there are uncommitted changes",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Remote name (default: origin)",
    )
    parser.add_argument(
        "--branch",
        help="Branch to push (default: current branch)",
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Only push; fail if there are uncommitted changes",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without executing git write operations",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Pass --force to git push (use with caution)",
    )
    args = parser.parse_args()

    repo = find_repo_root(args.repo.resolve())
    branch = args.branch or current_branch(repo)

    print(f"仓库: {repo}")
    print(f"分支: {branch}")

    dirty = has_changes(repo)
    if dirty:
        if args.no_commit:
            print("错误: 存在未提交变更，且指定了 --no-commit。", file=sys.stderr)
            return 1
        print("检测到未提交变更，将执行 add + commit。")
        if args.dry_run:
            print(f"[dry-run] git add -A && git commit -m {args.message!r}")
        else:
            run(["add", "-A"], cwd=repo)
            run(["commit", "-m", args.message], cwd=repo)
            print(f"已提交: {args.message}")
    else:
        print("工作区干净，跳过提交。")

    upstream = upstream_ref(repo)
    push_args = ["push"]
    if args.force:
        push_args.append("--force")
    if upstream:
        display_target = upstream
    else:
        push_args.extend([args.remote, branch])
        display_target = f"{args.remote}/{branch}"

    if args.dry_run:
        print(f"[dry-run] git {' '.join(push_args)}")
        return 0

    run(push_args, cwd=repo)
    print(f"已推送到远端: {display_target}")
    status = git_output(["status", "-sb"], repo)
    print(status)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        cmd = " ".join(exc.cmd) if exc.cmd else "git"
        err = (exc.stderr or exc.stdout or "").strip()
        print(f"Git 命令失败: {cmd}", file=sys.stderr)
        if err:
            print(err, file=sys.stderr)
        raise SystemExit(exc.returncode or 1) from exc
