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
    LeaderBoardDoesNotExist
)


@dataclass
class Endpoint(abc.ABC):
    action: str
    id: int = None
    title: str = TITLE_QUERY_PARAM
    query_params: dict = field(default_factory=lambda: {'count': 2, 'type': 0})
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

    def validate_response(self, response):
        if response.status_code == 400:
            raise LeaderBoardDoesNotExist(self.id)


@dataclass
class GetAllLeaderBoards(Endpoint):
    """
    Return all the available leaderboards
    """
    action: str = 'getAvailableLeaderboards/'

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
class GetLeaderBoard(Endpoint):
    action: str = 'getleaderboard2'

    @property
    def leaderboard_id(self):
        if not self.id:
            raise LeaderBoardIdIsNone()
        return self.id

    @leaderboard_id.setter
    def leaderboard_id(self, value):
        self.id = value

    @property
    def leaderboard_data(self):
        self.response = self.get()
        return self.response

    def get(self, **kwargs) -> dict:
        self.query_params['leaderboard_id'] = self.leaderboard_id
        response = requests.get(self.url)
        self.validate_response(response)
        print(self.url)
        return response.json()
