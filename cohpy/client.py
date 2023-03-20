from dataclasses import dataclass
from cohpy.endpoint import (
    AllLeaderboards,
    Leaderboard,
    MatchHistory
)
from .leaderboards import Codes


@dataclass
class APIClient:
    """
    API interface between user and implementation
    """
    _all_leaderboards: AllLeaderboards = AllLeaderboards()
    _specific_leaderboard: Leaderboard = Leaderboard()
    _match_history: MatchHistory = MatchHistory()

    def leaderboards(self) -> list:
        """
        Return all types of leaderboards with info
        :return: All leaderboards
        """
        return self._all_leaderboards.leaderboards

    def leaderboard(self, *, leaderboard_id):
        """
        Retrieve data about a specific leaderboard given her id.

        :param leaderboard_id: int or cohpy.leaderboards.Code
        :return: leaderboard info dict
        """
        if isinstance(leaderboard_id, Codes):
            leaderboard_id = leaderboard_id.value
        self._specific_leaderboard.leaderboard_id = leaderboard_id
        return self._specific_leaderboard.players

    def profile(self, *, profile_id):
        self._match_history.player_id = profile_id
        return self._match_history.profile


def get_api_client() -> APIClient:
    """
    :return: APIClient instance
    """
    return APIClient()
