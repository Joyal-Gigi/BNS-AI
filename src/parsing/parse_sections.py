import json
import re

from config.paths import PROCESSED_DATA_DIR

INPUT_PATH = PROCESSED_DATA_DIR / "BSA2023_clean.txt"
OUTPUT_PATH = PROCESSED_DATA_DIR / "BSA2023_sections.json"

# SECTION_PATTERN = re.compile(r"^\s*(\d{1,3})\.(?=\s|\()")  #for BNS and BNSS

SECTION_PATTERN = re.compile(r"(?m)^\s*(\d{1,3})\.(?=\s|\(|\w)") #for BSA
CHAPTER_PATTERN = re.compile(r"^\s*CHAPTER\s+([IVXLCDM]+)\s*$")


def is_chapter_title(line: str) -> bool:
    """Identify uppercase chapter-title lines."""
    line = line.strip()
    return bool(line) and line.isupper() and not line.startswith("CHAPTER ")


def parse_sections(text: str) -> list[dict]:
    lines = text.splitlines()

    # Locate numbered section headings.
    section_positions = []

    for index, line in enumerate(lines):
        match = SECTION_PATTERN.match(line)
        if match:
            section_positions.append((index, int(match.group(1))))

    sections = []

    chapter_number = None
    chapter_title = None
    pending_section_title = None

    # Process the text before Section 1 as metadata for Section 1.
    first_section_line = section_positions[0][0] if section_positions else len(lines)
    preamble = [line.strip() for line in lines[:first_section_line] if line.strip()]

    for index, line in enumerate(preamble):
        chapter_match = CHAPTER_PATTERN.match(line)

        if chapter_match:
            chapter_number = chapter_match.group(1)

            if index + 1 < len(preamble) and is_chapter_title(preamble[index + 1]):
                chapter_title = f"CHAPTER {preamble[index + 1]}"

        elif (
            index > 0
            and not CHAPTER_PATTERN.match(preamble[index - 1])
            and not is_chapter_title(line)
        ):
            pending_section_title = line.rstrip(".")

    for position, (start_line, section_number) in enumerate(section_positions):
        end_line = (
            section_positions[position + 1][0]
            if position + 1 < len(section_positions)
            else len(lines)
        )

        block = lines[start_line:end_line]

        # A chapter heading inside this block introduces the NEXT section.
        chapter_offset = next(
            (
                offset
                for offset, line in enumerate(block)
                if CHAPTER_PATTERN.match(line)
            ),
            None,
        )

        if chapter_offset is not None:
            # Everything before the chapter heading belongs to this section.
            legal_lines = block[:chapter_offset]
            metadata_lines = [
                line.strip()
                for line in block[chapter_offset:]
                if line.strip()
            ]

            chapter_match = CHAPTER_PATTERN.match(metadata_lines[0])
            next_chapter_number = chapter_match.group(1)

            next_chapter_title = None
            next_section_title = None

            if len(metadata_lines) > 1 and is_chapter_title(metadata_lines[1]):
                next_chapter_title = f"CHAPTER {metadata_lines[1]}"

                if len(metadata_lines) > 2:
                    next_section_title = metadata_lines[2].rstrip(".")

            chapter_number = chapter_number
            chapter_title_for_current = chapter_title
            section_title_for_current = pending_section_title

            # Save metadata for the next section.
            chapter_number = next_chapter_number
            chapter_title = next_chapter_title
            pending_section_title = next_section_title

        else:
            legal_lines = block
            chapter_title_for_current = chapter_title
            section_title_for_current = pending_section_title

            # The last non-empty line before the next numbered section
            # is usually that next section's title.
            if position + 1 < len(section_positions):
                nonempty = [
                    i for i, line in enumerate(legal_lines)
                    if line.strip()
                ]

                if nonempty:
                    last_index = nonempty[-1]
                    candidate = legal_lines[last_index].strip()

                    # Avoid treating numbered provisions or explanatory
                    # labels as section titles.
                    if (
                        not SECTION_PATTERN.match(candidate)
                        and not candidate.startswith(
                            ("Explanation", "Illustration", "Exception")
                        )
                    ):
                        pending_section_title = candidate.rstrip(".")
                        legal_lines = legal_lines[:last_index]

        section_text = "\n".join(legal_lines).strip()

        sections.append(
            {
                "section_number": section_number,
                "chapter_number": chapter_number,
                "chapter_title": chapter_title_for_current,
                "section_title": section_title_for_current,
                "text": section_text,
            }
        )

    return sections


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    text = INPUT_PATH.read_text(encoding="utf-8")
    sections = parse_sections(text)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(sections, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Sections parsed: {len(sections)}")
    print(f"Output saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()