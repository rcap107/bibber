#%%
import requests
import json
from urllib.parse import quote_plus
from pypdf import PdfReader
import re
from pathlib import Path

url = "https://doi.org/"
header = {"Accept": "application/x-bibtex"}

# Regex from https://stackoverflow.com/a/24246270/3741342
pattern = re.compile(r"(\b10\.(\d+\.*)+[\/](([^\s\.])+\.*)+\b)")

# %%
def parse_pdf_file(pdf_path):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    text = page.extract_text()
    return text

#%%
def prepare_citations(pdf_dir,pattern):
    citations = []

    for f in Path(pdf_dir).iterdir():
        if f.is_file() and f.suffix == ".pdf":
            text = parse_pdf_file(f)
            matches = pattern.findall(text)
            for match in matches:
                doi = match[0]
                test_doi_url = url + doi
                r = requests.get(test_doi_url, headers=header)
                if r.status_code == 200:
                    cit = r.text
                    cit = cit.replace("%2F", "/")
                    citations.append(cit)
                    break
    return citations


#%%
if __name__ == "__main__":
    pdf_dir = "."
    citations = prepare_citations(pdf_dir, pattern)
    with open("citations.txt", "w") as f:
        for c in citations:
            f.write(c + "\n")
    
# %%
