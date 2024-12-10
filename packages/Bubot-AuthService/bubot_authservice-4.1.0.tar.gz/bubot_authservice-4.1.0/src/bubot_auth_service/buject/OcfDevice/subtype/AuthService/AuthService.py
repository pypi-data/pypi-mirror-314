import os.path

from bubot.buject.OcfDevice.subtype.Device.Device import Device


class AuthService(Device):
    file = __file__
    template = False

    def add_route(self, app):
        path_device = os.path.dirname(self.file)
        app.router.add_static(f'/{self.__class__.__name__}/ui/', f'{path_device}/static/ui')
        app.router.add_static(f'/{self.__class__.__name__}/i18n/', f'{self.path}/i18n')
