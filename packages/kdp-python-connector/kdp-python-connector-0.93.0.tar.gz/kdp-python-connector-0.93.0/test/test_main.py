import unittest
from unittest.mock import Mock, patch, ANY
from urllib.parse import quote

from kdp_connector.main import KdpConn


class TestKdpConn(unittest.TestCase):

    def setUp(self):
        self.jwt = 'eyJhbGciOiJIUzI1NiIs'
        self.workspace_id = 'abc'
        self.dataset_id = '8c6718fa-348f-4019-a28f-c85037fc4b85'
        self.host = 'https://api.koverse.localhost'
        self.batch_size = 50000
        self.limit = 5
        self.offset = 0
        self.include_internal_fields = False

    @patch('kdp_connector.main.QueryApi')
    def test_post_sql_query(self, MockQueryApi):
        mock_query_api_instance = MockQueryApi.return_value
        expected_result = Mock()
        mock_query_api_instance.post_sql_query.return_value = expected_result

        kdp_conn = KdpConn()
        expression = f'select * from "{self.dataset_id}"'

        # Call the method
        result = kdp_conn.post_sql_query(self.dataset_id, expression, self.limit, self.offset, self.include_internal_fields)

        # Assert the expected behavior
        encoded_expression = quote(expression)
        mock_query_api_instance.post_sql_query.assert_called_once_with(
            ANY, dataset_id=self.dataset_id, expression=encoded_expression, limit=self.limit, offset=self.offset, include_internal_fields=self.include_internal_fields
        )
        self.assertEqual(result, expected_result)

    @patch('kdp_connector.main.QueryApi')
    def test_post_lucene_query(self, MockQueryApi):
        mock_query_api_instance = MockQueryApi.return_value
        expected_result = Mock()
        mock_query_api_instance.post_lucene_query.return_value = expected_result

        kdp_conn = KdpConn()
        expression = 'name: John'

        # Call the method
        result = kdp_conn.post_lucene_query(self.dataset_id, expression, self.limit, self.offset)

        # Assert the expected behavior
        encoded_expression = quote(expression)
        mock_query_api_instance.post_lucene_query.assert_called_once_with(
            ANY, dataset_id=self.dataset_id, expression=encoded_expression, limit=self.limit, offset=self.offset
        )
        self.assertEqual(result, expected_result)

    @patch('kdp_connector.main.QueryApi')
    def test_post_document_lucene_query(self, MockQueryApi):
        mock_query_api_instance = MockQueryApi.return_value
        expected_result = Mock()
        mock_query_api_instance.post_document_lucene_query.return_value = expected_result

        kdp_conn = KdpConn()
        expression = 'name: John'

        # Call the method
        result = kdp_conn.post_document_lucene_query(self.dataset_id, expression, self.limit, self.offset)

        # Assert the expected behavior
        encoded_expression = quote(expression)
        mock_query_api_instance.post_document_lucene_query.assert_called_once_with(
            ANY, dataset_id=self.dataset_id, expression=encoded_expression, limit=self.limit, offset=self.offset
        )
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
