#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


LOCAL_SOFTWARE_DEV_SKILLS = [
    "woos-development-workflow",
    "woos-feature-design",
    "woos-design-review-gate",
    "woos-executable-acceptance-gate",
    "woos-failure-state-machine",
    "woos-deviation-control-gate",
    "woos-run-orchestrator",
    "woos-human-handoff",
    "woos-workflow-memory",
    "woos-review-context",
    "woos-agent-decision",
    "woos-code-review-gate",
    "woos-pr-readiness",
    "woos-story-decomposition",
    "woos-systematic-debugging",
    "woos-setup-rules",
    "woos-ecc-production-audit",
    "woos-architect",
    "woos-product-planner",
    "woos-code-reviewer",
    "woos-security-reviewer",
]

ECC_SKILLS = [
    "git-workflow",
    "tdd-workflow",
    "coding-standards",
    "verification-loop",
    "api-design",
    "browser-qa",
    "security-review",
    "architecture-decision-records",
    "e2e-testing",
    "deployment-patterns",
    "database-migrations",
    "codebase-onboarding",
]




def style(text: str, code: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


def print_header() -> None:
    print()
    print(style("Hermes ECC Profile Installer", "1;36"))
    print(style("-" * 32, "36"))
    print("Interactive setup mode (press Enter to accept defaults).")


def print_step(label: str) -> None:
    print()
    print(style(label, "1"))


def prompt_text(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("Please enter a value.")


def validate_vendor_path(vendor_path: Path) -> str | None:
    if not vendor_path.is_dir():
        return f"Path does not exist: {vendor_path}"
    if not (vendor_path / "skills").is_dir():
        return f"Missing skills/: {vendor_path}"
    return None


def fail(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def prompt_yes_no(question: str, default_yes: bool = True) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    default = "y" if default_yes else "n"
    while True:
        reply = input(f"{question} {suffix} ").strip().lower() or default
        if reply in {"y", "yes"}:
            return True
        if reply in {"n", "no"}:
            return False
        print("Please answer y or n.")


def copy_dir(src: Path, dst: Path) -> None:
    if not src.is_dir():
        fail(f"Missing skill directory: {src}")
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def iter_local_skill_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.iterdir() if path.is_dir())


def ensure_backup(profile_root: Path, backup_enabled: bool, backup_dir: Path | None) -> Path | None:
    if not profile_root.exists() or not profile_root.is_dir():
        return None
    if not any(profile_root.iterdir()):
        return None
    if not backup_enabled:
        return None

    if backup_dir is None:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = Path(f"{str(profile_root).rstrip('/')}.backup.{ts}")
    if backup_dir.exists():
        fail(f"Backup path already exists: {backup_dir}")
    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(profile_root, backup_dir)
    print(f"  ✓ profile backup created: {backup_dir}")
    return backup_dir


def install_core_skills(script_dir: Path, profile_root: Path, vendor_path: Path) -> None:
    (profile_root / "skills" / "product-design").mkdir(parents=True, exist_ok=True)
    (profile_root / "skills" / "software-development").mkdir(parents=True, exist_ok=True)
    (profile_root / "skills" / "ecc-import").mkdir(parents=True, exist_ok=True)

    for skill_dir in iter_local_skill_dirs(script_dir / "skills" / "product-design"):
        copy_dir(skill_dir, profile_root / "skills" / "product-design" / skill_dir.name)
        print(f"  ✓ product-design skill: {skill_dir.name}")

    for skill in LOCAL_SOFTWARE_DEV_SKILLS:
        copy_dir(script_dir / "skills" / "software-development" / skill, profile_root / "skills" / "software-development" / skill)
        print(f"  ✓ software-dev skill: {skill}")

    for skill in ECC_SKILLS:
        copy_dir(vendor_path / "skills" / skill, profile_root / "skills" / "ecc-import" / skill)
        print(f"  ✓ vendored ecc skill: {skill}")


def install_profile_soul(script_dir: Path, profile_root: Path) -> None:
    soul_src = script_dir / "SOUL.md"
    if not soul_src.is_file():
        fail("Missing SOUL.md in profile repo")
    shutil.copy2(soul_src, profile_root / "SOUL.md")
    print("  ✓ profile SOUL.md installed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Hermes ECC skill collection")
    parser.add_argument("--profile-root", help="Target profile / skills root")
    parser.add_argument("--install-soul", action="store_true", help="Install SOUL.md into profile root")
    parser.add_argument("--backup-dir", help="Backup destination path for existing profile root")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup of existing profile root")
    return parser.parse_args()


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    args = parse_args()
    interactive_mode = args.profile_root is None or not args.install_soul

    vendor_path = script_dir / "vendor" / "ecc"
    issue = validate_vendor_path(vendor_path)
    if issue is not None:
        fail(
            f"Invalid vendored ECC snapshot: {issue}\n"
            "Run scripts/refresh-ecc-vendor.sh <path-to-ecc-repo> to populate it."
        )

    profile_root_default = Path(
        os.environ.get("HERMES_PROFILE_ROOT", str(Path.home() / ".hermes" / "profiles" / "coding"))
    ).expanduser()
    profile_root = Path(args.profile_root).expanduser() if args.profile_root else profile_root_default

    install_soul = args.install_soul
    install_soul_set = args.install_soul
    backup_enabled = not args.no_backup
    backup_set = args.no_backup or bool(args.backup_dir)
    backup_dir = Path(args.backup_dir).expanduser() if args.backup_dir else None
    backup_done = False

    if interactive_mode:
        print_header()
        print(f"Vendored ECC snapshot: {vendor_path}")

    if not args.profile_root:
        if interactive_mode:
            print_step("Step 1/2 - Profile target + core skills")
        profile_root_input = prompt_text("Profile root", str(profile_root_default))
        profile_root = Path(profile_root_input).expanduser()

    if not backup_set and profile_root.is_dir() and any(profile_root.iterdir()):
        backup_enabled = prompt_yes_no("Backup existing profile root before install?", True)
        if backup_enabled:
            backup_dir = ensure_backup(profile_root, True, backup_dir)
            backup_done = True

    if not backup_done:
        backup_dir = ensure_backup(profile_root, backup_enabled, backup_dir)

    if interactive_mode:
        print(f"Target profile: {profile_root}")
        print("Applying core skill installation now...")
    install_core_skills(script_dir, profile_root, vendor_path)

    if not install_soul_set:
        if interactive_mode:
            print_step("Step 2/2 - SOUL.md")
        install_soul = prompt_yes_no("Install SOUL.md into profile root?", True)
    if install_soul:
        install_profile_soul(script_dir, profile_root)

    print("\nInstall complete.")
    print(f"Profile root: {profile_root}")
    print(f"Vendored ECC snapshot: {vendor_path}")
    if backup_dir is not None and backup_enabled:
        print(f"Backup: {backup_dir}")


if __name__ == "__main__":
    main()
