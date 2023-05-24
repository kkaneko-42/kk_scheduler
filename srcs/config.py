from dotenv import load_dotenv
import os

load_dotenv()
TOKEN: str              = os.getenv("KK_SCHEDULER_TOKEN")
GUILD_ID: int           = int(os.getenv("KK_SCHEDULER_GUILD_ID"))
NOTIFY_CHANNEL_ID: int  = int(os.getenv("KK_SCHEDULER_NOTIFY_CHANNEL_ID"))
POOLING_SECONDS: int    = int(os.getenv("KK_SCHEDULER_POOLING_SECONDS"))
SNAPSHOT_PATH: str      = os.getenv("KK_SCHEDULER_SNAPSHOT_PATH")
