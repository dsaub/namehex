from dotenv import load_dotenv
import os
load_dotenv()

DEBUG: bool = os.environ.get("DEBUG", "false").upper() == "TRUE"
SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
ITERATIONS = 600_000
DB_STRING: str = os.environ.get("DATABASE_URL", "sqlite:///database.db")