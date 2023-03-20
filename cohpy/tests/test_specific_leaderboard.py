import unittest
import cohpy


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
            self.api_client.leaderboard(leaderboard_id=10058)
