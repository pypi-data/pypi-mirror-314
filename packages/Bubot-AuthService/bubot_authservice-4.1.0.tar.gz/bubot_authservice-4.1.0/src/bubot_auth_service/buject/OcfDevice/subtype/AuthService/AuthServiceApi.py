# from bubot.Helpers.Сryptography.SignedData import SignedData

from bubot_helpers.ActionDecorator import async_action
from bubot.core.ObjApi import DeviceApi


# from bubot.Catalog.Account.Account import Account

class AuthServiceApi(DeviceApi):
    @async_action
    async def public_api_read_auth_methods(self, view, **kwargs):
        result = {
            'Auth': {
                "methods": [
                    {
                        "id": 'Password',
                    },
                    # {
                    #     "id": 'Cert',
                    # },
                    # {
                    #     "id": 'OAuth',
                    #     "services": [
                    #         {
                    #             "id": 'Apple'
                    #         },
                    #         {
                    #             "id": 'Facebook'
                    #         },
                    #         {
                    #             "id": 'VK'
                    #         },
                    #         {
                    #             "id": 'Saby'
                    #         },
                    #         {
                    #             "id": 'Yandex'
                    #         },
                    #         {
                    #             "id": 'Google'
                    #         },
                    #         {
                    #             "id": 'Odnoklassniki'
                    #         },
                    #         {
                    #             "id": 'MailRu'
                    #         },
                    #     ]
                    # }
                ],
                "active": 0
            },
            # 'Reg': {
            #     "methods": [
            #         {
            #             "id": 'Password',
            #         },
            #         # {
            #         #     "id": 'Cert',
            #         # },
            #         # {
            #         #     "id": 'OAuth',
            #         #     "services": [
            #         #         {
            #         #             "id": 'Saby'
            #         #         }
            #         #     ]
            #         # }
            #     ],
            #     "active": 0
            # }
        }
        return self.response.json_response(result)
