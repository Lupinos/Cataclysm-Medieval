#!/bin/bash
set -euo pipefail
repo_root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
git -C "$repo_root" config --local core.hooksPath .githooks
echo '已启用仓库 Git 提交钩子；process 由当前 agent 核对和补充。'
