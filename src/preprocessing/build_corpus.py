
import json

from config.paths import (
    PROCESSED_DATA_DIR,
    PROCESSED_DOCUMENTS,
    DATABASE_DIR,
    UNIFIED_CORPUS_PATH,
)


REQUIRED_FIELDS = {
    "section_number",
    "chapter_number",
    "chapter_title",
    "section_title",
    "text",
}


def load_document(act_id: str, filename: str) -> list[dict]:
    """Load and validate a processed legal document."""

    file_path = PROCESSED_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError(f"{act_id}: Expected a JSON list.")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(
                f"{act_id}: Record {index} is not a JSON object."
            )

        if set(record.keys()) != REQUIRED_FIELDS:
            raise ValueError(
                f"{act_id}: Invalid schema at record {index}. "
                f"Found: {set(record.keys())}"
            )

    print(f"{act_id}: Loaded {len(records)} records.")

    return records


def build_corpus() -> None:
    """Combine BNS, BNSS and BSA into one corpus."""

    all_records = []
    all_metadata = []

    for act_id, filename in PROCESSED_DOCUMENTS.items():
        records = load_document(act_id, filename)

        all_records.extend(records)
        all_metadata.extend(
            {"act_id": act_id} for _ in records
        )

    corpus = {
        "records": all_records,
        "metadata": all_metadata,
    }

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    with UNIFIED_CORPUS_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            corpus,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print("\nUnified corpus created successfully!")
    print(f"Total records: {len(all_records)}")
    print(f"Output: {UNIFIED_CORPUS_PATH}")


if __name__ == "__main__":
    build_corpus()
