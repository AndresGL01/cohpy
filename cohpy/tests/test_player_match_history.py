import unittest
import cohpy

from cohpy.exceptions import (
    ProfileIdDoesNotExist
)


class TestPlayerMatchHistoryEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = cohpy.get_api_client()

    def test_get_a_player_history(self):
        response = self.api_client.profile(profile_id=10058)  # My own profile id :)
        expected_keys = ('matchHistoryStats', 'profiles',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_a_player_history_with_server_response(self):
        response = self.api_client.profile(profile_id=10058, remove_server_status=False)
        expected_keys = ('result', 'matchHistoryStats', 'profiles',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_non_existing_player_raise_a_exception(self):
        with self.assertRaises(ProfileIdDoesNotExist):
            self.api_client.profile(profile_id=-999)
