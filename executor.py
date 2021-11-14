from typing import Dict

from jina import Executor, DocumentArray, requests, DocumentArrayMemmap


class U100KIndexer(Executor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self._docs = DocumentArrayMemmap(self.workspace)
        except ValueError:
            self._docs = DocumentArrayMemmap()

    @requests(on='/index')
    def index(self, docs: 'DocumentArray', **kwargs):
        """Index new docs into storage

        :param docs: DocumentArray containing Documents
        :param kwargs: other keyword arguments
        """
        self._docs.extend(docs)

    @requests(on='/search')
    def search(self, docs: 'DocumentArray', parameters: Dict = {}, **kwargs):
        """Append kNN matches to each document in docs

        :param docs: documents that are searched
        :param parameters: dictionary of pairs (parameter,value)
        :param kwargs: other keyword arguments
        """
        docs.match(
            self._docs,
            metric='cosine',
            normalization=(1, 0),
            **parameters
        )

    @requests(on='/search_by_key')
    def search_by_key(self, parameters: Dict, **kwargs):
        """Append kNN matches to each document in docs

        :param parameters: dictionary of key
        :param kwargs: other keyword arguments
        """
        return DocumentArray([self._docs[int(_id)] for _id in parameters['keys']])
