
from os import getenv
from dotenv import load_dotenv
from pyrogram import Client
import mytelegrambot
# Recebe variaveis de ambientes setados no arquivo .env
load_dotenv()

# Inicia instancia do servidor 
app= Client(
    'Gabals_bot',
    api_id=getenv('TELEGRAM_API_ID'),
    api_hash=getenv('TELEGRAM_API_TOKEN'),
    bot_token=getenv('TELEGRAM_API_HASH')
)
print(f"api_id:{getenv('TELEGRAM_API_ID')}")

print("O SERVER TA ON 😎 ")
print("----------------------------------------------------------------") 

#inicializando todos os setups
mytelegrambot.setup(app)

# Inicia o servidor
app.run()
