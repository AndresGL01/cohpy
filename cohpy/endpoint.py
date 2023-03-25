import abc
from dataclasses import dataclass, field

import requests
from requests import Response

from .constants import (
    BASE_COH3_URL,
    BASE_ACTIONS,
    TITLE_QUERY_PARAM
)

from .exceptions import (
    LeaderBoardDoesNotExist,
    ProfileIdDoesNotExist,
)


@dataclass
class Endpoint(abc.ABC):
    action: str
    leaderboard_pk: int = None
    profile_id: int = None
    title: str = TITLE_QUERY_PARAM
    query_params: dict = field(default_factory=lambda: {})
    base_actions: str = BASE_ACTIONS
    base_url: str = BASE_COH3_URL

    @property
    def url(self):
        return self._build_url()

    @abc.abstractmethod
    def get(self, **kwargs) -> dict:
        pass

    def _build_url(self) -> str:
        url = f'{self.base_url}{self.base_actions}{self.action}'
        url += self.title
        for param in self.query_params:
            url += f'&{param}={self.query_params.get(param)}'
        return url

    @staticmethod
    def validate_response(response) -> bool:
        """

        :param response: Payload from the API
        :return: False if validation fails else True
        """
        if response.status_code in [400]:
            return False
        response = response.json()
        if response.get('result')['code'] == 5:
            return False
        if response.get('matchHistoryStats') is not None and response.get('profiles') is not None:
            return bool(response.get('matchHistoryStats')) or bool(response.get('profiles'))
        return True


@dataclass
class AllLeaderboards(Endpoint):
    """
    Return all the available leaderboards
    """
    action: str = 'leaderboard/getAvailableLeaderboards/'

    @property
    def leaderboards(self):
        return self.get().json()

    def get(self, **kwargs) -> Response:
        response = requests.get(self.url)
        return response


@dataclass
class Leaderboard(Endpoint):
    action: str = 'leaderboard/getleaderboard2'

    @property
    def leaderboard_id(self):
        return self.leaderboard_pk

    @leaderboard_id.setter
    def leaderboard_id(self, value):
        self.leaderboard_pk = value

    @property
    def players(self) -> dict:
        return self.get().json()

    def get(self, **kwargs) -> Response:
        self.query_params['leaderboard_id'] = self.leaderboard_id
        response = requests.get(self.url)
        if not self.validate_response(response):
            raise LeaderBoardDoesNotExist(self.leaderboard_id)
        return response


@dataclass
class MatchHistory(Endpoint):
    action: str = 'Leaderboard/getRecentMatchHistoryByProfileId'

    @property
    def player_id(self):
        return self.profile_id

    @player_id.setter
    def player_id(self, value):
        self.profile_id = value

    @property
    def profile(self) -> dict:
        response = self.get()
        if not self.validate_response(response):
            raise ProfileIdDoesNotExist(self.profile_id)
        return response.json()

    def get(self, **kwargs) -> Response:
        self.query_params['profile_id'] = self.profile_id
        response = requests.get(self.url)
        self.validate_response(response)
        return response
