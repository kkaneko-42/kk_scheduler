from dotenv import load_dotenv
import os

load_dotenv()
TOKEN: str      = os.getenv("KK_SCHEDULER_TOKEN")
GUILD_ID: int   = int(os.getenv("KK_SCHEDULER_GUILD_ID"))
