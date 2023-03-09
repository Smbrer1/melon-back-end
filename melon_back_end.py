from fastapi import FastAPI
from dotenv import load_dotenv
from os import environ

from models.user_model import User

load_dotenv()
melon = FastAPI()
config_dict = environ
session = {}


@melon.get("/")
async def root() -> dict:
    return {"message": config_dict.get('DB_LINK')}


@melon.post('/authorize/')
async def authorize(user: User) -> dict:
    """"""
    session['username'] = user.username
    session['password'] = user.password
    return {'message': 'ok'}
#asdhkjashdkjahsdkjhaskjdhkashdjkashdkjashdjkashdkjhaskjdhaskjdhjakshdkjahsdkjahsdjkhaskjdhakjshdkjashdkjahsdkjhaskdjasdaksjdhakjshd

@melon.get('/authorize/')
async def get_credentials() -> dict:
    return session