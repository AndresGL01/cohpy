from dataclasses import dataclass


class CoreException(Exception):
    def __init__(self, failure_msg):
        self.failure_msg = failure_msg
        super().__init__(self.failure_msg)

    pass


class LeaderBoardIdIsNone(CoreException):
    def __init__(self):
        self.failure_msg = 'Leaderboard_id cannot be None, set a value before.'
        super().__init__(self.failure_msg)


class LeaderBoardDoesNotExist(CoreException):
    def __init__(self, leaderboard_id):
        self.failure_msg = f'Leaderboard with id: {leaderboard_id} does not exists.'
        super().__init__(self.failure_msg)
