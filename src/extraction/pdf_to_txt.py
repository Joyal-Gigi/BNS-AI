import pymupdf

from config.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

PDF_PATH = RAW_DATA_DIR / "BSA2023.pdf"
OUTPUT_PATH = PROCESSED_DATA_DIR / "BSA2023.txt"

START_PAGE = 26  # Human-readable PDF page number


def extract_text() -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with pymupdf.open(PDF_PATH) as pdf:
        if len(pdf) < START_PAGE:
            raise ValueError(
                f"PDF has only {len(pdf)} pages; "
                f"cannot start from page {START_PAGE}."
            )

        with OUTPUT_PATH.open("w", encoding="utf-8") as output:
            for page_index in range(START_PAGE - 1, len(pdf)):
                page = pdf[page_index]
                text = page.get_text("text")

                output.write(text)
                output.write("\n")

    # print(f"Extracted pages {START_PAGE}-{len(pdf)}.")
    print(f"Saved text to: {OUTPUT_PATH}")


if __name__ == "__main__":
    extract_text()
