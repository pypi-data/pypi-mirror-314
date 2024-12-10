import kdp_api
from kdp_api import LuceneQueryRequest, QueryDocumentLuceneRequest, Query
from kdp_api.api import read_and_query_api
from kdp_api.models.query_document_lucene_response import QueryDocumentLuceneResponse


class QueryApi(object):

    def post_lucene_query(self, config, dataset_id: str, expression: str, limit: int = 5, offset: int = 0):
        """This method will be used to query data in KDP datasets using the lucene syntax

            :param Configuration config: Connection configuration
            :param str dataset_id: ID of the KDP dataset where the data will queried
            :param str expression: Lucene style query expression ex. name: John

            :returns: Records matching query expression

            :rtype: RecordBatch
        """
        with kdp_api.ApiClient(config) as api_client:
            api_instance = read_and_query_api.ReadAndQueryApi(api_client)

            lucene_query_request = LuceneQueryRequest(datasetId=dataset_id, expression=expression, limit=limit, offset=offset)

            return api_instance.post_lucene_query(lucene_query_request=lucene_query_request)

    def post_document_lucene_query(self, config, dataset_id: str, expression: str, limit: int = 5, offset: int = 0) -> QueryDocumentLuceneResponse:
        """This method will be used to query document data in KDP datasets using the lucene syntax

            :param Configuration config: Connection configuration
            :param str dataset_id: ID of the KDP dataset where the data will queried
            :param str expression: Lucene style query expression ex. name: John
            :param int limit: max number of results in the response.
            :param int offset: how many records to skip before returning first record.
            :returns: QueryDocumentLuceneResponse object contains records matching query expression

            :rtype: QueryDocumentLuceneResponse
        """
        with kdp_api.ApiClient(config) as api_client:
            api_instance = read_and_query_api.ReadAndQueryApi(api_client)

            query_document_lucene_request = QueryDocumentLuceneRequest(datasetId=dataset_id, expression=expression, limit=limit, offset=offset)

            return api_instance.post_lucene_query_document(query_document_lucene_request=query_document_lucene_request)

    def post_sql_query(self, config, dataset_id: str, expression: str, limit: int = 5, offset: int = 0, include_internal_fields: bool = False):
        """This method will be used to query data in KDP datasets using the SQL syntax

            :param Configuration config: Connection configuration
            :param str dataset_id: ID of the KDP dataset where the data will queried
            :param str expression: Lucene style query expression ex. name: John
            :param bool include_internal_fields: Include internal fields in the response

            :returns: Records matching query expression

            :rtype: RecordBatch
        """
        with kdp_api.ApiClient(config) as api_client:
            api_instance = read_and_query_api.ReadAndQueryApi(api_client)

            sql_query_request = Query(datasetId=dataset_id, expression=expression, limit=limit, offset=offset)

            return api_instance.post_query(query=sql_query_request, include_internal_fields=include_internal_fields)