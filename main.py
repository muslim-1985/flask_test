from app import app
import view
from app import db

#регистрируем блюпринт для подключаемых модулей
from bot.blueprint import bot

#регистрация модуля блюпринт
app.register_blueprint(bot, url_prefix='/bot')

if __name__ == '__main__':
    app.run()