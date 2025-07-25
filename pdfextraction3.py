import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🚫 Noise filter
def is_noise(text):
    text = text.strip()

    # Empty or too short
    if len(text) < 10:
        return True

    # Only digits or symbols
    if re.fullmatch(r"[\[\]()\d\s:|.]+", text):
        return True

    # Page footer/header stuff
    noise_keywords = [
        "এইচএসসি", "বাংলা ১ম পত্র", "বাংলা প্রথম পত্র",
        "পৃষ্ঠা", "পরীক্ষার জন্য নয়", "অভ্যন্তরীণ", "শিক্ষার্থী","অনলাইন ব্যাচ"
    ]
    if any(kw in text for kw in noise_keywords):
        return True

    return False

# 📦 Merge cleaned paragraphs into ~500-char chunks
def merge_into_chunks(clean_paragraphs, max_chunk_size=500):
    chunks = []
    current = ""

    for para in clean_paragraphs:
        if len(current) + len(para) + 1 <= max_chunk_size:
            current += " " + para
        else:
            chunks.append(current.strip())
            current = para

    if current.strip():
        chunks.append(current.strip())

    return chunks

# 🔍 Main extraction
def extract_paragraphs_from_pages(pdf_path, page_numbers):
    paragraphs = []
    images = convert_from_path(
        pdf_path,
        first_page=min(page_numbers) + 1,
        last_page=max(page_numbers) + 1
    )
    page_to_img_idx = {p: i for i, p in enumerate(sorted(page_numbers))}

    for page_num in page_numbers:
        img_idx = page_to_img_idx.get(page_num)
        if img_idx is None or img_idx >= len(images):
            continue

        image = images[img_idx]
        text = pytesseract.image_to_string(image, lang='ben')

        if text:
            raw_chunks = [p.strip() for p in text.split('\n\n') if p.strip()]
            if len(raw_chunks) == 1:
                raw_chunks = [p.strip() for p in text.split('\n') if p.strip()]
            clean_chunks = [p for p in raw_chunks if not is_noise(p)]
            paragraphs.extend(clean_chunks)

    return paragraphs

# 🏁 Main execution
if __name__ == "__main__":
    pdf_path = "data/HSC-1ST-Paragraph.pdf"
    reader = PdfReader(pdf_path)
    page_numbers = list(range(len(reader.pages)))

    clean_paragraphs = extract_paragraphs_from_pages(pdf_path, page_numbers)

    # 💡 Merge paragraphs into chunks
    merged_chunks = merge_into_chunks(clean_paragraphs, max_chunk_size=500)

    # 📦 Optional: Trim to ~150 chunks if too many
    if len(merged_chunks) > 150:
        step = len(merged_chunks) // 150
        merged_chunks = [merged_chunks[i] for i in range(0, len(merged_chunks), step)][:150]

    # 💾 Save
    with open("smart_chunked_output.txt", "w", encoding="utf-8") as f:
        for i, chunk in enumerate(merged_chunks, 1):
            f.write(f"[CHUNK {i}]\n{chunk}\n{'='*50}\n")

    print(f"✅ Smart chunking done! Total Chunks: {len(merged_chunks)} saved to smart_chunked_output.txt")
