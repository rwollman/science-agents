#!/usr/bin/env sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
environment_file=$repository_root/install/conda/science-figures.yml
environment_name=science-figures

if [ -n "${SCIENCE_FIGURE_MAMBA:-}" ]; then
    mamba_executable=$SCIENCE_FIGURE_MAMBA
elif command -v mamba >/dev/null 2>&1; then
    mamba_executable=$(command -v mamba)
elif [ -x "$HOME/miniconda3/envs/admin/bin/mamba" ]; then
    mamba_executable=$HOME/miniconda3/envs/admin/bin/mamba
else
    printf '%s\n' \
        'Mamba was not found. Set SCIENCE_FIGURE_MAMBA to its executable path.' >&2
    exit 1
fi

if "$mamba_executable" run --name "$environment_name" \
    python -c 'import sys; sys.exit(0)' >/dev/null 2>&1; then
    "$mamba_executable" env update \
        --yes \
        --no-rc \
        --prune \
        --file "$environment_file"
else
    "$mamba_executable" env create \
        --yes \
        --strict-channel-priority \
        --override-channels \
        --file "$environment_file"
fi

"$mamba_executable" run --name "$environment_name" \
    python -m ipykernel install \
    --user \
    --name "$environment_name" \
    --display-name "Python (science-figures)"

"$mamba_executable" run --name "$environment_name" \
    python "$repository_root/tests/figure_environment_smoke.py"
