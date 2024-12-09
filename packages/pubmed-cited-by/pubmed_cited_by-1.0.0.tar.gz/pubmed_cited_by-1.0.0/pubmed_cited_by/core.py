import os
import time
import loguru
from webrequests import WebRequest

from . import utils


class PubmedCitedBy(object):
    """
    Get cited by data from Pubmed
    =============================

    Usage:
    >>> from pubmed_cited_by.core import PubmedCitedBy
    >>> 
    >>> pcb = PubmedCitedBy()
    >>> 
    >>> result = pcb.get_cited_by_data(1)
    >>> print(result)
    >>> 
    >>> pmids = [1, 2, 3]
    >>> data = pcb.get_cited_by(pmids)
    >>> for item in data:
    >>>     print(item)
    """

    def __init__(self, ncbi_api_key=None):
        self.ncbi_api_key = ncbi_api_key
        self._api_key = None

    @property
    def api_key(self):
        if self._api_key is None:
            self._api_key = self.ncbi_api_key or os.environ.get('NCBI_API_KEY') or False
            if self._api_key:
                loguru.logger.debug(f'use NCBI_API_KEY: {self._api_key}')
        return self._api_key

    def get_cited_by_data(self, pmid):
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
        payload = {
            'dbfrom': 'pubmed',
            'db': 'pubmed',
            'cmd': 'neighbor',
            'retmode': 'json',
            'id': pmid,
        }
        if self.api_key:
            payload['api_key'] = self.api_key

        while True:
            try:
                resp = WebRequest.get_response(url, params=payload)
                data = resp.json()
                break
            except Exception as e:
                # loguru.logger.exception(f'failed: {e}')
                time.sleep(3)

        cited_by_pmids = []
        for item in data['linksets'][0]['linksetdbs']:
            if item['linkname'] == 'pubmed_pubmed_citedin':
                cited_by_pmids = item['links']
                break

        return dict(count=len(cited_by_pmids), cited_by_pmids=cited_by_pmids)
    
    def get_cited_by(self, pmids):
        for pmid in utils.get_pmid_list(pmids):
            context = {'pmid': pmid}
            context.update(self.get_cited_by_data(pmid))
            yield context


if __name__ == '__main__':
    pcb = PubmedCitedBy()
    result = pcb.get_cited_by_data(36708705)
    print(result)
