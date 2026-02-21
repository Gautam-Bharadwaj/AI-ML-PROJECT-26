import re

def split_into_clauses(text):
    header_pattern = r'\n(?=(?:Article|Section|ARTICLE|SECTION|Schedule|Annex|SCHEDULE|ANNEX|\d+\.\d+)\s+)'
    
    sections = re.split(header_pattern, text)
    
    return [s.strip() for s in sections if len(s.strip()) > 15]

def save_clauses(clauses, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for idx, item in enumerate(clauses, 1):
            f.write(f"--- CLAUSE {idx} ---\n{item}\n\n")
