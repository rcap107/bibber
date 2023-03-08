#%%
import requests
import json
from urllib.parse import quote_plus
from pypdf import PdfReader
import re

#%% 
### working with doi
test_doi_url = "https://doi.org/10.1145/3318464.3389742"

header = {"Accept": "text/x-bibliography"}

r = requests.get(test_doi_url, headers=header)

if r.status_code == 200:
    print(r.text)

#%%
reader = PdfReader("embdi-paper.pdf")
page = reader.pages[0]
text = page.extract_text()

p = re.compile(r"(\b10\.(\d+\.*)+[\/](([^\s\.])+\.*)+\b)")
matches = p.findall(text)
# %%
url = "https://doi.org/"
for match in matches:
    doi = match[0]
    header = {"Accept": "application/x-bibtex"}
    test_doi_url = url + doi
    r = requests.get(test_doi_url, headers=header)
    if r.status_code == 200:
        print(r.text)


# %%
