class CoreException(Exception):
    def __init__(self, failure_msg):
        self.failure_msg = failure_msg
        super().__init__(self.failure_msg)

    pass


class LeaderBoardDoesNotExist(CoreException):
    def __init__(self, leaderboard_id):
        self.failure_msg = f'Leaderboard with id: {leaderboard_id} does not exists.'
        super().__init__(self.failure_msg)


class ProfileIdDoesNotExist(CoreException):
    def __init__(self, profile_id):
        self.failure_msg = f'player_id with id: {profile_id} does not exists.'
        super().__init__(self.failure_msg)


class BadSteamIdExpression(CoreException):
    def __init__(self):
        self.failure_msg = 'Failed to set steam id player. Revise profile_params'
        super().__init__(self.failure_msg)


class BadRelicIdExpression(CoreException):
    def __init__(self):
        self.failure_msg = 'Failed to set relic id player. Revise type of ids'
        super().__init__(self.failure_msg)


class BadAliasesExpression(CoreException):
    def __init__(self):
        self.failure_msg = 'Failed to set alias player. Revise type of alias. Maybe you want' \
                           ' relic id mode? Set to mode="relic"'
        super().__init__(self.failure_msg)


class QueryModeException(CoreException):
    def __init__(self, param):
        self.failure_msg = f'Uknown query mode {param}. Options are ["steam", "relic", "alias"]'
        super().__init__(self.failure_msg)
