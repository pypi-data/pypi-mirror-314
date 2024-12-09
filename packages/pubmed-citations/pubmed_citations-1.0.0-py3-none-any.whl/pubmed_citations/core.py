from enum import Enum
from webrequests import WebRequest

from . import utils


class CiteFormat(Enum):
    MLA = 'mla'
    AMA = 'ama'
    APA = 'apa'
    NLM = 'nlm'


class PubmedCitations(object):
    """PubmedCitations
    ===============
    Get citation data for a list of PubMed IDs.

    Usage:
    >>> from pubmed_citations.core import PubmedCitations
    >>> citations = PubmedCitations(12345678, 12345679, 12345680)
    >>> citations.data
    >>> citations.to_docx()
    >>> citations.to_excel()
    >>> citations.to_json()
    >>> citations.to_csv()
    >>> citations.to_csv(outfile='citations.tsv', sep='\\t')
    """
    def __init__(self, *pmids, cite_fmt: CiteFormat = 'mla'):
        self.cite_fmt = self.check_cite_fmt(cite_fmt)
        self.pmid_list = utils.get_pmid_list(pmids)
        self._data = None

    def check_cite_fmt(self, cite_fmt):
        if cite_fmt.upper() not in CiteFormat.__members__:
            raise ValueError(f'invalid citation format, available formats: {CiteFormat.__members__}')
        return cite_fmt.lower()

    def get_citation_data(self, pmid):
        url = 'https://pubmed.ncbi.nlm.nih.gov/{}/citations/'.format(pmid)
        try:
            return WebRequest.get_response(url, max_try=3).json()
        except:
            return {}

    @property
    def data(self):
        if self._data is None:
            self._data = []
            for pmid in self.pmid_list:
                result = self.get_citation_data(pmid).get(self.cite_fmt) or {}
                self._data.append([pmid, result])
        return self._data
    
    @property
    def orig_data(self):
        data = []
        for pmid, citation in self.data:
            data.append([pmid, citation.get('orig', '.')])
        return data

    @property
    def format_data(self):
        data = []
        for pmid, citation in self.data:
            data.append([pmid, citation.get('format', '.')])
        return data
    
    def to_docx(self, outfile='output.docx'):
        utils.create_docx(self.format_data, outfile=outfile)

    def to_excel(self, outfile='output.xlsx'):
        utils.create_excel(self.orig_data, outfile=outfile)

    def to_csv(self, outfile='output.csv', sep=','):
        utils.create_csv(self.orig_data, outfile=outfile, sep=sep)

    def to_json(self, outfile='output.json'):
        utils.create_json(self.orig_data, outfile=outfile)

    def to_jsonlines(self, outfile='output.jl'):
        utils.create_jsonlines(self.orig_data, outfile=outfile)
