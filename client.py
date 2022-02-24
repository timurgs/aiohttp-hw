import asyncio
import aiohttp


HOST = 'http://127.0.0.1:8080'


async def make_request(path, method='get', **kwargs):
    async with aiohttp.ClientSession() as session:
        request_method = getattr(session, method)
        async with request_method(f'{HOST}/{path}', **kwargs) as response:
            return (await response.json())


async def main():
    # response = await make_request('advertisements', 'post', json={'title': 'Шкаф IKEA',
    #                                                               'description': 'зимняя коллекция'})
    # response = await make_request('advertisements/3', 'get')
    response = await make_request('users', 'post', json={'username': 'admin7',
                                                         'password': 'sgdshjk4434FET32325',
                                                         'email': 'admin7@admin.com'})
    # response = await make_request('login', 'post', data={'username': 'admin1',
    #                                                      'password': 'sgdsSTAT4434FET32325',
    #                                                      'email': 'admin1@admin.com', })
    print(response)


asyncio.run(main())
