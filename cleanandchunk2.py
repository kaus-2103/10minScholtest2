INPUT_FILE = "main_text.txt"
OUTPUT_FILE = "meaning_chunked_output.txt"

meaning_chunks = []
current_chunk = ""

def is_end_of_chunk(sentence):
    # Bengali sentence end markers: ।, !, ?, …
    return sentence.endswith("।") or sentence.endswith("!") or sentence.endswith("?") or sentence.endswith("…")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        sentence = line.strip().replace("\n", " ")
        if not sentence:
            continue
        current_chunk += sentence + " "
        if is_end_of_chunk(sentence):
            meaning_chunks.append(current_chunk.strip())
            current_chunk = ""

if current_chunk:
    meaning_chunks.append(current_chunk.strip())

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(meaning_chunks, 1):
        f.write(f"[MEANING CHUNK {i}]\n{chunk}\n{'='*50}\n")

print(f"✅ Saved {len(meaning_chunks)} meaning-based chunks to {OUTPUT_FILE}")
