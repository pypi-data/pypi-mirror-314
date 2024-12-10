"""
  get_observation_data(dataset_key: String, dataset_cycle: Int, file_name: String, continuation_token: String): API_Data!
  get_dataset_cycle_data(dataset_key: String, dataset_cycle: Int, file_name: String, continuation_token: String): API_Data!
  get_metadata(dataset_key: String, continuation_token: String): API_Data!
"""

GET_OBSERVATION_DATA = """
    query($dataset_key: String, $dataset_cycle: Int, $file_name: String, $continuation_token: String) {
        get_observation_data(dataset_key: $dataset_key, dataset_cycle: $dataset_cycle, file_name: $file_name, continuation_token: $continuation_token) {
            data
            continuation_token
        }
    }
    """

GET_DATASET_CYCLE_DATA = """
    query($dataset_key: String, $dataset_cycle: Int, $file_name: String, $continuation_token: String) {
        get_dataset_cycle_data(dataset_key: $dataset_key, dataset_cycle: $dataset_cycle, file_name: $file_name, continuation_token: $continuation_token) {
            data
            continuation_token
        }
    }
    """

GET_METADATA = """
    query($dataset_key: String, $continuation_token: String) {
        get_metadata(dataset_key: $dataset_key, continuation_token: $continuation_token) {
            data
            continuation_token
        }
    }
    """
