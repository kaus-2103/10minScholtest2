import pytesseract
from pdf2image import convert_from_path
import os

# Optional: Set Tesseract path explicitly (if not added to PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_bangla_from_pdf(pdf_path, output_txt="data\ocr_bangla_output.txt", poppler_path=r"C:\\Poppler\\poppler-24.08.0\\Library\\bin"):
    # Convert PDF to images
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

    all_text = []

    for idx, page_image in enumerate(pages):
        print(f"OCR processing page {idx+1}/{len(pages)}...")

        # Run Tesseract OCR (Bangla language)
        text = pytesseract.image_to_string(
            page_image,
            lang='ben',  # 'ben' is the language code for Bangla
            config='--psm 6'  # Assume a uniform block of text
        )

        all_text.append(text.strip())

    final_text = "\n\n".join(all_text)

    # Save extracted Bangla text
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"OCR completed. Bangla text saved to {output_txt}")

if __name__ == "__main__":
    pdf_path = "data\HSC26-Bangla1st-Paper.pdf"  # Change this path as needed
    ocr_bangla_from_pdf(pdf_path)
