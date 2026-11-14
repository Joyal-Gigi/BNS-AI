
import json
import numpy as np

from sentence_transformers import SentenceTransformer

from config.paths import CHUNKS_PATH, EMBEDDINGS_PATH

MODEL_NAME = "BAAI/bge-m3"

MAX_TOKENS = 8192
WINDOW_OVERLAP = 512
BATCH_SIZE = 4


def load_chunks() -> list[dict]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_PATH}"
        )

    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or "chunks" not in data:
        raise ValueError("Invalid chunks file structure.")

    chunks = data["chunks"]

    if not isinstance(chunks, list) or not chunks:
        raise ValueError("No chunks found.")

    required_fields = {
        "chunk_id",
        "act_id",
        "section_number",
        "chapter_number",
        "chapter_title",
        "section_title",
        "text",
    }

    for index, chunk in enumerate(chunks):
        if not isinstance(chunk, dict):
            raise ValueError(f"Invalid chunk at index {index}.")

        if not required_fields.issubset(chunk.keys()):
            raise ValueError(f"Missing fields in chunk {index}.")

    print(f"Loaded {len(chunks)} legal sections.")
    return chunks




def create_windows(text: str, tokenizer, max_tokens: int) -> list[str]:
    # Tokenize the complete section without truncation.
    token_ids = tokenizer(
        text,
        add_special_tokens=False,
        truncation=False,
        verbose=False,
    )["input_ids"]

    # Reserve space for special tokens added by the model.
    special_tokens = tokenizer.num_special_tokens_to_add(pair=False)
    content_limit = max_tokens - special_tokens

    step = content_limit - WINDOW_OVERLAP
    windows = []

    for start in range(0, len(token_ids), step):
        window_ids = token_ids[start:start + content_limit]

        if not window_ids:
            break

        window_text = tokenizer.decode(
            window_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )

        windows.append(window_text)

        if start + content_limit >= len(token_ids):
            break

    return windows



def generate_embeddings(chunks: list[dict]) -> None:
    print(f"\nLoading model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print(f"Model maximum sequence length: {model.max_seq_length}")
    print(
        f"Embedding dimensions: "
        f"{model.get_embedding_dimension()}"
    )

    all_embeddings = []
    chunk_ids = []

    total_windows = 0
    oversized_sections = 0

    for index, chunk in enumerate(chunks, start=1):
        chunk_id = chunk["chunk_id"]
        text = chunk["text"]

        windows = create_windows(
                text,
                model.tokenizer,
                model.max_seq_length,
            )

        if len(windows) > 1:
            oversized_sections += 1

        total_windows += len(windows)

        window_embeddings = model.encode(
            windows,
            batch_size=BATCH_SIZE,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        # Average the window embeddings.
        section_embedding = np.mean(
            window_embeddings,
            axis=0,
        )

        # Normalize the final section embedding.
        section_embedding = section_embedding / np.linalg.norm(
            section_embedding
        )

        all_embeddings.append(section_embedding)
        chunk_ids.append(chunk_id)

        if index % 50 == 0 or index == len(chunks):
            print(
                f"Processed {index}/{len(chunks)} sections."
            )

    embeddings = np.array(all_embeddings, dtype=np.float32)

    EMBEDDINGS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.savez_compressed(
        EMBEDDINGS_PATH,
        chunk_ids=np.array(chunk_ids),
        embeddings=embeddings,
    )

    print("\nEmbedding generation completed!")
    print(f"Total sections: {len(chunks)}")
    print(f"Total windows: {total_windows}")
    print(f"Sections using multiple windows: {oversized_sections}")
    print(f"Embedding shape: {embeddings.shape}")
    print(f"Saved to: {EMBEDDINGS_PATH}")


def main() -> None:
    chunks = load_chunks()
    generate_embeddings(chunks)


if __name__ == "__main__":
    main()
