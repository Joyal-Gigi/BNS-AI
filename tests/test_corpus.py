
import json

from config.paths import (
    UNIFIED_CORPUS_PATH,
    PROCESSED_DATA_DIR,
    PROCESSED_DOCUMENTS,
)

EXPECTED_FIELDS = {
    "section_number",
    "chapter_number",
    "chapter_title",
    "section_title",
    "text",
}


def load_corpus():
    with UNIFIED_CORPUS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_corpus_file_exists():
    assert UNIFIED_CORPUS_PATH.exists()


def test_corpus_structure():
    corpus = load_corpus()

    assert "records" in corpus
    assert "metadata" in corpus
    assert isinstance(corpus["records"], list)
    assert isinstance(corpus["metadata"], list)


def test_record_metadata_alignment():
    corpus = load_corpus()

    assert len(corpus["records"]) == len(corpus["metadata"])


def test_all_acts_included():
    corpus = load_corpus()

    act_ids = {
        metadata["act_id"]
        for metadata in corpus["metadata"]
    }

    assert act_ids == {"BNS", "BNSS", "BSA"}


def test_record_schema():
    corpus = load_corpus()

    for record in corpus["records"]:
        assert set(record.keys()) == EXPECTED_FIELDS


def test_metadata_alignment_with_source_counts():
    corpus = load_corpus()

    for act_id, filename in PROCESSED_DOCUMENTS.items():
        source_path = PROCESSED_DATA_DIR / filename

        with source_path.open("r", encoding="utf-8") as file:
            source_records = json.load(file)

        metadata_count = sum(
            metadata["act_id"] == act_id
            for metadata in corpus["metadata"]
        )

        assert metadata_count == len(source_records)


def test_record_preservation():
    corpus = load_corpus()

    for act_id, filename in PROCESSED_DOCUMENTS.items():
        source_path = PROCESSED_DATA_DIR / filename

        with source_path.open("r", encoding="utf-8") as file:
            source_records = json.load(file)

        unified_records = [
            record
            for record, metadata in zip(
                corpus["records"],
                corpus["metadata"],
            )
            if metadata["act_id"] == act_id
        ]

        assert unified_records == source_records
