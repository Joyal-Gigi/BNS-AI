import re

from config.paths import PROCESSED_DATA_DIR

INPUT_PATH = PROCESSED_DATA_DIR / "BSA2023_clean.txt"


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"File not found: {INPUT_PATH}")

    text = INPUT_PATH.read_text(encoding="utf-8")

    # Find section numbers appearing at the start of a line.
    # section_numbers = re.findall(r"(?m)^(\d{1,3})\.(?=\s|\()", text)
    # section_numbers = re.findall(r"(?m)^\s*(\d{1,3})\.(?=\s|\()", text)
    section_numbers = re.findall(r"(?m)^\s*(\d{1,3})\.(?=\s|\(|\w)", text)
    numbers = [int(number) for number in section_numbers]

    print(f"Total characters: {len(text):,}")
    print(f"Total lines: {len(text.splitlines()):,}")
    print(f"Section headings detected: {len(numbers)}")
    print(f"First section numbers: {numbers[:10]}")
    print(f"Last section numbers: {numbers[-10:]}")
    print(f"Missing section numbers: {sorted(set(range(1, 359)) - set(numbers))}")

    print("\nChapter headings:")
    chapters = re.findall(r"(?mi)^CHAPTER\s+[IVXLCDM]+\s*$", text)
    print(f"Total chapter headings detected: {len(chapters)}")


if __name__ == "__main__":
    main()