import os
from dotenv import load_dotenv
from icecream import ic

ic(load_dotenv(".env.env"))

BOT_TOKEN:str = os.environ.get("BOT_TOKEN")
