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

    print("science-agents layout is valid")


if __name__ == "__main__":
    main()
