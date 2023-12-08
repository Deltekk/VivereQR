import os
from dotenv import load_dotenv, find_dotenv

token : str = ""

def LoadConfigs() -> None:
    """LOAD_CONFIG: Carichiamo le stringhe dal file '.env' """
    
    load_dotenv(find_dotenv()) # Carichiamo il file di ambiente dove sono stati salvati i file di config

    global token

    token = os.environ.get("BOT_TOKEN")

    return None

def GetToken() -> str : return token