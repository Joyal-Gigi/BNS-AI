
import json

from config.paths import (
    UNIFIED_CORPUS_PATH,
    DATABASE_DIR,
    CHUNKS_PATH,
)


REQUIRED_FIELDS = {
    "act_id",
    "section_number",
    "chapter_number",
    "chapter_title",
    "section_title",
    "text",
}


def load_corpus() -> list[dict]:
    """Load and validate the unified legal corpus."""

    if not UNIFIED_CORPUS_PATH.exists():
        raise FileNotFoundError(
            f"Unified corpus not found: {UNIFIED_CORPUS_PATH}"
        )

    with UNIFIED_CORPUS_PATH.open("r", encoding="utf-8") as file:
        corpus = json.load(file)

    if not isinstance(corpus, dict) or "records" not in corpus:
        raise ValueError("Invalid corpus structure.")

    records = corpus["records"]

    if not isinstance(records, list):
        raise ValueError("Corpus records must be a list.")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"Invalid record at index {index}.")

        if set(record.keys()) != REQUIRED_FIELDS:
            raise ValueError(
                f"Invalid schema at record {index}."
            )

    print(f"Loaded {len(records)} legal sections.")

    return records


def generate_chunks(records: list[dict]) -> list[dict]:
    """Generate one chunk for each complete legal section."""

    chunks = []

    for record in records:
        chunk = {
            "chunk_id": (
                f"{record['act_id']}_{record['section_number']:03d}"
            ),
            **record,
        }

        chunks.append(chunk)

    return chunks


def save_chunks(chunks: list[dict]) -> None:
    """Save generated chunks to a JSON file."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    with CHUNKS_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            {"chunks": chunks},
            file,
            ensure_ascii=False,
            indent=4,
        )

    print(f"Saved {len(chunks)} chunks to: {CHUNKS_PATH}")


def main() -> None:
    records = load_corpus()

    chunks = generate_chunks(records)

    save_chunks(chunks)

    print("\nChunk generation completed successfully!")
    print(f"Total sections: {len(records)}")
    print(f"Total chunks: {len(chunks)}")


if __name__ == "__main__":
    main()
