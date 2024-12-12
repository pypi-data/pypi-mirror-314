class CLIArgs:
    args = {
        "BOARDPATH": {
            "name_or_flags": ["-b", "--board"],
            "type": str,
            "help": "Path to the board to use.",
            "required": True,
        },
        "BOTNAME": {
            "name_or_flags": ["-n", "--name"],
            "type": str,
            "help": "Name of the bot. Defaults to 'Hal-E'.",
            "required": False,
            "default": "Hal-E",
        },
        "DEBUG": {
            "name_or_flags": ["-d", "--debug"],
            "action": "store_true",
            "help": "Enable debug mode.",
            "required": False,
        },
        "INTROTEXT": {
            "name_or_flags": ["-i", "--introtext"],
            "type": str,
            "help": "Intro text for the bot. Defaults to 'Welcome to Hal-E! Your helpful assistant.'",
            "required": False,
            "default": "Welcome to Hal-E! Your helpful assistant.",
        },
        "LOGLEVEL": {
            "name_or_flags": ["-l", "--loglevel"],
            "type": int,
            "choices": [10, 20, 30, 40, 50],
            "help": "Log level. Defaults to 20 (INFO).",
            "required": False,
            "default": 20,
        },
        "CURRENT_CARD_ID": {
            "name_or_flags": ["-q", "--current_card_id"],
            "type": str,
            "help": "Current card ID.",
            "required": True,
        },
        "CHATLOGS": {
            "name_or_flags": ["-c", "--chatlogs"],
            "type": str,
            "help": "Path to store the chatlogs under.",
            "required": True,
        },
        "PORT": {
            "name_or_flags": ["-o", "--port"],
            "type": int,
            "help": "Port to start API on. Defaults to 8501.",
            "required": False,
        },
        "PUBLIC": {
            "name_or_flags": ["-p", "--public"],
            "action": "store_true",
            "help": "Sets port to 8499 to make API publicly available.",
            "required": False,
        },
        "SKIPLOGIN": {
            "name_or_flags": ["-s", "--skiplogin"],
            "action": "store_true",
            "help": "Skip login page and start chat directly",
            "required": False,
        },
        "PASSWORD": {
            "name_or_flags": ["-w", "--password"],
            "type": str,
            "help": "Password for authentication.",
            "required": False,
        }
    }
