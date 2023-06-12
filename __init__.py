import json

from aiogram import Bot


config = json.load(open('./json_file/config.json', 'rb'))

project = json.load(open('./json_file/project.json', 'rb'))

bot = Bot(config['TOKEN'])