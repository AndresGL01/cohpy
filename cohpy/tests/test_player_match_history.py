import unittest

import cohpy
from cohpy.exceptions import (
    BadAliasesExpression,
    BadRelicIdExpression,
    BadSteamIdExpression,
    ProfileIdDoesNotExist,
    QueryModeException,
)


class TestPlayerMatchHistoryEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = cohpy.get_api_client()

    def test_get_a_player_history(self):
        response = self.api_client.match_history(profile_params=10058)  # My own profile id :)
        expected_keys = ('matchHistoryStats', 'profiles',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_players_history_with_relic_ids(self):
        response = self.api_client.match_history(profile_params=[10058, 175836])
        expected_keys = ('matchHistoryStats', 'profiles',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_a_player_history_with_server_response(self):
        response = self.api_client.match_history(profile_params=10058, remove_server_status=False)
        expected_keys = ('result', 'matchHistoryStats', 'profiles',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_a_player_history_with_steam_profile(self):
        response = self.api_client.match_history(profile_params='/steam/76561198116217807',
                                                 mode='steam')
        expected_keys = ('matchHistoryStats', 'profiles',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_get_players_history_with_steam_id(self):
        response = self.api_client.match_history(profile_params=['/steam/76561198116217807',
                                                                 '/steam/76561198116217807'],
                                                 mode='steam')
        expected_keys = ('matchHistoryStats', 'profiles',)

        assert all(key in response for key in expected_keys)
        assert isinstance(response, dict)

    def test_non_existing_player_raise_exception(self):
        with self.assertRaises(ProfileIdDoesNotExist):
            self.api_client.match_history(profile_params=-999)

    def test_input_bad_ids_raise_exception(self):
        with self.assertRaises(BadRelicIdExpression):
            self.api_client.match_history(profile_params=[10058, 'test_value'])

    def test_input_bad_strings_steam_mode_raise_exception(self):
        with self.assertRaises(BadSteamIdExpression):
            self.api_client.match_history(profile_params=['test_value', 10058], mode='steam')

    def test_input_bad_string_in_alias_mode_raise_exception(self):
        with self.assertRaises(BadAliasesExpression):
            self.api_client.match_history(profile_params=10058, mode='alias')

    def test_input_bad_list_string_in_alias_mode_raise_exception(self):
        with self.assertRaises(BadAliasesExpression):
            self.api_client.match_history(profile_params=[10058], mode='alias')

    def test_bad_query_mode_raise_exception(self):
        with self.assertRaises(QueryModeException):
            self.api_client.match_history(profile_params=10058, mode='unknown')
