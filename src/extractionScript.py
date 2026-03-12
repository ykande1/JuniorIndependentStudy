import fitz  # PyMuPDF: Used for high performance PDF text and coordinate extraction
import json  # Used to save our structured data into a format machines can read easily
import re    # Used to find patterns in the text
import os    # Used to handle folder paths and ensure the script works on any computer

def extract_content(pdf_path, ranges):
    """
    Reads a PDF, clips out headers/footers, identifies the legal section,
    and splits the text into small, labeled paragraph chunks.
    """
    if not os.path.exists(pdf_path):
        print(f"Skipping: {pdf_path} (File not found)")
        return []

    doc = fitz.open(pdf_path)
    extracted_chunks = []
    
    # If Page 4 has no header it inherits the header found on Page 3.
    current_dr = "General Context"

    for start, end in ranges:
        # PDF page index: (page 1 is index 0)
        for page_num in range(start - 1, end):
            page = doc.load_page(page_num)
            
            # COORDINATE CLIPPING: (x0, y0, x1, y1)
            view_box = fitz.Rect(0, 50, 595, 750) 
            text = page.get_text("text", clip=view_box)
            
            # NOISE FILTER: Skip pages that are just a Table of Contents.
            if "Table of contents" in text or text.count("........") > 5:
                continue

            # SECTION IDENTIFICATION:
            # Looks for patterns like "Disclosure Requirement E1-1" or "ESRS 2".
            dr_match = re.search(r"(Disclosure Requirement [A-Z0-9-]+|ESRS \d+|ESRS [A-Z]\d+)", text)
            if dr_match:
                current_dr = dr_match.group(0)

            # SEMANTIC PARTITIONING:
            # Instead of a whole page, we split text into individual clauses.
            # This regex splits whenever it sees a line starting with "1. ", "14. ", or "AR 1. "
            paragraphs = re.split(r'\n(?=\d+\.\s|AR\s\d+\.\s)', text)

            for para in paragraphs:
                # Clean up whitespace and newlines for a consistent text string
                clean_para = " ".join(para.split()).strip()
                
                # LENGTH FILTER: Ignore tiny fragments or artifacts under 60 characters.
                if len(clean_para) < 60:
                    continue

                # TYPE TAGGING: 
                # Distinguish between the PP and the AR
                # This allows for advanced filtering during the AI retrieval stage.
                chunk_type = "Application Requirement" if clean_para.startswith("AR") else "Primary Provision"

                # Store all data and metadata in a dictionary
                extracted_chunks.append({
                    "source": os.path.basename(pdf_path), # Name of the file
                    "page": page_num + 1,                 # Actual page number
                    "section": current_dr,                # The legal section it belongs to
                    "type": chunk_type,                   # Provision VS Application
                    "text": clean_para                    # Real content
                })
                print ("+")
                
    doc.close()
    return extracted_chunks

# --- EXECUTION BLOCK ---

# CONFIGURATION: Define which files to process and which pages contain the real content
jobs = [
    ("./data/raw/ESRS E1 Delegated-act-2023-5303-annex-1_en.pdf", [(1, 40)]),
    ("./data/raw/OJ_L_202302772_EN_TXT.pdf", [(1, 38)]) 
]

master_data = []
#Iterating through the "jobs" list
for file_path, page_ranges in jobs:
    print(f"Processing {file_path}...")
    # .extend() adds the list of chunks to our master list without nesting them
    master_data.extend(extract_content(file_path, page_ranges))

# OUTPUT: Save the final list of dictionaries to a JSON file
os.makedirs("./data/processed", exist_ok=True)
with open("./data/processed/master_esrs.json", "w") as f:
    json.dump(master_data, f, indent=4)

print(f"Finished! Combined {len(master_data)} semantic chunks into master_esrs.json")