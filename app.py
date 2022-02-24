from aiohttp import web
from aiohttp_auth import auth
from aiohttp_auth import auth_middleware
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from gino import Gino
import config
import pydantic
from os import urandom


@web.middleware
async def validation_error_handler(request, handler):
    try:
        response = await handler(request)
    except pydantic.error_wrappers.ValidationError as er:
        response = web.json_response({'error': str(er)}, status=400)
    return response


policy = auth.SessionTktAuthentication(urandom(32), 60, include_ip=True)

app = web.Application(middlewares=[validation_error_handler, session_middleware(EncryptedCookieStorage(urandom(32))),
                                   auth_middleware(policy)])
db = Gino()


async def init_orm(app):
    print('Приложение стартовало')
    await db.set_bind(config.DB_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('Приложение остановилось')


app.cleanup_ctx.append(init_orm)
