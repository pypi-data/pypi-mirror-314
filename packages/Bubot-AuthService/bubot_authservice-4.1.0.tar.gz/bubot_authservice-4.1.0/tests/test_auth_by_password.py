import urllib.parse

from bubot.core.DataBase.Mongo import Mongo as Storage
from bubot_helpers.ExtException import ExtException, Unauthorized, AccessDenied
from bubot_webserver.buject.OcfDevice.subtype.WebServer.WebServer import WebServer
from bubot.buject.User.User import User
from bubot_auth_service.buject.User.UserApi import UserApi
from aiohttp import FormData
from aiohttp.test_utils import AioHTTPTestCase
import logging

logging.basicConfig(level=logging.ERROR)


class TestAuthByPassword(AioHTTPTestCase):
    test_login = 'razgovorov'
    test_password = ''

    # async def asyncSetUp(self) -> None:
    #
    async def get_application(self):
        self.device = WebServer.init_from_file()
        self.device.log = self.device.get_logger()
        app = await self.device.run_web_server()
        self.storage = self.device.storage
        self.user = User(self.storage)
        return app.result

    async def tearDownAsync(self):
        await self.client.close()
        # self.storage.close()
        await self.device.on_stopped()

    async def delete_user_by_login(self, login):
        await self.user.find_user_by_auth('password', login)
        await self.user.delete_one()

    async def create_test_user(self):
        data = FormData({'login': self.test_login, 'password': self.test_password})
        resp = await self.client.request(
            "POST",
            "/AuthService/public_api/User/sign_up_by_password",
            data=data
        )
        resp_data = await resp.json()
        return resp, resp_data

    async def sign_in_by_password(self, login, password):
        data = FormData({'login': login, 'password': password})
        resp = await self.client.request(
            "POST",
            "/AuthService/public_api/User/sign_in_by_password",
            data=data
        )
        resp_data = await resp.json()
        if resp.status == 401:
            raise ExtException(parent=resp_data)
        return resp, resp_data
    
    def test_generate_password_hash(self):
        salt = self.test_password[:32]
        res = UserApi.generate_password_hash(salt, self.test_password)
        print(res)

    async def test_sign_up_by_password(self):
        try:
            await self.delete_user_by_login(self.test_login)
        except Unauthorized:
            pass
        resp, resp_data = await self.create_test_user()
        self.assertEqual(200, resp.status, 'response status')

        # повторный вызов должен вернуть исключение что пользователь уже зарегистрирован

        resp, resp_data = await self.create_test_user()
        self.assertEqual(500, resp.status, 'response status')
        self.assertEqual(resp_data['message'], 'Такой пользователь уже зарегистрирован', 'error_message')

    async def test_sign_in_by_password_good_password(self):
        resp, resp_data = await self.create_test_user()
        param = FormData({'login': self.test_login, 'password': self.test_password})
        resp = await self.client.request(
            "POST",
            "/public_api/AuthService/User/sign_in_by_password",
            data=param
        )
        if resp.status != 200:
            print(await resp.text())
        self.assertEqual(200, resp.status, 'response status')
        set_cookie = resp.headers.get('Set-Cookie')
        set_cookie = urllib.parse.unquote(set_cookie)
        session = set_cookie.split(';')
        self.assertEqual('session', session[0][:7], 'set session')
        session = session[0][8:]
        data = await resp.json()
        self.assertEqual(session, data['session'])

        resp = await self.client.request(
            "POST",
            "/public_api/AuthService/User/sign_in_by_password",
            data=param
        )

        set_cookie2 = resp.headers.get('Set-Cookie')
        data2 = await resp.json()

        if resp.status != 200:
            print(await resp.text())
        self.assertEqual(200, resp.status, 'response status')
        self.assertIsNone(set_cookie2, 'don\'t new session')
        self.assertEqual(session, data['session'], 'return first session')
        self.assertEqual(session, data2['session'])

        resp = await self.client.request(
            "POST",
            "/api/AuthService/User/sign_out",
            data=param
        )
        set_cookie3 = resp.headers.get('Set-Cookie')
        session2 = urllib.parse.unquote(set_cookie3).split(';')
        self.assertEqual('session', session2[0][:7], 'set session')
        session2 = session2[0][8:]
        data3 = await resp.json()
        if resp.status != 200:
            print(await resp.text())
        self.assertEqual('""', session2, 'new_session')
        self.assertEqual(200, resp.status, 'response status')
        self.assertEqual({}, data3)

    async def test_get_current_user(self):
        data = FormData({'login': self.test_login, 'password': self.test_password})
        resp = await self.client.request(
            "POST",
            "/public_api/AuthService/User/auth_by_password",
            data=data
        )
        resp = await self.client.request(
            "GET",
            "/public_api/AuthService/User/read_session_info",
        )
        print(await resp.text())
        self.assertEqual(200, resp.status, 'response status')

    async def test_sign_in_by_password_bad_password(self):
        try:
            await self.delete_user_by_login(self.test_login)
        except Unauthorized:
            pass
        resp, resp_data = await self.create_test_user()
        try:
            resp = await self.sign_in_by_password(self.test_login, 'bad')
        except Unauthorized as err:
            pass

        try:
            resp = await self.sign_in_by_password(self.test_login, 'bad')
        except Unauthorized as err:
            pass

        try:
            resp = await self.sign_in_by_password(self.test_login, 'bad')
        except AccessDenied as err:
            pass

    async def test_create_user(self):
        data = FormData({'login': 'x', 'password': 'x!'})
        resp = await self.client.request(
            "POST",
            "/AuthService/public_api/User/sign_up_by_password",
            data=data
        )
        resp_data = await resp.json()
        return resp, resp_data