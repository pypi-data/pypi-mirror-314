from typing import Dict, Optional, List
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from .decorators import _elastic_connection


class KataElastic:
    """A class to manage all required Elasticsearch operations for Kata.
    """
    def __init__(self, elasticsearch_url, timeout: Optional[int] = None):
        self.timeout = timeout
        self.elasticsearch_url = elasticsearch_url
        self.elasticsearch = Elasticsearch(self.elasticsearch_url, request_timeout=self.timeout)

    @_elastic_connection
    def check(self) -> bool:
        """Checks Elasticsearch connection.
        :return: bool: Elasticsearch accessible or not.
        """
        if self.elasticsearch.ping():
            return True
        return False

    @_elastic_connection
    def create_index(
            self,
            index: str,
            shards: int = 3,
            replicas: int = 1,
            settings: Optional[dict] = None
    ) -> Dict:
        """Creates empty index.
        :param: index str: Name of the created index.
        :param: shards int: Number of shards for the index.
        :param: replicas int: Number of replicas of the index.
        :param: settings dict: Overwrite settings for the index.
        """
        body = settings or {
            "number_of_shards": shards,
            "number_of_replicas": replicas,
        }
        return self.elasticsearch.indices.create(index=index, settings=body)

    @_elastic_connection
    def delete_index(self, index: str, ignore: Optional[bool] = True) -> dict:
        """Deletes index.
        :param: index str: Name of the index to be deleted.
        :param: ignore bool: Ignore errors because of closed/deleted index.
        """
        response = self.elasticsearch.indices.delete(index=index, ignore_unavailable=ignore)
        return response

    @_elastic_connection
    def delete_document(self, document_id: str, index: str, ignore: Optional[bool] = True) -> dict:
        """Deletes document fom index.
        :param: document_id str: ID of the document to be deleted.
        :param: index str: Index where the document is to be found.
        :param: ignore bool: Ignore errors because of closed/deleted index.
        """
        response = self.elasticsearch.delete(id=document_id, index=index, ignore_unavailable=ignore)
        return response

    @_elastic_connection
    def index_document(self, index: str, body: dict, document_id: Optional[str] = None) -> Dict:
        """Indexes document.
        :param: index str: Index that document will be indexed into.
        :param: body dict: Document body.
        :param: document_id str: Optional id for the document. Is generated automatically if None.
        """
        if document_id:
            document = self.elasticsearch.index(index=index, id=document_id, body=body)
        else:
            document = self.elasticsearch.index(index=index, body=body)
        return document

    @_elastic_connection
    def get_documents_by_key(self, index: str, document_key: str) -> List:
        """This method is for retrieving all texts/pages of the original document.
        :param: index str: Index to search the documents from.
        :param: document_key str: parent_id field that connects pages of document together.
        :return: List of matching documents. 
        """
        s = Search(using=self.elasticsearch, index=index)
        docs = s.query("match", parent_id=document_key).execute()
        return docs

    def __str__(self) -> str:
         return self.elasticsearch_url
