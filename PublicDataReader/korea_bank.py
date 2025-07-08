import os
import pandas as pd
import time
from PublicDataReader import Ecos

# .env 파일이 있다면 로드 (선택사항)

from dotenv import load_dotenv
load_dotenv()
    

service_key = os.getenv("KOREA_BANK")

