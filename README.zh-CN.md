# hermes-ecc-profile（中文）

[English README](./README.md)

这是一个面向 Hermes 的 skill-first 编码 profile，包含：

- 本地工作流/门禁 skills（`woos-*`）
- 导入 skills（`skills/ecc-import/*`）
- agent 适配 skills（`skills/ecc-agent-skills/*`）

## 安装内容

1. 本地 workflow skills：
   - `woos-development-workflow`
   - `woos-prd-authoring`
   - `woos-prd-review-gate`
   - `woos-feature-design`
   - `woos-design-review-gate`
   - `woos-code-review-gate`
   - `woos-pr-readiness`
2. 导入 skills：
   - `git-workflow`
   - `search-first`
   - `dmux-workflows`
   - `product-capability`
   - `tdd-workflow`
   - `coding-standards`
   - `verification-loop`
3. agent 适配 skills：
   - `planner`
   - `architect`
   - `code-reviewer`
   - `security-reviewer`

## 安装

```bash
cd /path/to/hermes-ecc-profile
./install-profile.sh
```

脚本会提示输入本地 ECC 仓库路径。

可选参数：

```bash
./install-profile.sh --ecc-path /path/to/ecc --profile-root ~/.hermes/profiles/coding --install-soul
```

默认安装目录（`~/.hermes/profiles/coding`）：

- `skills/software-development/*`（本地 workflow skills）
- `skills/ecc-import/*`（导入 skills）
- `skills/ecc-agent-skills/*`（agent 适配 skills）
- `SOUL.md`（仅 `--install-soul` 时安装）


## 升级流程（ECC 更新后）

agent 适配 skills 中包含源追踪字段：

- `ecc_source_repo`
- `ecc_source_path`
- `ecc_source_commit`

当 ECC 升级后，对比这些 commit 与 ECC 当前历史；若有变化，重新做一次 adapter 转换。

## Hermes 中的规则使用

Hermes 默认不走 ECC 风格的独立 `rules/` 目录加载。  
建议通过项目上下文文件进行规则路由：

- `.hermes.md` / `HERMES.md`（推荐）
- `AGENTS.md`
- `.cursorrules` 或 `.cursor/rules/*.mdc`

全局原则放在 `SOUL.md`，项目/语言规则放在项目上下文文件中。
