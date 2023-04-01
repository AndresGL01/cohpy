import abc
import json
import re
from collections.abc import Iterable
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
    BadSteamIdExpression,
    BadRelicIdExpression,
    BadAliasesExpression,
    QueryModeException,
)


@dataclass
class Endpoint(abc.ABC):
    action: str
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


class PlayersEndpoint(Endpoint):
    _profile_params = None
    _mode = None

    @property
    def profile_params(self):
        return self._profile_params

    @profile_params.setter
    def profile_params(self, value):
        self._profile_params = value

    @property
    def query_mode(self):
        return self._mode

    @query_mode.setter
    def query_mode(self, value):
        self._mode = value

    @abc.abstractmethod
    def get(self, **kwargs) -> dict:
        pass

    def _set_params(self):
        if self.query_mode not in ['steam', 'relic', 'alias']:
            raise QueryModeException(self.query_mode)
        if self.query_mode == 'steam':
            self._validate_steam_params()
            self.query_params['profile_names'] = json.dumps(self.profile_params)
        elif self.query_mode == 'relic':
            self._validate_relic_params()
            self.query_params['profile_ids'] = json.dumps(self.profile_params)
        elif self.query_mode == 'alias':
            self._validate_aliases_params()
            self.query_params['aliases'] = json.dumps(self.profile_params)

    def _validate_steam_params(self):
        """
        Validate that all steam profiles id are str and startswith steam/

        Regex explanation:

        - ^ is an anchor that specifies the beginning of the string.
        - This means that the string being matched must start with /steam/.
        - [0-9] is a character set that matches any digit (0-9).
        - (+) quantifier specifies that the digit character set must occur one or more times.

         Examples:

        - /steam/123
        - /steam/0
        - /steam/9876543210
        :return:
        """
        self.profile_params = self.profile_params.split() if type(self.profile_params) is str \
            else self.profile_params
        pattern = re.compile(r'^/steam/[0-9]+')
        if not all(type(param) is str and
                   re.fullmatch(pattern, param) for param in self.profile_params):
            raise BadSteamIdExpression()

    def _validate_relic_params(self):
        """
        Validate all relic's params are int
        :return:
        """
        self.profile_params = [self.profile_params] if type(self.profile_params) is not list else \
            self.profile_params
        if not all(type(param) == int for param in self.profile_params):
            raise BadRelicIdExpression()

    def _validate_aliases_params(self):
        """
        Validate all aliases params are str
        :return:
        """
        self.profile_params = self.profile_params.split() if type(self.profile_params) is str \
            else self.profile_params
        if isinstance(self.profile_params, Iterable):
            if not all(type(param) == str for param in self.profile_params):
                raise BadAliasesExpression()
        else:
            if type(self.profile_params) != str:
                raise BadAliasesExpression()


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
    leaderboard_pk: int = None

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
class MatchHistory(PlayersEndpoint):
    action: str = 'leaderboard/getRecentMatchHistory'

    @property
    def match_history(self) -> dict:
        response = self.get()
        if not self.validate_response(response):
            raise ProfileIdDoesNotExist(self.profile_params)
        return response.json()

    def get(self, **kwargs) -> Response:
        self._set_params()
        response = requests.get(self.url)
        self.validate_response(response)
        return response


@dataclass
class PersonalStats(PlayersEndpoint):
    action: str = 'leaderboard/getPersonalStat'

    @property
    def personal_stats(self):
        response = self.get()
        if not self.validate_response(response):
            raise ProfileIdDoesNotExist(self.profile_params)
        return response.json()

    def get(self, **kwargs) -> Response:
        self._set_params()
        response = requests.get(self.url)
        self.validate_response(response)
        return response
