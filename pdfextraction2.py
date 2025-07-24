import pytesseract
from pdf2image import convert_from_path
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_and_chunk_table(
    pdf_path,
    output_txt="data\\table_chunks.txt",
    poppler_path=r"C:\\Poppler\\poppler-24.08.0\\Library\\bin"
):
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    table_chunks = []
    table_pages = {1, 2, 3, 16}  # 1-based page numbers

    for idx, page_image in enumerate(pages):
        if (idx + 1) not in table_pages:
            continue

        print(f"Extracting table from page {idx+1}...")

        text = pytesseract.image_to_string(
            page_image,
            lang='ben',
            config='--psm 6'
        )

        lines = text.strip().splitlines()
        lines = [line.strip() for line in lines if line.strip()]

        # Remove filtering: keep all lines
        # table_lines = [line for line in lines if is_table_line(line)]
        table_lines = lines

        # Chunking: group every 15 lines as a chunk (adjust as needed)
        chunk_size = 15
        for i in range(0, len(table_lines), chunk_size):
            chunk = table_lines[i:i+chunk_size]
            table_chunks.append("===TABLE CHUNK===\n" + "\n".join(chunk))

    os.makedirs(os.path.dirname(output_txt), exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n\n".join(table_chunks))

    print(f"Table extraction and chunking completed. Output saved to: {output_txt}")

if __name__ == "__main__":
    pdf_path = "data\\HSC26-Bangla1st-Paper-3-19.pdf"
    extract_and_chunk_table(pdf_path)
