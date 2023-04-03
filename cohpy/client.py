from dataclasses import dataclass, field

from cohpy.endpoint import (
    AllLeaderboards,
    Leaderboard,
    MatchHistory,
    PersonalStats,
)

from .leaderboards import Codes, SortType


@dataclass
class APIClient:
    """
    API interface between user and implementation
    """
    _all_leaderboards: AllLeaderboards = field(default_factory=lambda: AllLeaderboards())
    _specific_leaderboard: Leaderboard = field(default_factory=lambda: Leaderboard())
    _match_history: MatchHistory = field(default_factory=lambda: MatchHistory())
    _personal_stats: PersonalStats = field(default_factory=lambda: PersonalStats())

    def leaderboards(self, *, remove_server_status=True) -> dict:
        """
        Return all types of leaderboards with info

        :param remove_server_status: Set to True if you want the server status response.
        :return: All leaderboards
        """
        response = self._all_leaderboards.get()
        if remove_server_status:
            response.pop('result')
        return response

    def leaderboard(self, *, leaderboard_id, remove_server_status=True, count=200,
                    sort_type=SortType.ELO, start=1):
        """
        Retrieve data about a specific leaderboard given her id.

        :param start: Position of the first player in the requests
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
        self._specific_leaderboard.query_params['leaderboard_id'] = leaderboard_id
        self._specific_leaderboard.query_params['count'] = count
        self._specific_leaderboard.query_params['type'] = sort_type
        self._specific_leaderboard.query_params['start'] = start
        self._specific_leaderboard.leaderboard_id = leaderboard_id
        response = self._specific_leaderboard.get()

        if remove_server_status:
            response.pop('result')
        return response

    def match_history(self, *, profile_params, remove_server_status=True, mode='relic'):
        """
        :param mode: Query mode against the API. Choose between steam, relic or alias
        :param profile_params: Relic's player (int) id, steam profile (str),
         list of Relic's players ids or list of steam profiles (list)

        single relic's id => profile_params = 1
        single steam id => profile_params = steam/123456789
        single relic's id => profile_params = [1,2,3,4,5...]
        single relic's id => profile_params = [steam/123456789,steam/9786756453423,steam/987654321]

        :param remove_server_status: Set to False if you want the server status response.
        :return:
        """
        self._match_history.profile_params = profile_params
        self._match_history.query_mode = mode
        response = self._match_history.get()
        if remove_server_status:
            response.pop('result')
        return response

    def personal_stats(self, *, profile_params, remove_server_status=True, mode='relic'):
        self._personal_stats.profile_params = profile_params
        self._personal_stats.query_mode = mode
        response = self._personal_stats.get()

        if remove_server_status:
            response.pop('result')
        return response


def get_api_client() -> APIClient:
    """
    :return: APIClient instance
    """
    return APIClient()
