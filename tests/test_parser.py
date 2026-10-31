import json

from config.paths import PROCESSED_DATA_DIR


JSON_PATH = PROCESSED_DATA_DIR / "BNS2023_sections.json"


def load_sections() -> list[dict]:
    with JSON_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_section_count():
    sections = load_sections()
    assert len(sections) == 358


def test_section_numbering():
    sections = load_sections()
    numbers = [section["section_number"] for section in sections]

    assert numbers == list(range(1, 359))


def test_required_fields():
    sections = load_sections()
    required_fields = {
        "section_number",
        "chapter_number",
        "chapter_title",
        "section_title",
        "text",
    }

    for section in sections:
        assert required_fields.issubset(section.keys())
        assert isinstance(section["text"], str)
        assert section["text"].strip()


def test_section_1():
    sections = load_sections()
    section = next(s for s in sections if s["section_number"] == 1)

    assert "Bharatiya Nyaya Sanhita, 2023" in section["text"]


def test_section_4_metadata():
    sections = load_sections()
    section = next(s for s in sections if s["section_number"] == 4)

    assert section["chapter_number"] == "II"
    assert section["chapter_title"] == "CHAPTER OF PUNISHMENTS"
    assert section["section_title"] == "Punishments"
    assert section["text"].startswith("4.")


def test_section_3_boundary():
    sections = load_sections()
    section = next(s for s in sections if s["section_number"] == 3)

    assert "CHAPTER II" not in section["text"]
    assert "Punishments." not in section["text"]


def test_section_358_completeness():
    sections = load_sections()
    section = next(s for s in sections if s["section_number"] == 358)

    for marker in ["(1)", "(2)", "(3)", "(4)"]:
        assert marker in section["text"]

    # Normalize whitespace so line breaks don't cause false failures.
    normalized_text = " ".join(section["text"].split())

    assert "General Clauses Act, 1897" in normalized_text