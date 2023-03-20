import abc
from dataclasses import dataclass, field

import requests

from .constants import (
    BASE_COH3_URL,
    BASE_ACTIONS,
    TITLE_QUERY_PARAM
)

from .exceptions import (
    LeaderBoardIdIsNone,
    LeaderBoardDoesNotExist,
    PlayerIdIsNone,
    ProfileIdDoesNotExist
)


@dataclass
class Endpoint(abc.ABC):
    action: str
    leaderboard_pk: int = None
    profile_id: int = None
    title: str = TITLE_QUERY_PARAM
    query_params: dict = field(default_factory=lambda: {'count': 100, 'type': 0})
    base_actions: str = BASE_ACTIONS
    base_url: str = BASE_COH3_URL
    response: dict = None

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

    def validate_response(self, endpoint, response):
        if response.status_code == 400:
            if isinstance(endpoint, Leaderboard):
                raise LeaderBoardDoesNotExist(self.leaderboard_pk)
            if isinstance(endpoint, MatchHistory):
                raise ProfileIdDoesNotExist(self.profile_id)


@dataclass
class AllLeaderboards(Endpoint):
    """
    Return all the available leaderboards
    """
    action: str = 'leaderboard/getAvailableLeaderboards/'

    @property
    def leaderboards(self):
        if not self.response:
            self.get()
        return self.response.get('leaderboards')

    @property
    def raw_response(self):
        self.response = self.get()
        return self.response

    def get(self, **kwargs) -> dict:
        self.response = requests.get(self.url).json()
        return self.response


@dataclass
class Leaderboard(Endpoint):
    action: str = 'leaderboard/getleaderboard2'

    @property
    def leaderboard_id(self):
        if not self.leaderboard_pk:
            raise LeaderBoardIdIsNone()
        return self.leaderboard_pk

    @leaderboard_id.setter
    def leaderboard_id(self, value):
        self.leaderboard_pk = value

    @property
    def players(self):
        self.response = self.get()
        return self.response

    def get(self, **kwargs) -> dict:
        self.query_params['leaderboard_id'] = self.leaderboard_id
        response = requests.get(self.url)
        self.validate_response(self, response)
        return response.json()


@dataclass
class MatchHistory(Endpoint):
    action: str = 'Leaderboard/getRecentMatchHistoryByProfileId'

    @property
    def player_id(self):
        if not self.profile_id:
            raise PlayerIdIsNone()
        return self.profile_id

    @player_id.setter
    def player_id(self, value):
        self.profile_id = value

    @property
    def profile(self):
        self.response = self.get()
        return self.response.get('matchHistoryStats')

    def get(self, **kwargs) -> dict:
        self.query_params['profile_id'] = self.profile_id
        response = requests.get(self.url)
        self.validate_response(self, response)
        return response.json()

