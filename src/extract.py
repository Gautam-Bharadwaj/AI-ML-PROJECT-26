import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path, start=0, end=None):
    """ Grabs text from PDF. end=None reads till the end. """
    try:
        doc = fitz.open(pdf_path)
        content = []
        
        last_page = end if end and end <= len(doc) else len(doc)
        print(f"Reading: {pdf_path} (Pages {start+1} to {last_page})")
        
        for i in range(start, last_page):
            page = doc.load_page(i)
            content.append(page.get_text("text"))
            
        doc.close()
        return "\n".join(content)
    except Exception as err:
        print(f"PDF Error: {err}")
        return None

def save_text(text, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to: {target_path}")

if __name__ == "__main__":
    pass
