#!/usr/bin/env sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skills_home=${SCIENCE_AGENTS_SKILLS_HOME:-${AGENTS_HOME:-$HOME/.agents}/skills}

mkdir -p "$skills_home"

for skill_path in "$repository_root"/skills/*; do
    [ -f "$skill_path/SKILL.md" ] || continue
    skill_name=$(basename "$skill_path")
    target_path=$skills_home/$skill_name

    if [ -e "$target_path" ] || [ -L "$target_path" ]; then
        printf 'skip: %s already exists\n' "$target_path"
        continue
    fi

    ln -s "$skill_path" "$target_path"
    printf 'linked: %s -> %s\n' "$target_path" "$skill_path"
done
