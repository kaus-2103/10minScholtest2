import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

PAGE_NUMBER_PATTERN = re.compile(r'^\s*\d+\s*$')
HEADER_KEYWORDS = ['অনলাইন ব্যাচ','মূল শব্দ','শব্দার্থ ও টীকা','শব্দের অর্থ ও ব্যাখ্যা']

def is_header_or_page_number(line):
    if PAGE_NUMBER_PATTERN.match(line):
        return True
    for keyword in HEADER_KEYWORDS:
        if keyword in line:
            return True
    return False

def extract_main_text_rows(pdf_path):
    reader = PdfReader(pdf_path)
    images = convert_from_path(pdf_path, first_page=1, last_page=len(reader.pages))

    all_rows = []
    for img in images:
        text = pytesseract.image_to_string(img, lang='ben')
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        filtered = [line for line in lines if not is_header_or_page_number(line)]
        all_rows.extend(filtered)

    return all_rows

def merge_every_two_lines(rows):
    """Merge every two consecutive lines into one chunk"""
    merged_chunks = []
    i = 0
    while i < len(rows):
        if i+1 < len(rows):
            merged = rows[i] + ' ' + rows[i+1]
            merged_chunks.append(merged.strip())
            i += 2
        else:
            # Last leftover line
            merged_chunks.append(rows[i].strip())
            i += 1
    return merged_chunks

if __name__ == "__main__":
    pdf_path = "data/HSC26-Bangla1st-Paper (1).pdf"
    rows = extract_main_text_rows(pdf_path)
    chunks = merge_every_two_lines(rows)

    with open("merged_column_chunks.txt", "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(chunks, 1):
            f.write(f"[CHUNK {idx}]\n{chunk}\n{'='*50}\n")

    print(f"✅ Done! Extracted {len(chunks)} merged chunks to merged_column_chunks.txt")
