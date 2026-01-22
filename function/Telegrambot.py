import telegram
from dotenv import load_dotenv, find_dotenv
import os
import sys

# .env 파일에서 환경 변수 로드
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

# # .env 파일에서 환경 변수 로드
# if getattr(sys, "frozen", False):  # PyInstaller 실행 파일
#     base_path = sys._MEIPASS # sys._MEIPASS는 PyInstaller로 컴파일된 실행환경에서만 존재.
#                             # --add-data 로 .env파일을 접근할 수 있도록 다음과 같이 진행
# else:
#     base_path = os.path.abspath(".")

# dotenv_path = os.path.join(base_path, ".env")
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     print(f".env 파일을 찾을 수 없습니다: {dotenv_path}")

# 커스터마이즈된 Bot 클래스
class TelegramBot:
    def __init__(self, token_env_key, chat_id_env_key):
        self.TELEGRAM_TOKEN = os.environ.get(token_env_key)
        self.TELEGRAM_CHAT_ID = os.environ.get(chat_id_env_key)
        self.bot = telegram.Bot(self.TELEGRAM_TOKEN)
        self.chat_id = self.TELEGRAM_CHAT_ID

    def send_message(self, message):
        """메시지를 chat_id로 전송"""
        self.bot.send_message(chat_id=self.chat_id, text=message)