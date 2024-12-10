import pytest
from config import CAMP_TOKEN
from byterat.client import ByteratClientSync


class TestObservationMetrics:
    @classmethod
    def setup_class(cls):
        cls.client = ByteratClientSync(CAMP_TOKEN)

    def test_base(self):
        data = self.client.get_observation_metrics()
        assert data is not None
        assert len(data.data) > 0

    def test_by_dataset_key(self):
        data = self.client.get_observation_metrics_by_dataset_key(
            "abcd"
        )
        assert data is not None
        assert len(data.data) > 0

    def test_by_dataset_key_and_cycle(self):
        data = self.client.get_observation_metrics_by_dataset_key_and_dataset_cycle(
            "abcd", 87
        )
        assert data is not None
        assert len(data.data) > 0

    def test_by_filename(self):
        data = self.client.get_observation_metrics_by_filename(
            "SampleFileName.csv"
        )
        assert data is not None
        assert len(data.data) > 0

    def test_continuation_token(self):
        data = self.client.get_observation_metrics()
        assert data is not None
        assert len(data.data) > 0

        next_data = self.client.get_observation_metrics(
            data.continuation_token
        )
        assert next_data is not None
