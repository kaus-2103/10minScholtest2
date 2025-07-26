# 📚 Bangla RAG Question Answering System (AI Engineer Level-1 Assessment)

A lightweight, local Retrieval-Augmented Generation (RAG) system that supports **Bangla and English** queries using a document-based knowledge base, semantic search, and a local LLM. It includes an API for integration and supports short-term session memory.

---

## ⚙️ Setup Guide

### 🔧 1. Clone the Repository
```bash
git clone https://github.com/kaus-2103/10minScholtest2.git
```

### 📦 2. Install Dependencies
```bash
pip install -r requirements.txt
```

> Make sure `Tesseract OCR` is installed for text extraction (used during preprocessing):
- Windows: `pip install pytesseract` LINK `https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-setup-3.02.02.exe/download`
- Linux: `sudo apt install tesseract-ocr`

Also install [Ollama](https://ollama.com) and run:
```bash
ollama run mistral
```

### 🧠 3. Preprocess & Embed PDF
Ensure you’ve extracted and chunked the Bangla textbook and embedded it using the script (provided in preprocessing module).

### 🚀 4. Start the API
```bash
fastapi dev main.py
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) to interact via Swagger UI.

---

## 🛠️ Tools, Libraries, and Packages

| Category              | Tool/Library                             |
|-----------------------|-------------------------------------------|
| Framework             | FastAPI                                   |
| OCR                   | pytesseract, pdf2image                    |
| Vector Database       | ChromaDB                                   |
| Embedding Model       | `intfloat/multilingual-e5-base` (Hugging Face) |
| Local Language Model  | `mistral` (via Ollama)                    |
| Vector Similarity     | Cosine Similarity                         |
| Data Format           | JSON, UTF-8 (Bangla-compatible)           |

---

## 💬 Sample Queries & Outputs

### 🔎 Bangla Query:
**Question**: `কল্যাণী কে ছিল?`

---

### 🔎 English Query:
**Question**: `What was the theme of the story?`


---

## 📘 API Documentation

### Endpoint
`POST /ask`

### Request Body
```json
{
  "question": "Your Bangla or English question here",
  "session_id": "optional-session-id"
}
```

### Response
```json
{
  "session_id": "test1",
  "question": "ছদ্মনাম?",
  "answer": "ভানুসিংহ ঠাকুর (Chunk 28)",
  "top_chunks": [
    {
      "chunk": "[CHUNK 28]\nছদ্মনাম: ভানুসিংহ ঠাকুর।",
      "score": 0.35181593894958496
    },
    {
      "chunk": "[CHUNK 25]\nজড়িমা আড়ষ্টতা। জড়ত্ব।",
      "score": 0.38326403498649597
    },
    {
      "chunk": "[CHUNK 67]\nদুই ধার দিয়া এলোচুল আসিয়া পড়ে না? হঠাৎ বাহিরে কারও পায়ের শব্দ পাইলে সে কি তাড়াতাড়ি তার সুগন্ধ\nআঁচলের মধ্যে ছবিটিকে লুকাইয়া ফেলে না? দিন যায়। একটা বৎসর গেল। মামা তো লজ্জায় বিবাহসন্বন্ধের কথা তুলিতেই পারেন না। মার ইচ্ছা ছিল,\nআমার অপমানের কথা যখন সমাজের লোকে ভুলিয়া যাইবে তখন বিবাহের চেষ্টা দেখিবেন।",
      "score": 0.3969522714614868
    }
  ]
}
```

Session memory allows contextual follow-up questions in the same session.

---

## 📊 Evaluation Matrix

| Metric        | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| **Groundedness**  | The system returns context-backed answers from relevant document chunks. |
| **Relevance**     | Cosine similarity (via ChromaDB) ensures top-K relevant chunk retrieval. |
| **Handling Vagueness** | If the query lacks context or clarity, the model gracefully responds with "উত্তর পাওয়া যায়নি" |
| **Short-Term Memory** | Maintains last 5 question-answer pairs per session to improve coherence in follow-up queries. |
| **Noise Reduction**   | Low-confidence chunks (MCQs/Q&A OCR failures) are removed during preprocessing to improve chunk quality. |

---


## 🧪 Future Improvements

- Advanced chunking strategies (e.g., QA-aware or sentence-graph-based).
- Use of larger, fine-tuned models for generation.
- Improved OCR using paddleocr or layout-aware tools like Donut.

---



1. What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?

        I used pytesseract combined with pdf2image to extract the Bangla text from the PDF. 
        Initially, I attempted to use standard PDF parsing libraries like PyMuPDF, pdfplumber, and pdfminer.
        However, despite the PDF using Unicode-compliant fonts (e.g., NotoSansBengali), these libraries failed to extract clean, 
        properly ordered text due to how the Bangla content was internally structured in the PDF—likely stored in a visually-correct but logically-disordered format.
        Because of these formatting challenges, I switched to an OCR-based approach. 
        I used pdf2image to convert each PDF page into high-resolution images and then 
        applied pytesseract with the Bangla language model (ben) to accurately extract the text as Unicode Bangla. 
        While OCR introduces some performance overhead, it provided a reliable way to recover correctly ordered and readable Bangla text from the document.
        In short, OCR using Tesseract was necessary due to structural and encoding issues that made traditional text extraction libraries unsuitable for this specific PDF.

2. What chunking strategy did you choose (e.g. paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?

       I chose a primarily paragraph-based chunking strategy, with adjustments based on content type. The OCR-extracted text was first cleaned and split using double newlines as paragraph boundaries. 
       For question-answer style sections, I initially grouped entire QA blocks into one chunk to preserve context. 
       For longer narrative sections like stories and essays, I used paragraph boundaries but also considered a 500-character soft limit to avoid chunks becoming too long for embedding. 
       However, due to the noisy OCR output in structured QA sections and MCQs, this strategy did not perform well in practice. 
       As a result, I excluded MCQ and question-answer parts and focused instead on narrative and vocabulary sections. 
       For vocabulary sections, I applied meaning-based chunking by joining related word-meaning pairs into coherent units. 
       This approach worked well because these paragraphs or word blocks typically contain complete and independent thoughts. 
       Embedding models like multilingual-e5 perform better on such semantically coherent chunks. 
       Avoiding low-quality OCR regions also helped reduce noise and improved retrieval relevance. 
       In summary, using content-aware, paragraph-based, and meaning-based chunking helped produce cleaner and more semantically useful chunks for retrieval.

3. What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?

        I used the intfloat/multilingual-e5-base embedding model. 
        I chose it because it supports multiple languages, including Bangla, which is essential for this RAG application. 
        The model was trained in two stages—first, on a massive set of multilingual text pairs using contrastive learning, and then fine-tuned on labeled datasets for sentence similarity tasks. 
        This training helps it learn how to place semantically similar sentences close together in vector space, even if they are in different languages or have different wording. 
        As a result, it can match questions and context based on meaning rather than just surface-level similarity. This makes it ideal for tasks like document retrieval and question answering.

4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?

        I compare the query and stored chunks by converting both into vector embeddings using the multilingual-e5 model and then calculating the cosine similarity between them. 
        Cosine similarity is a widely used method in semantic search because it measures the angle between vectors, which reflects how semantically similar two texts are. 
        I chose ChromaDB as the vector database because it’s lightweight, easy to use locally, and integrates well with Python. It also allows fast retrieval of top-k relevant chunks 
        based on similarity scores. This setup offers a simple yet effective way to support real-time question answering based on dense retrieval.


5. How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?

        I ensure meaningful comparison by converting both the question and document chunks into semantic embeddings using the multilingual-e5 model. 
        Since this model captures the actual meaning of text, it allows queries and chunks to be matched even if they are phrased differently. 
        This semantic approach is more robust than keyword-based methods. 
        However, if the question is vague or lacks context, the model may retrieve irrelevant or loosely related chunks. 
        In some cases, the system correctly identifies that no matching information is available and returns a fallback message. 
        To improve this in the future, I plan to use better query rewriting and relevance filtering techniques.



6. Do the results seem relevant? If not, what might improve them (e.g. better chunking, better embedding model, larger document)?

        The relevance of results varied. For clean, narrative content like stories or essays with well-structured paragraphs, 
        the system performed well. But in sections where OCR failed to extract clean or complete text tabular Q&A sections, the results were less reliable. 
        One major challenge was the poor quality of text extraction due to PDF formatting and OCR limitations. 
        Even though OCR helped overcome the text extraction barrier, it introduced some misspellings and character issues. 
        To improve this, I believe a more advanced OCR pipeline or better-quality source PDF would help significantly. 
        Additionally, more experimentation with chunking strategies, especially layout-aware or sentence-level chunking, could improve retrieval accuracy. 
        Overall, the main improvements would come from cleaner extraction and more refined chunking.




Poppler path: C:\Program Files\poppler-24.08.0\Library\bin

