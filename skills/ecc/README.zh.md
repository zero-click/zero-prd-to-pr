# ECC Skills（上游快照）

[English](./README.md) | [中文](./README.zh.md)

本地工作流依赖的上游 ECC（Everything Claude Code）skill 的一份冻结快照。

**不要手改。** 这个目录由 `scripts/refresh-ecc-skills.sh` 整体重写。本地扩展请放到 `skills/software-development/`（用 `woos-` 前缀）或 `skills/product-design/`。

## 刷新

```bash
scripts/refresh-ecc-skills.sh /path/to/everything-claude-code
git diff skills/ecc
git add skills/ecc && git commit
```

## 上游

<https://github.com/everything-claude-code/everything-claude-code>

## 备注

- `production-audit` 已被上游移除。本地重写版位于 `skills/software-development/woos-production-audit/`。
