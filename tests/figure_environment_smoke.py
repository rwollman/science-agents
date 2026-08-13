#!/usr/bin/env python3
"""Exercise the scientific figure runtime and export publication formats."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
from pathlib import Path
import tempfile

import cairosvg
import jupyter_client
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)

import matplotlib.pyplot as plt
import nbformat
import numpy as np
import pandas as pd
from PIL import Image
import requests
import scipy
from scipy import stats
import seaborn as sns
from skimage import io as skimage_io
import statsmodels.api as sm
import websocket
import yaml


PACKAGE_NAMES = (
    "CairoSVG",
    "ipykernel",
    "ipympl",
    "jupyter-client",
    "jupyterlab",
    "matplotlib",
    "nbformat",
    "numpy",
    "pandas",
    "Pillow",
    "PyYAML",
    "requests",
    "scikit-image",
    "scipy",
    "seaborn",
    "statsmodels",
    "websocket-client",
)


def build_figure(output_dir: Path) -> dict[str, object]:
    rng = np.random.default_rng(20260813)
    groups = ("Control", "Treatment A", "Treatment B")
    centers = (1.0, 1.35, 1.7)
    frame = pd.DataFrame(
        {
            "group": np.repeat(groups, 16),
            "value": np.concatenate(
                [rng.normal(center, 0.18, 16) for center in centers]
            ),
        }
    )

    summary = frame.groupby("group", observed=True)["value"].agg(["mean", "count", "std"])
    summary = summary.reindex(groups)
    summary["sem"] = summary["std"] / np.sqrt(summary["count"])
    summary["ci95"] = summary["sem"] * stats.t.ppf(
        0.975, summary["count"] - 1
    )

    design = pd.get_dummies(frame["group"], drop_first=True, dtype=float)
    design = sm.add_constant(design)
    model = sm.OLS(frame["value"], design).fit()

    sns.set_theme(style="ticks", context="paper")
    palette = ("#4477AA", "#EE6677", "#228833")
    figure, axis = plt.subplots(figsize=(6.5, 4.0), constrained_layout=True)
    sns.stripplot(
        data=frame,
        x="group",
        y="value",
        hue="group",
        order=groups,
        hue_order=groups,
        palette=palette,
        jitter=0.12,
        size=4.5,
        alpha=0.72,
        legend=False,
        ax=axis,
    )
    axis.errorbar(
        np.arange(len(groups)),
        summary["mean"],
        yerr=summary["ci95"],
        fmt="o",
        color="#111111",
        markersize=5,
        capsize=4,
        linewidth=1.3,
        label="Mean and 95% CI",
        zorder=10,
    )
    axis.set(xlabel="Condition", ylabel="Normalized response")
    axis.set_title("Science figure environment smoke test", loc="left", weight="bold")
    axis.legend(frameon=False, loc="upper left")
    sns.despine(ax=axis)

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "png": output_dir / "figure-smoke.png",
        "svg": output_dir / "figure-smoke.svg",
        "pdf": output_dir / "figure-smoke.pdf",
        "svg_preview": output_dir / "figure-smoke-from-svg.png",
    }
    figure.savefig(outputs["png"], dpi=300)
    figure.savefig(outputs["svg"])
    figure.savefig(outputs["pdf"])
    plt.close(figure)

    cairosvg.svg2png(
        url=str(outputs["svg"]),
        write_to=str(outputs["svg_preview"]),
        output_width=650,
        output_height=400,
    )

    for path in outputs.values():
        if not path.is_file() or path.stat().st_size < 1_000:
            raise AssertionError(f"missing or unexpectedly small output: {path}")

    with Image.open(outputs["png"]) as image:
        if image.size != (1950, 1200):
            raise AssertionError(f"unexpected PNG dimensions: {image.size}")
        image.verify()

    svg_preview = skimage_io.imread(outputs["svg_preview"])
    if tuple(svg_preview.shape[:2]) != (400, 650):
        raise AssertionError(
            f"unexpected rasterized SVG dimensions: {svg_preview.shape[:2]}"
        )

    if not outputs["pdf"].read_bytes().startswith(b"%PDF"):
        raise AssertionError("PDF signature is missing")
    if "<svg" not in outputs["svg"].read_text(encoding="utf-8")[:1_000]:
        raise AssertionError("SVG root element is missing")

    notebook = nbformat.v4.new_notebook(
        cells=[nbformat.v4.new_code_cell("import matplotlib; matplotlib.__version__")]
    )
    if notebook.nbformat != 4:
        raise AssertionError("failed to create a v4 notebook")

    # Exercise imports that persistent_jupyter needs without making network calls.
    if not jupyter_client.__version__ or not requests.__version__ or not websocket.__version__:
        raise AssertionError("notebook transport dependencies did not import correctly")
    if not scipy.__version__ or not yaml.__version__:
        raise AssertionError("scientific dependencies did not import correctly")

    return {
        "environment": "science-figures",
        "formats": {name: str(path) for name, path in outputs.items()},
        "model_r_squared": round(float(model.rsquared), 6),
        "packages": {
            name: importlib.metadata.version(name) for name in PACKAGE_NAMES
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Keep smoke-test artifacts in this directory instead of a temporary directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.output_dir:
        report = build_figure(args.output_dir.resolve())
        print(json.dumps(report, indent=2, sort_keys=True))
        return

    with tempfile.TemporaryDirectory(prefix="science-figures-smoke-") as directory:
        report = build_figure(Path(directory))
        print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
