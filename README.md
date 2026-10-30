# NyayaAI 🇮🇳

### AI-Powered Indian Legal Information Platform

**Making Indian legislation easier to understand through structured legal data, intelligent search, and AI-powered explanations.**

NyayaAI is an open-source project aimed at making Indian legal information more accessible. It combines data extraction, structured legal databases, hybrid search, and Retrieval-Augmented Generation (RAG) to help users explore legislation and understand legal provisions in simple language.

The initial version focuses on India's three new criminal laws: the Bharatiya Nyaya Sanhita (BNS), the Bharatiya Nagarik Suraksha Sanhita (BNSS), and the Bharatiya Sakshya Adhiniyam (BSA).

> 🚧 **Project Status: In Development**
>
> The initial milestone focuses on building and validating the legal data extraction pipeline. Features described in the roadmap represent planned functionality and may not yet be implemented.

## 🎯 Objectives

- Extract and structure legal provisions from official government publications.
- Build a searchable database of individual legal sections.
- Implement exact section lookup and keyword-based search.
- Explore semantic search using vector embeddings.
- Develop a RAG-based assistant that explains retrieved legal provisions in simple language.
- Provide source references so users can verify the underlying legislation.
- Explore multilingual support, including Malayalam.

## ⚖️ Initial Legal Scope

| Legislation | Focus |
|---|---|
| Bharatiya Nyaya Sanhita, 2023 (BNS) | Criminal offences and punishments |
| Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) | Criminal procedure |
| Bharatiya Sakshya Adhiniyam, 2023 (BSA) | Law of evidence |

### Official Resources

- [India Code](https://www.indiacode.nic.in/)
- [Bharatiya Nyaya Sanhita, 2023 — Official PDF](https://www.indiacode.nic.in/bitstream/123456789/20062/1/a2023-45.pdf)
- [Ministry of Home Affairs — Judicial Division](https://www.mha.gov.in/en/commoncontent/judicial-division)
- [National Crime Records Bureau — New Criminal Laws Portal](https://www.ncrb.mha.gov.in/uploads/SankalanPortal/Index.html)

## 🏗️ Planned Architecture

```text
Official Government Sources
          |
          v
     Data Extraction
          |
          v
    Raw Legal Documents
          |
          v
   Text Processing & Cleaning
          |
          v
   Section-Level Validation
          |
          v
 Structured Legal Dataset
          |
          v
      SQLite Database
          |
          v
    Hybrid Search Engine
      /           \
     v             v
Keyword Search  Semantic Search
      \           /
          v
     Relevant Legal Text
          |
          v
      RAG Pipeline
          |
          v
 AI-Generated Explanation
          |
          v
 Citations to Legal Sources
```

## 🛠️ Technology Stack

The following technologies are planned for the project.

| Technology | Purpose |
|---|---|
| Python | Data processing and application logic |
| Requests | HTTP requests to public sources |
| Beautiful Soup | HTML parsing and web scraping |
| PyMuPDF | PDF text extraction |
| JSON | Structured legal data |
| SQLite | Persistent storage and exact lookup |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector storage and semantic retrieval |
| Ollama | Local LLM experimentation |
| FastAPI | Backend API |
| Streamlit | Interactive user interface |
| Pytest | Automated testing |

## 📂 Project Structure

```text
NyayaAI/
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
├── src/
│   ├── extraction/
│   ├── processing/
│   ├── validation/
│   └── database/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔍 Key Engineering Principles

### 1. Reliable Legal Data Extraction
Extract legal text while preserving section numbers, subsections, provisos, explanations, and exceptions.

### 2. Data Quality and Validation
Implement checks for missing records, duplicate sections, empty content, and discrepancies between extracted text and official publications.

### 3. Hybrid Retrieval
Combine exact section lookup and keyword search with semantic retrieval to improve the relevance of search results.

### 4. Source-Grounded AI
Design the assistant to generate explanations from retrieved legal provisions rather than relying solely on the language model's internal knowledge.

### 5. Traceability
Associate each legal record with source information so users can inspect and verify the original text.

### 6. Privacy and Local Development
Explore local inference and local data storage to reduce dependence on paid external services during development.

## 🗺️ Roadmap

- [x] Set up the Python project and development environment.
- [ ] Identify and download official legislation sources.
- [ ] Extract legal text from the BNS.
- [ ] Structure individual sections into JSON records.
- [ ] Validate extracted records against the official publication.
- [ ] Store validated sections in SQLite.
- [ ] Implement exact section lookup.
- [ ] Add keyword-based search.
- [ ] Implement semantic retrieval using embeddings.
- [ ] Integrate a local language model.
- [ ] Build the RAG question-answering pipeline.
- [ ] Add citations and source verification.
- [ ] Develop a Streamlit interface.
- [ ] Expand coverage to the BNSS and BSA.
- [ ] Explore Malayalam-language support.
- [ ] Add automated evaluation and regression tests.

## ⚠️ Disclaimer

NyayaAI is an educational and informational project. It is intended to help users discover and understand publicly available legal information.

It does not provide professional legal advice, establish whether a person has committed an offence, or replace consultation with a qualified legal professional.

AI-generated explanations may be incomplete or incorrect. Users should verify relevant provisions against official legal publications and consult a qualified professional when necessary.

## 🤝 Contributions

Contributions, suggestions, and issue reports are welcome as the project develops.

Potential areas for contribution include legal data extraction, text validation, search quality, retrieval evaluation, documentation, and multilingual accessibility.

## 📜 License

The project's original code is intended to be released under the MIT License. Official legal documents and third-party resources remain subject to their respective terms and conditions.

---

**NyayaAI — Making Indian law easier to explore and understand. 🇮🇳**