import os, logging, asyncio
from logging.handlers import RotatingFileHandler
from pyrogram import Client
from dotenv import load_dotenv
from pyromod import listen
import pymongo
from pymongo import MongoClient


if os.path.exists('config.env'):
  load_dotenv('config.env')
try:
  os.makedirs('encodes/')
  os.makedirs('temp/')
  os.makedirs('downloads/')
except:
   pass


class Config(object):
  API_ID = os.environ.get("25918874")
  API_HASH = os.environ.get("87c7c525932cf3d753bea33786ad71ee")
  BOT_TOKEN = os.environ.get("6285717483:AAEblU-xKCkAPDJedbQ94ASCt5FP4uV5DuM")
  DATABASE_URL = os.environ.get("mongodb+srv://ultron:ultron@cluster0.pnaaxsa.mongodb.net/?retryWrites=true&w=majority")
  USERNAME = os.environ.get("UltronEncoder_Bot")
  LOG_CHANNEL = os.environ.get("-1001811301225")
  AUTH_USERS = list(set(int(x) for x in os.environ.get("AUTH_USERS", "5179011789").split()))
  ADMIN = list(set(int(x) for x in os.environ.get("ADMIN", "5179011789").split()))
  OWNER = list(set(int(x) for x in os.environ.get("5179011789").split()))
  TEMP = 'temp/'
  DOWNLOAD_DIR = str(os.environ.get("DOWNLOAD_DIR"))


LOG_FILE_NAME = "Logs.txt"


if os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, "r+") as f_d:
        f_d.truncate(0)


cluster = MongoClient(Config.DATABASE_URL)
db = cluster[Config.USERNAME]
collection = db["data"]
queue = db["queue"]
words = db["words"]


data = []
list_handler = []


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=2097152000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
LOGS = logging.getLogger(__name__)


bot = Client("Encoder", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, workers=2)


if not Config.DOWNLOAD_DIR.endswith("/"):
  Config.DOWNLOAD_DIR = str() + "/"
if not os.path.isdir(Config.DOWNLOAD_DIR):
  os.makedirs(Config.DOWNLOAD_DIR)
