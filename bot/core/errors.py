class UnknownGuildError(Exception):
    def __init__(self, *, guild_id: int):
        super().__init__()
        self.guild_id = guild_id
