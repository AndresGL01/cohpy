import unittest

import cohpy
from cohpy import SortType
from cohpy.exceptions import (
    LeaderBoardDoesNotExist
)


class TestSpecificLeaderboardEndpoint(unittest.TestCase):

    def setUp(self) -> None:
        self.api_client = cohpy.get_api_client()

    def test_specific_leaderboard_with_server_response(self):
        response = self.api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3,
                                               remove_server_status=False)
        expected_keys = ('result', 'statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)
        assert isinstance(response, dict)

    def test_all_leaderboard_without_server_response(self):
        response = self.api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3)
        expected_keys = ('statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)
        assert isinstance(response, dict)

    def test_all_leaderboard_with_int(self):
        response = self.api_client.leaderboard(leaderboard_id=2130329)
        expected_keys = ('statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)
        assert isinstance(response, dict)

    def test_non_existing_leaderboard_raise_exception(self):
        with self.assertRaises(LeaderBoardDoesNotExist):
            self.api_client.leaderboard(leaderboard_id=-1)

    def test_default_player_len_is_200(self):
        response = self.api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3)
        expected_keys = ('statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)
        assert len(response['statGroups']) == 200

    def test_player_count_filter(self):
        response = self.api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3, count=50)
        expected_keys = ('statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)
        assert len(response['statGroups']) == 50

    def test_players_sort_by_type(self):
        response = self.api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3, sort_type=0)
        expected_keys = ('statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)

    def test_players_sort_by_type_with_sort_type_enum(self):
        response = self.api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3,
                                               sort_type=SortType.ELO)
        expected_keys = ('statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)

    def test(self):
        response = self.api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3,
                                               sort_type=SortType.ELO,
                                               start=200)
        expected_keys = ('statGroups', 'leaderboardStats', 'rankTotal',)

        assert all(key in expected_keys for key in response)
