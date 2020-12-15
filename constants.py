import os

class Constants:
    #---- For report.py
    #-- colouring command-line outputs
    ENABLE_LOG_COLOR = False
    BG_OKBLUE = '\033[94m' if ENABLE_LOG_COLOR else ""
    BG_OKGREEN = '\033[92m' if ENABLE_LOG_COLOR else ""
    BG_WARNING = '\033[93m' if ENABLE_LOG_COLOR else ""
    BG_FAIL = '\033[91m' if ENABLE_LOG_COLOR else ""
    BG_ENDC = '\033[0m' if ENABLE_LOG_COLOR else ""
    BG_LOG = '\033[0;37;40m' if ENABLE_LOG_COLOR else ""
    BG_NORMAL = '\033[1;37;0m' if ENABLE_LOG_COLOR else ""
    BG_BOLD = '\033[1m' if ENABLE_LOG_COLOR else ""
    #-- for filetype
    FILETYPE_INVESTMENT = 0
    FILETYPE_PROFIT_LOSS = 1
    FILETYPE_UNKNOWN = -1
    #-- filename prefix of each filetype
    FILENAME_INVESTMENT_POSITION = "investment positions"
    FILENAME_PROFIT_LOSS = "profit loss"

    #---- For ima.py
    FILENAME_DAILY_INTEREST = "daily interest"