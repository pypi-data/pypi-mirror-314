import unittest
from unittest.mock import Mock

from kdp_api.models import RecordBatch

from kdp_connector.connectors.query import QueryApi
from kdp_connector.main import KdpConn


class TestQuery(unittest.TestCase):

    def setup(self):
        self.jwt = 'eyJhbGciOiJIUzI1NiIs'
        self.workspace_id = 'abc'
        self.dataset_id = '8c6718fa-348f-4019-a28f-c85037fc4b85'
        self.host = 'https://api.koverse.localhost'
        self.batch_size = 50000
        self.starting_record_id = ''

    def test_post_sql_query(self):
        self.setup()
        query_api = QueryApi()
        expected_record_batch = self.getRecordBatch()
        query_api.post_sql_query = Mock(return_value=expected_record_batch)

        kdp_conn = KdpConn()
        config = kdp_conn.create_configuration()

        # Call the method
        result = query_api.post_sql_query(config=config, dataset_id=self.dataset_id, sql_query="SELECT * FROM table")

        # Assert the expected behavior
        query_api.post_sql_query.assert_called_once_with(config=config, dataset_id=self.dataset_id, sql_query="SELECT * FROM table")
        self.assertEqual(len(result.records), 2)
        self.assertEqual(result, expected_record_batch)

    @staticmethod
    def getRecords():
        # Including data to test that the dataframe gets the correct data
        first_json_record = {"record": {'a': 3}}
        second_json_record = {"record": {'b': 4}}
        return [first_json_record, second_json_record]

    @staticmethod
    def getDataStoreList(json_record_list):
        result_list = []
        for json_record in json_record_list:
            result_list.append(json_record['record'])

        return result_list

    def getRecordBatch(self):
        record_batch = RecordBatch()
        record_batch.records = self.getRecords()
        record_batch.last_record_id = '2.' + self.dataset_id + '.recordId'
        record_batch.more = bool(True)
        return record_batch

    def getRecordBatchNoMoreRecords(self):
        record_batch = RecordBatch()
        record_batch.records = self.getRecords()
        record_batch.last_record_id = '3.' + self.dataset_id + '.recordId'
        record_batch.more = bool(False)
        return record_batch


if __name__ == '__main__':
    unittest.main()