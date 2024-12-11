import unittest
from unittest import mock
from unittest.mock import Mock, call

import pandas as pd
from kdp_api.models import WriteBatchResponse

from kdp_connector.main import KdpConn


class TestUpdate(unittest.TestCase):
    def setup(self):
        self.JWT = 'eyJhbGciOiJIUzI1NiI'
        self.workspace_id = 'abc'
        self.dataset_id = 'd851a97f-b94a-465a-ae9c-207df0a8260f'
        self.host = 'https://api.koverse.localhost'
        self.input_file = '~/documents/Test documents/WithDates.csv'
        self.write_batch_response = WriteBatchResponse(workspace=self.workspace_id,
                                                       dataset_id=self.dataset_id,
                                                       partitions=[0, 1])
        self.api_instance = Mock()
        self.api_instance.post_write_id.return_value = self.write_batch_response
        self.configuration = Mock()
        self.configuration.host = self.host

    @staticmethod
    def getDataframe(size: int):
        data = []
        for x in range(size):
            data.append({'name': 'tom', 'age': 20 + x, '_koverse_record_id': str(x)})
        return pd.DataFrame(data)

    @staticmethod
    def getDataframeNoRecordId(size: int):
        data = []
        for x in range(size):
            data.append({'name': 'tom', 'age': 20 + x})
        return pd.DataFrame(data)

    def test_update_dataframe(self):
        self.setup()
        self.batch_size = 10
        mock_api_instance = self.api_instance
        mock_configuration = self.configuration
        expected_write_calls = [call(dataset_id=self.dataset_id,
                                     request_body=[{'name': 'tom', 'age': 20, '_koverse_record_id': '0'}, {'name': 'tom', 'age': 21, '_koverse_record_id': '1'},
                                                  {'name': 'tom', 'age': 22, '_koverse_record_id': '2'}, {'name': 'tom', 'age': 23, '_koverse_record_id': '3'}],
                                     is_async=False)]

        with(mock.patch('kdp_api.ApiClient')):
            with(mock.patch('kdp_api.Configuration', side_effect=[mock_configuration])):
                with(mock.patch('kdp_api.api.write_api.WriteApi', side_effect=[mock_api_instance])):
                    self.setup()
                    self.batch_size = 10
                    kdp_conn = KdpConn()
                    partitions_set = kdp_conn.batch_write(dataframe=self.getDataframe(4), dataset_id=self.dataset_id, batch_size=self.batch_size)
                    mock_api_instance.post_write_id.assert_has_calls(expected_write_calls)

        expected_partitions_set = {0, 1}
        self.assertEqual(expected_partitions_set, partitions_set)

def test_update_dataframe_no_record_id(self):
    self.setup()
    self.batch_size = 10
    mock_api_instance = self.api_instance
    mock_configuration = self.configuration

    with(mock.patch('kdp_api.ApiClient')):
        with(mock.patch('kdp_api.Configuration', side_effect=[mock_configuration])):
            with(mock.patch('kdp_api.api.write_api.WriteApi', side_effect=[mock_api_instance])):
                self.setup()
                self.batch_size = 10
                kdp_conn = KdpConn()
                with self.assertRaises(ValueError) as context:
                    kdp_conn.batch_write(self.getDataframeNoRecordId(4), self.dataset_id, self.JWT, self.batch_size)
                self.assertEqual(str(context.exception), "Each record must include an existing _koverse_record_id field")


if __name__ == '__main__':
    unittest.main()
