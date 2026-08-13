from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("science-analysis", "science-figure", "science-review")
REQUIRED_DIRECTORIES = ("agents", "scripts", "install", "docs", "tests", "examples")


def main() -> None:
    for directory in REQUIRED_DIRECTORIES:
        assert (ROOT / directory).is_dir(), f"missing directory: {directory}"

    for name in SKILLS:
        skill_file = ROOT / "skills" / name / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        assert re.search(rf"^name: {re.escape(name)}$", text, re.MULTILINE)
        assert re.search(r"^description: .+", text, re.MULTILINE)

    environment_file = ROOT / "install" / "conda" / "science-figures.yml"
    environment_text = environment_file.read_text(encoding="utf-8")
    assert re.search(r"^name: science-figures$", environment_text, re.MULTILINE)
    assert "  - conda-forge\n" in environment_text
    assert "  - nodefaults\n" in environment_text
    assert "  - python=3.12\n" in environment_text
    assert (ROOT / "tests" / "figure_environment_smoke.py").is_file()
    assert (ROOT / "install" / "create-science-figures.sh").is_file()

    print("science-agents layout is valid")


if __name__ == "__main__":
    main()
