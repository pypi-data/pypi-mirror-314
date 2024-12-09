import re
from pathlib import Path


def get_pmid_list(pmids):
    for pmid in pmids:
        pmid = str(pmid)
        if Path(pmid).exists():
            text = Path(pmid).read_text().strip()
            yield from re.split(r'\s+', text)
        else:
            yield pmid


if __name__ == '__main__':
    pmid_list = list(get_pmid_list(['1', '2', '3']))
    print(pmid_list)
