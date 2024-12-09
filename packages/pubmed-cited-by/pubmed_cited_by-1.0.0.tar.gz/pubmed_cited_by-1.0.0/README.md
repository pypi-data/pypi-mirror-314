# Get cited by information from Pubmed.

## Installation

```bash
python3 -m pip install pubmed-cited-by
```

## Usage

> set API_KEY in environment variable [***recommend***]

> see more: https://account.ncbi.nlm.nih.gov/settings/#api-key

```bash
echo NCBI_API_KEY=<your_api_key> >> ~/.bashrc
```

### Use in Python

```python
from pubmed_cited_by.core import PubmedCitedBy

pcb = PubmedCitedBy()

result = pcb.get_cited_by_data(1)
print(result)

pmids = [1, 2, 3]
data = pcb.get_cited_by(pmids)
for item in data:
    print(item)
```

### Use in CMD

```bash

pubmed_cited_by --help

pubmed_cited_by  1 2 3
pubmed_cited_by  pmid.list

pubmed_cited_by  1 2 3 -o output.xlsx
pubmed_cited_by  1 2 3 -o output.csv
pubmed_cited_by  1 2 3 -o output.tsv
pubmed_cited_by  1 2 3 -o output.json
pubmed_cited_by  1 2 3 -o output.jl
```
