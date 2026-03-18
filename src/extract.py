import fitz  # PyMuPDF
import os
import re
from typing import Any

def extract_text_from_pdf(pdf_path, start=0, end=None):
    """ Grabs text from PDF. end=None reads till the end. """
    try:
        doc = fitz.open(pdf_path)
        content = []
        
        last_page = end if end and end <= len(doc) else len(doc)
        print(f"Reading: {pdf_path} (Pages {start+1} to {last_page})")
        
        for i in range(start, last_page):
            page = doc.load_page(i)
            page_text = page.get_text("text")
            
            # Simple OCR detection: If no text but images exist
            if not page_text.strip() and page.get_images():
                print(f"Warning: Page {i+1} appears to be an image. OCR may be required.")
            
            content.append(page_text)
            
        doc.close()
        return "\n".join(content)
    except Exception as err:
        print(f"PDF Error: {err}")
        return None

def extract_legal_metadata(text):
    """
    Data Engineering: Extract key identifiers from raw text.
    Kumar's Responsibility.
    """
    metadata: dict[str, Any] = {
        "Parties": [],
        "Effective Date": None,
        "Governing Law": None,
        "Jurisdiction": None
    }
    
    # Regex Patterns for Legal Terms
    patterns = {
        "Parties": r'(?:between|among)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s*(?:LLC|Inc|Corp|Ltd|and))?)',
        "Effective Date": r'(?:Effective\s+Date|dated|this\s+day\s+of)\s+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
        "Governing Law": r'governed\s+by\s+the\s+laws\s+of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        "Jurisdiction": r'exclusive\s+jurisdiction\s+of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    }
    
    for key, pattern in patterns.items():
        matches = list(re.findall(pattern, text))
        if matches:
            if key == "Parties":
                # Ensure we only take first 2 and strip them
                metadata[key] = [str(m).strip() for m in matches[:2]]
            else:
                metadata[key] = str(matches[0]).strip()
                
    return metadata

def save_text(text, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to: {target_path}")

if __name__ == "__main__":
    pass
