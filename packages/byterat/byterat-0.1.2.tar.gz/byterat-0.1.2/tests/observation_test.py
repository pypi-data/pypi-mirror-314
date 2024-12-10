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
            "B14B-6"
        )
        assert data is not None
        assert len(data.data) > 0

    def test_by_dataset_key_and_cycle(self):
        data = self.client.get_observation_metrics_by_dataset_key_and_dataset_cycle(
            "B14B-6", 570
        )
        assert data is not None
        assert len(data.data) > 0

    def test_by_filename(self):
        data = self.client.get_observation_metrics_by_filename(
            "ARGONNE_11_CFF-B14B-P6f.014"
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
