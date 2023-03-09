#%%
import requests
import json
from urllib.parse import quote_plus
from pypdf import PdfReader
import re
from pathlib import Path
import sys
from tqdm import tqdm

url = "https://doi.org/"
header = {"Accept": "application/x-bibtex"}

# Regex from https://stackoverflow.com/a/24246270/3741342
pattern = re.compile(r"(\b10\.(\d+\.*)+[\/](([^\s\.])+\.*)+\b)")


def parse_pdf_file(pdf_path):
    """Given a a path to a pdf file, return the text of the first page of the file.

    Args:
        pdf_path (Path): Path to a pdf file.

    Returns:
        str: The text of the first page of the pdf file.
    """
    reader = PdfReader(pdf_path)
    try:
        page = reader.pages[0]
        text = page.extract_text()
        return text
    except AttributeError:
        print(f"{pdf_path} does contain pages.")
        text = None
        return text

def query_by_doi(doi):
    test_doi_url = url + doi
    r = requests.get(test_doi_url, headers=header)
    if r.status_code == 200:
        cit = r.text
        cit = cit.replace("%2F", "/")
    else:
        cit = None
    return cit


def prepare_citations(pdf_dir, pattern):
    citations = []
    missing_citations = []
    n_files = len(list(pdf_dir.glob("*.pdf")))

    for f in tqdm(Path(pdf_dir).iterdir(), total=n_files):
        if f.is_file() and f.suffix == ".pdf":
            tqdm.write(f"Parsing {f.name}")
            text = parse_pdf_file(f)
            if text is not None:
                matches = pattern.findall(text)
                for match in matches:
                    doi = match[0]
                    cit = query_by_doi(doi)
                    if cit is not None:
                        citations.append(cit)
                        break
            else:
                print(f"{f} does not contain text.")
                missing_citations.append(f)
    return citations, missing_citations


if __name__ == "__main__":
    pdf_dir = Path(sys.argv[1])    
    citations, missing_citations = prepare_citations(pdf_dir, pattern)
    with open("citations.txt", "w") as f:
        for c in citations:
            f.write(c + "\n")

    with open("missing_citations.txt", "w") as f:
        for m in missing_citations:
            f.write(str(m) + "\n")