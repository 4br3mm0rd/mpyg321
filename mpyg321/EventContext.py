class MPyg321EventContext:
    """Base class for all events"""

    def __init__(self, player) -> None:
        self.player = player


class MPyg321ErrorContext(MPyg321EventContext):
    """Context for error events"""

    def __init__(self, player, error_type, error_message) -> None:
        super().__init__(player)
        self.error_type = error_type
        self.error_message = error_message
