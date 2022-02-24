from aiohttp import web
from aiohttp_auth import auth

from models import Advertisement, User
from serializers import AdvertisementSerializerPost, AdvertisementSerializerPatch, UserSerializer
from app import app
from config import SALT
import hashlib


class AdvertisementView(web.View):

    async def get(self):
        adv_id = self.request.match_info['adv_id']
        adv = await Advertisement.by_id(int(adv_id))
        adv_data = adv.to_dict()
        return web.json_response(adv_data)

    async def post(self):
        user_remember = await auth.get_auth(self.request)
        if user_remember is not None:
            adv_data = await self.request.json()
            adv_serialized = AdvertisementSerializerPost(**adv_data)
            adv_data = adv_serialized.dict()
            adv_data['user_id'] = int(user_remember)
            new_adv = await Advertisement.create_instance(**adv_data)
            return web.json_response(new_adv.to_dict())
        else:
            raise web.HTTPForbidden()

    async def delete(self):
        user_remember = await auth.get_auth(self.request)
        if user_remember is not None:
            adv_id = self.request.match_info['adv_id']
            adv = await Advertisement.by_id(int(adv_id))
            if adv.user_id == int(user_remember):
                await Advertisement.delete.where(Advertisement.id == adv.id).gino.status()
                return web.json_response(adv.to_dict())
            else:
                raise web.HTTPForbidden()
        else:
            raise web.HTTPForbidden()

    async def patch(self):
        user_remember = await auth.get_auth(self.request)
        if user_remember is not None:
            adv_id = self.request.match_info['adv_id']
            adv = await Advertisement.by_id(int(adv_id))
            if adv.user_id == int(user_remember):
                data = await self.request.json()
                adv_serialized = AdvertisementSerializerPatch(**data)
                data = adv_serialized.dict()
                await adv.update(**data).apply()
                return web.json_response(adv.to_dict())
            else:
                raise web.HTTPForbidden()
        else:
            raise web.HTTPForbidden()


class UserView(web.View):

    async def get(self):
        user_id = self.request.match_info['adv_id']
        user = await User.get(int(user_id))
        user_data = user.to_dict()
        return web.json_response(user_data)

    async def post(self):
        user_data = await self.request.json()
        user_serialized = UserSerializer(**user_data)
        user_data = user_serialized.dict()
        new_user = await User.create_instance(**user_data)
        return web.json_response(new_user.to_dict())


class LoginView(web.View):

    async def post(self):
        user_remember = await auth.get_auth(self.request)
        if user_remember is None:
            data = await self.request.post()
            username = data.get('username')
            email = data.get('email')
            raw_password = f'{data.get("password")}{SALT}'
            password = hashlib.md5(raw_password.encode()).hexdigest()
            user = await User.query.where(User.username == username).where(User.password == password).\
                where(User.email == email).gino.first()
            if user:
                identify = str(user.id)
                await auth.remember(self.request, identify)
                return web.json_response({'status': 200, "message": "You are logged in"})
            else:
                return web.json_response({"status": 401,
                                          "message": "Username or Password Error"})
        else:
            return web.json_response({"status": 200,
                                      "message": "You are already logged in"})


app.add_routes(
    [
        web.get('/advertisements/{adv_id:\d+}', AdvertisementView),
        web.post('/advertisements', AdvertisementView),
        web.get('/users/{user_id:\d+}', UserView),
        web.post('/users', UserView),
        web.post('/login', LoginView),
        web.delete('/advertisements/{adv_id:\d+}', AdvertisementView),
        web.patch('/advertisements/{adv_id:\d+}', AdvertisementView)
    ]
)

web.run_app(app, host='0.0.0.0', port=8080)
