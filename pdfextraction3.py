import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_paragraphs_from_pages(pdf_path, page_numbers):
    paragraphs = []
    images = convert_from_path(pdf_path, first_page=min(page_numbers)+1, last_page=max(page_numbers)+1)
    page_to_img_idx = {p: i for i, p in enumerate(sorted(page_numbers))}
    for page_num in page_numbers:
        img_idx = page_to_img_idx[page_num]
        image = images[img_idx]
        text = pytesseract.image_to_string(image, lang='ben')
        if text:
            chunks = [p.strip() for p in text.split('\n\n') if p.strip()]
            if len(chunks) == 1:
                chunks = [p.strip() for p in text.split('\n') if p.strip()]
            paragraphs.extend(chunks)
    return paragraphs

if __name__ == "__main__":
    pdf_path = "data/HSC-1ST-Paragraph.pdf"
    reader = PdfReader(pdf_path)
    page_numbers = list(range(len(reader.pages)))
    paragraphs = extract_paragraphs_from_pages(pdf_path, page_numbers)
    with open("extracted_paragraphs.txt", "w", encoding="utf-8") as f:
        for i, para in enumerate(paragraphs, 1):
            f.write(f" [ CHUNK {i}] \n{para}\n{'='*50}\n")
    print("Paragraphs saved to extracted_paragraphs.txt")