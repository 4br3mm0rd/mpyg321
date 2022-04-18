# # # Errors # # #
class MPygError(RuntimeError):
    """Base class for any errors encountered by the player during runtime"""
    pass


class MPygFileError(MPygError):
    """Errors encountered by the player related to files"""
    pass


class MPygCommandError(MPygError):
    """Errors encountered by the player related to player commands"""
    pass


class MPygArgumentError(MPygError):
    """Errors encountered by the player related to arguments for commands"""
    pass


class MPygEQError(MPygError):
    """Errors encountered by the player related to the equalizer"""
    pass


class MPygSeekError(MPygError):
    """Errors encountered by the player related to the seek"""
    pass


class MPygPlayerNotFoundError(MPygError):
    """Errors encountered when no suitable player is found"""
    pass
