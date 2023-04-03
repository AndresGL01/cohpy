import unittest

import cohpy
from cohpy.exceptions import (
    BadAliasesExpression,
    BadRelicIdExpression,
    BadSteamIdExpression,
    ProfileIdDoesNotExist,
    QueryModeException,
)


class PersonalStatsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = cohpy.get_api_client()

    def test_get_personal_stat_with_relic_id(self):
        response = self.api_client.personal_stats(profile_params=10058)
        expected_keys = ('statGroups', 'leaderboardStats',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_personal_stat_with_steam_id(self):
        response = self.api_client.personal_stats(profile_params='/steam/76561198116217807',
                                                  mode='steam')
        expected_keys = ('statGroups', 'leaderboardStats',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_personal_stat_with_in_game_alias(self):
        response = self.api_client.personal_stats(profile_params='W1ntersLP',
                                                  mode='alias')
        expected_keys = ('statGroups', 'leaderboardStats',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_multiple_stats_with_relics_ids(self):
        response = self.api_client.personal_stats(profile_params=[10058, 175836])
        expected_keys = ('statGroups', 'leaderboardStats',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_multiple_stats_with_steam_ids(self):
        response = self.api_client.personal_stats(profile_params=['/steam/76561198116217807',
                                                                  '/steam/76561198116217807'],
                                                  mode='steam')
        expected_keys = ('statGroups', 'leaderboardStats',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_multiple_stats_with_in_game_alias(self):
        response = self.api_client.personal_stats(profile_params=['W1ntersLP', '@dr1guerre'],
                                                  mode='alias')
        expected_keys = ('statGroups', 'leaderboardStats',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_non_existing_player_raise_exception(self):
        with self.assertRaises(ProfileIdDoesNotExist):
            self.api_client.personal_stats(profile_params=-999)

    def test_input_bad_strings_steam_mode_raise_exception(self):
        with self.assertRaises(BadSteamIdExpression):
            self.api_client.personal_stats(profile_params=['test_value', 10058], mode='steam')

    def test_input_bad_ids_raise_exception(self):
        with self.assertRaises(BadRelicIdExpression):
            self.api_client.personal_stats(profile_params=[10058, 'test_value'])

    def test_input_bad_aliases_raise_exception(self):
        with self.assertRaises(BadAliasesExpression):
            self.api_client.personal_stats(profile_params=[10058, 'test_value'], mode='alias')

    def test_bad_query_mode_raise_exception(self):
        with self.assertRaises(QueryModeException):
            self.api_client.personal_stats(profile_params=10058, mode='unknown')
