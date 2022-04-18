from pexpect import TIMEOUT as pexpectTIMEOUT
mpg_outs = [
    {
        "mpg_code": "@P 0",
        "action": "music_stop",
        "description": """For mpg123, it corresponds to any stop
                        For mpg312 it corresponds to user stop only"""
    },
    {
        "mpg_code": "@P 1",
        "action": "user_pause",
        "description": "Music has been paused by the user."
    },
    {
        "mpg_code": "@P 2",
        "action": "user_start_or_resume",
        "description": "Music has been started resumed by the user."
    },
    {
        "mpg_code": "@E *",
        "action": "error",
        "description": "Player has encountered an error."
    },
    {
        "mpg_code": "@silence",
        "action": None,
        "description": "Player has been silenced by the user."
    },
    {
        "mpg_code": r"@V [0-9\.\s%]*",
        "action": None,
        "description": "Volume change event.",
    },
    {
        "mpg_code": r"@S [a-zA-Z0-9\.\s-]*",
        "action": None,
        "description": "Stereo info event."
    },
    {
        "mpg_code": "@I *",
        "action": None,
        "description": "Information event."
    },
    {
        "mpg_code": pexpectTIMEOUT,
        "action": None,
        "description": "Timeout event."
    }
]

mpg_outs_ext = {
    "mpg123": [
        {
            "mpg_code": "@mute",
            "action": "user_mute",
            "description": "Player has been muted by the user."
        },
        {
            "mpg_code": "@unmute",
            "action": "user_unmute",
            "description": "Player has been unmuted by the user."
        }
    ],
    "mpg321": [
        {
            "mpg_code": "@P 3",
            "action": "end_of_song",
            "description": "Player has reached the end of the song."
        }
    ]
}

mpg_errors = [
    {
        "message": "empty list name",
        "action": "generic_error"
    },
    {
        "message": "No track loaded!",
        "action": "generic_error"
    },
    {
        "message": "Error opening stream",
        "action": "file_error"
    },
    {
        "message": "failed to parse given eq file:",
        "action": "file_error"
    },
    {
        "message": "Corrupted file:",
        "action": "file_error"
    },
    {
        "message": "Unknown command:",
        "action": "command_error"
    },
    {
        "message": "Unfinished command:",
        "action": "command_error"
    },
    {
        "message": "Unknown command or no arguments:",
        "action": "argument_error"
    },
    {
        "message": "invalid arguments for",
        "action": "argument_error"
    },
    {
        "message": "Missing argument to",
        "action": "argument_error"
    },
    {
        "message": "failed to set eq:",
        "action": "eq_error"
    },
    {
        "message": "Error while seeking",
        "action": "seek_error"
    },
]


class PlayerStatus:
    INSTANCIATED = 0
    PLAYING = 1
    PAUSED = 2
    RESUMING = 3
    STOPPING = 4
    STOPPED = 5
    QUITTED = 6
