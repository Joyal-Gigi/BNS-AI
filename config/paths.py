from pathlib import Path

#Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

#data
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

#database
DATABASE_DIR = DATA_DIR / "database"
UNIFIED_CORPUS_PATH = DATABASE_DIR / "legal_corpus.json"

#documents
DOCUMENTS = {
    "BNS": {
        "filename": "BNS2023.pdf",
        "act_name": "Bharatiya Nyaya Sanhita, 2023",
    },
    "BNSS": {
        "filename": "BNSS2023.pdf",
        "act_name": "Bharatiya Nagarik Suraksha Sanhita, 2023",
    },
    "BSA": {
        "filename": "BSA2023.pdf",
        "act_name": "Bharatiya Sakshya Adhiniyam, 2023",
    },
}

#processed datasets
PROCESSED_DOCUMENTS = {
    "BNS": "BNS2023_sections.json",
    "BNSS": "BNSS2023_sections.json",
    "BSA": "BSA2023_sections.json",
}
