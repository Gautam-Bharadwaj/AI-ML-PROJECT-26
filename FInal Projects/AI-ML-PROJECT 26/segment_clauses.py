import re

def split_into_clauses(text):
    pattern = r'\n(?=(?:Article|Section|ARTICLE|SECTION|\d+\.\d+)\s+)'
    clauses = re.split(pattern, text)
    return [c.strip() for c in clauses if c.strip()]

with open("extracted_contract.txt", "r", encoding="utf-8") as f:
    contract_text = f.read()

clauses_list = split_into_clauses(contract_text)

print(f"Total Clauses: {len(clauses_list)}")

with open("segmented_clauses.txt", "w", encoding="utf-8") as out:
    for i, clause in enumerate(clauses_list):
        out.write(f"--- START CLAUSE {i+1} ---\n{clause}\n--- END ---\n\n")
        