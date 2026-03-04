import fitz  # PyMuPDF
import json  # json
import re    # REGEX
import os    # navigate folders

def extract_content(pdf_path, ranges):
    if not os.path.exists(pdf_path):
        print(f"Skipping: {pdf_path} (File not found)")
        return []

    doc = fitz.open(pdf_path)
    extracted_chunks = []
    current_dr = "General Context"

    # 'ranges' is a list of tuples like (start, end)
    for start, end in ranges:
        # PDF page index is 0-based, so subtract 1
        for page_num in range(start - 1, end):
            print(page_num)
            page = doc.load_page(page_num)
            view_box = fitz.Rect(0, 50, 595, 800) 
            text = page.get_text("text", clip=view_box)
            
            # Identify the Section (E1-X, ESRS 1, etc.)
            dr_match = re.search(r"(Disclosure Requirement|ESRS) (\d+|E1-\d+)", text)
            if dr_match:
                current_dr = dr_match.group(0)

            clean_text = " ".join(text.split())
            if clean_text:
                extracted_chunks.append({
                    "source": os.path.basename(pdf_path),
                    "page": page_num + 1,
                    "section": current_dr,
                    "text": clean_text
                })
    return extracted_chunks
    # return a list of dictionaries, each dictionary represents a chunk of text

# CONFIGURATION LIST jobs: Defines files and the specific pages to grab
# Each entry is a tuple of two things (file_path, page_ranges)
jobs = [
    ("./data/raw/ESRS E1 Delegated-act-2023-5303-annex-1_en.pdf", [(1, 40)]),
    ("./data/raw/OJ_L_202302772_EN_TXT.pdf", [(1, 38)]) 
]

#Single flat list that accumulates all the extracted chunks from every job into one combined dataset.
master_data = []
for file_path, page_ranges in jobs:
    print(f"Processing {file_path}...")
    master_data.extend(extract_content(file_path, page_ranges)) #Append all chunks from this call onto master data(as opposed to .append(), which would nest the list inside the list)

# SAVE THE RESULTS into master_esrs.json
os.makedirs("./data/processed", exist_ok=True)
with open("./data/processed/master_esrs.json", "w") as f:
    json.dump(master_data, f, indent=4)

print(f"Finished! Combined {len(master_data)} pages into master_esrs.json")