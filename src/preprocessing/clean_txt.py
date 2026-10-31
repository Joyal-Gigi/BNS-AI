import re

from config.paths import PROCESSED_DATA_DIR

INPUT_PATH = PROCESSED_DATA_DIR / "BSA2023.txt"
OUTPUT_PATH = PROCESSED_DATA_DIR / "BSA2023_clean.txt"


def clean_text(text: str) -> str:
    # Remove known PDF headers and navigation text.
    text = re.sub(r"(?m)^\s*Chapters and Sections\s*$", "", text)
    text = re.sub(r"(?m)^\s*HomePage\s*$", "", text)

    # Remove trailing whitespace from each line.
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Reduce three or more consecutive newlines to two.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip() + "\n"


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    text = INPUT_PATH.read_text(encoding="utf-8")
    cleaned_text = clean_text(text)

    OUTPUT_PATH.write_text(cleaned_text, encoding="utf-8")

    print(f"Original characters: {len(text):,}")
    print(f"Cleaned characters:  {len(cleaned_text):,}")
    print(f"Saved cleaned text to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
