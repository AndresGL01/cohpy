from dataclasses import dataclass
from cohpy.endpoint import (
    GetAllLeaderBoards,
    GetLeaderBoard
)
from .leaderboards import Codes


@dataclass
class APIClient:
    """
    API interface between user and implementation
    """
    _all_leaderboards: GetAllLeaderBoards = GetAllLeaderBoards()
    _specific_leaderboard: GetLeaderBoard = GetLeaderBoard()

    @property
    def leaderboards(self) -> list:
        """
        :return: All leaderboards
        """
        return self._all_leaderboards.leaderboards

    @property
    def raw_leaderboards(self) -> dict:
        """
        :return: All leaderboards including the api response message
        """
        return self._all_leaderboards.raw_response

    @property
    def leaderboard_id(self):
        """
        :return: Leaderboard id
        """
        return self._specific_leaderboard.leaderboard_id

    @leaderboard_id.setter
    def leaderboard_id(self, value):
        """

        :param value: int or Code instance. Set the leaderboard_id value for future requests
        :return:
        """
        if isinstance(value, Codes):
            value = value.value
        self._specific_leaderboard.leaderboard_id = value

    @property
    def leaderboard_data(self):
        """
        Default parameters:
        title = coh3

        type = 1  (1 - ELO, 0 - WINS)

        count = 200  (1-200)

        :return: Data relative to leaderboard
        """
        return self._specific_leaderboard.leaderboard_data


def get_api_client() -> APIClient:
    """
    :return: APIClient instance
    """
    return APIClient()
