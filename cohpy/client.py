from dataclasses import dataclass
from cohpy.endpoint import (
    AllLeaderboards,
    Leaderboard,
    MatchHistory
)
from .leaderboards import Codes, SortType


@dataclass
class APIClient:
    """
    API interface between user and implementation
    """
    _all_leaderboards: AllLeaderboards = AllLeaderboards()
    _specific_leaderboard: Leaderboard = Leaderboard()
    _match_history: MatchHistory = MatchHistory()

    def leaderboards(self, *, remove_server_status=True) -> dict:
        """
        Return all types of leaderboards with info

        :param remove_server_status: Set to True if you want the server status response.
        :return: All leaderboards
        """
        response = self._all_leaderboards.leaderboards
        if remove_server_status:
            response.pop('result')
        return response

    def leaderboard(self, *, leaderboard_id, remove_server_status=True, count=200,
                    sort_type=SortType.ELO):
        """
        Retrieve data about a specific leaderboard given her id.

        :param sort_type: 1 == Sort by Wins, 0 == Sort by ELO. int or Type instance
        :param count: How many players will be returned [1-200]
        :param leaderboard_id: int or cohpy.leaderboards.Code
        :param remove_server_status: Set to False if you want the server status response.
        :return: leaderboard info dict
        """
        if isinstance(leaderboard_id, Codes):
            leaderboard_id = leaderboard_id.value
        if isinstance(sort_type, SortType):
            sort_type = sort_type.value
        self._specific_leaderboard.query_params['count'] = count
        self._specific_leaderboard.query_params['type'] = sort_type
        self._specific_leaderboard.leaderboard_id = leaderboard_id
        response = self._specific_leaderboard.players

        if remove_server_status:
            response.pop('result')
        return response

    def profile(self, *, profile_id, remove_server_status=True):
        """

        :param profile_id: Relic's player id
        :param remove_server_status: Set to False if you want the server status response.
        :return:
        """
        self._match_history.player_id = profile_id
        response = self._match_history.profile
        if remove_server_status:
            response.pop('result')
        return response


def get_api_client() -> APIClient:
    """
    :return: APIClient instance
    """
    return APIClient()
