from unittest import TestCase

import cohpy


class TestAllLeaderboardsEndpoint(TestCase):

    def setUp(self) -> None:
        self.api_client = cohpy.get_api_client()

    def test_all_leaderboard_with_server_response(self):
        response = self.api_client.leaderboards(remove_server_status=False)
        expected_keys = ('result', 'leaderboards', 'matchTypes', 'races', 'factions',
                         'leaderboardRegions',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_all_leaderboard_without_server_response(self):
        response = self.api_client.leaderboards()
        expected_keys = ('leaderboards', 'matchTypes', 'races', 'factions', 'leaderboardRegions',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)
