# Installation

`install.sh` links the repository's portable skills into a global Agent Skills directory. It does not create or store runtime state.

## Figure environment

Create or update the publication-figure environment, register its Jupyter kernel, and run the smoke test:

```bash
./install/create-science-figures.sh
```

The installer uses `mamba` from `PATH`, or the Mamba executable in the `admin` environment used on `blue`. Set `SCIENCE_FIGURE_MAMBA` to override discovery.

The equivalent environment-creation command is:

```bash
mamba env create \
  --strict-channel-priority \
  --override-channels \
  --file install/conda/science-figures.yml
```

Register it manually as a Jupyter kernel:

```bash
conda run --name science-figures \
  python -m ipykernel install \
  --user \
  --name science-figures \
  --display-name "Python (science-figures)"
```

Run the smoke test manually without storing generated figures in the repository:

```bash
conda run --name science-figures \
  python tests/figure_environment_smoke.py
```
