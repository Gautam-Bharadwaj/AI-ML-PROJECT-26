import re

def split_into_clauses(text):
    """
    Splits contract text into individual clauses based on common legal headers.
    """
    # Pattern to match Section, Article, or numbered list like 1.1, 2.1 etc.
    pattern = r'\n(?=(?:Article|Section|ARTICLE|SECTION|\d+\.\d+)\s+)'
    clauses = re.split(pattern, text)
    return [c.strip() for c in clauses if c.strip()]

def save_clauses(clauses, output_path):
    """
    Saves the list of clauses to a file for preview.
    """
    with open(output_path, "w", encoding="utf-8") as out:
        for i, clause in enumerate(clauses):
            out.write(f"--- START CLAUSE {i+1} ---\n{clause}\n--- END ---\n\n")
