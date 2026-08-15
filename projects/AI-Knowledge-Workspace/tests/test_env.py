from dotenv import load_dotenv
import os

load_dotenv()

name = os.getenv("NOT_EXIST")

if name is None:
    raise ValueError("值不存在")
