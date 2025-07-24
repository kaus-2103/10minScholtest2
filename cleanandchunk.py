import re
import unicodedata


def clean_ocr_text(raw_text):
    # Normalize Unicode
    text = unicodedata.normalize('NFC', raw_text)

    # Remove unnecessary headers/footers (customize as needed)
    text = re.sub(r'অনলাইন ব্যাচ.*?76916', '', text, flags=re.DOTALL)
    text = re.sub(r'^\d{5,}\s*$', '', text, flags=re.MULTILINE)  # Remove large ID-like numbers

    # Fix broken line breaks (but preserve paragraph breaks)
    text = re.sub(r'[^\S\r\n]+', ' ', text)  # Remove extra spaces but preserve newlines
    text = re.sub(r'(\n\s*){2,}', '\n\n', text)  # Keep double newlines as paragraph breaks

    # Remove repetitive small numbers or misplaced numbering
    text = re.sub(r'^\s*\d+[\.\)]\s*', '', text, flags=re.MULTILINE)

    # Remove unnecessary page numbers or markers (optional)
    text = re.sub(r'\n\s*\d{1,3}\s*\n', '\n', text)

    # Remove single digit English numbers
    text = re.sub(r'\b[0-9]\b', '', text)

    return text.strip()


def smart_chunk(text, max_length=600):
    paragraphs = text.split('\n\n')  # Split by paragraph blocks
    chunks, current_chunk = [], ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Keep Q&A or MCQ blocks together as special case
        if re.match(r'^[০-৯]+\।', para) or re.search(r'উত্তর[:：]', para):
            # Force push current chunk if non-empty
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            chunks.append(para)
            continue

        # Normal chunking by paragraph size
        if len(current_chunk) + len(para) <= max_length:
            current_chunk += para + '\n\n'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + '\n\n'

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def process_ocr_file(input_txt_path, output_chunks_path):
    # Load OCR text
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Clean text
    cleaned_text = clean_ocr_text(raw_text)

    # Chunk text smartly
    chunks = smart_chunk(cleaned_text)

    # Save cleaned + chunked data (as one chunk per block)
    with open(output_chunks_path, 'w', encoding='utf-8') as f:
        for idx, chunk in enumerate(chunks, 1):
            f.write(f"[CHUNK {idx}]\n{chunk}\n\n{'='*50}\n\n")

    print(f"Total {len(chunks)} chunks generated and saved to {output_chunks_path}")


if __name__ == "__main__":
    input_txt = 'data\ocr_bangla_output.txt'          # Path to your OCR result file
    output_txt = 'data\cleaned_chunked_output.txt'    # Destination file

    process_ocr_file(input_txt, output_txt)
