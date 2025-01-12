from os import environ
import re

id_pattern = re.compile(r'^.\d+$')

# bot
API_ID = int(environ.get('API_ID', '29340327'))
API_HASH = environ.get('API_HASH', 'd963ddbf88030085b72cb3250195a12b')
BOT_TOKEN = environ.get('BOT_TOKEN', '7583224858:AAGhuOlKKMCEWypUI0dtiMo589q3La9ngDI')
ADMINS = [int(admins) if id_pattern.search(admins) else admins for admins in environ.get('ADMINS', '5056925533').split()]

# bs
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002117870388'))
fsub_eid = environ.get('-1001908798887')
FSUB_ID = int(fsub_eid) if fsub_eid and id_pattern.search(fsub_eid) else None

# database

DATABASE_URL = environ.get('DATABASE_URL', 'mongodb+srv://Autodb01:Autodb01@autodb01.iirm4.mongodb.net/?retryWrites=true&w=majority')
