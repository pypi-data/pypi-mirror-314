import kdp_api
from kdp_api.api import manage_records_api
from kdp_api.models.job import Job

class StorageApi(object):

    def clear_dataset(self, config, dataset_id: str) -> Job:
        """This method will be used to clear dataset.

            :param Configuration config: Connection configuration
            :param str dataset_id: ID of the KDP dataset where the data will queried

            :returns: clear dataset job

            :rtype: Job
        """
        with kdp_api.ApiClient(config) as api_client:
            api_instance = manage_records_api.ManageRecordsApi(api_client)
            return api_instance.post_clear_dataset(dataset_id=dataset_id)
