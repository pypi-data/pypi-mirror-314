# Generate citations for PubMed articles

## Installation

```bash
python3 -m pip install pubmed-citations
```

## Usage

### Use in Python

```python
from pubmed_citations.core import PubmedCitations

pmids = [12345678, 87654321]
citations = PubmedCitations(*pmids)

# get data
print(citations.data)
print(citations.orig_data)

# save to file
citations.to_docx("output.docx")
citations.to_excel("output.xlsx")
citations.to_json("output.json")
citations.to_jsonlines("output.jl")
citations.to_csv("output.csv")
citations.to_csv("output.tsv", sep="\t")
```

### Use in CMD

```bash
pubmed_citations --help

pubmed_citations 1 2 3
pubmed_citations pmid.list

pubmed_citations 1 2 3 -f apa -o output.xlsx
pubmed_citations 1 2 3 -f apa -o output.docx
pubmed_citations 1 2 3 -f apa -o output.csv
pubmed_citations 1 2 3 -f apa -o output.json
pubmed_citations 1 2 3 -f apa -o output.jl
pubmed_citations 1 2 3 -f apa -o output.tsv
```
