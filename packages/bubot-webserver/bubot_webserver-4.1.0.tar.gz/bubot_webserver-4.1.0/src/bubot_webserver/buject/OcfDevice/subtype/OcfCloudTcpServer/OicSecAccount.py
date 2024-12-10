# from bubot_thermostat_sml1000 import __version__ as device_version
from uuid import uuid4

from bubot.OcfResource.OcfResource import OcfResource
from bubot.buject.User.User import User
from bubot_helpers.ExtException import ExtException


class OicSecAccount(OcfResource):
    async def on_post(self, request, response):
        self.debug('post', request)
        payload = request.decode_payload()
        res = await self.device_register(payload)
        self.encode_json_response(response, res)
        return self, response

    async def device_register(self, payload):
        try:
            di = payload['di']
            access_token = payload['accesstoken']

            # todo вызов сервиса аутентификации
            user = User(self.device.storage)
            res = await user.find_user_by_auth(f'ocf_reg_device', di)
            found_access_token = res.result['value']
            if access_token != found_access_token:
                raise ExtException(message='Bad access token')
            new_access_token = str(uuid4())
            data = {
                'user': user.get_link(),
                'di': di,
                'access_token': new_access_token
            }

            res = await self.device.storage.find_one(self.device.db, self.device.device_table, {'di': di})

            data['_id'] = res['_id'] if res else str(uuid4())

            res = await self.device.storage.update(self.device.db, self.device.device_table, data, filter={
                'di': di, '_id': data['_id']
            })

            result = {
                'uid': user.obj_id,
                'di': di,
                'accesstoken': new_access_token
            }

            return result
        except Exception as err:
            raise ExtException(parent=err)

    def render_GET(self, request, response):
        """
        Method to be redefined to render a GET request on the resource.

        :param response: the partially filled response
        :param request: the request
        :return: a tuple with (the resource, the response)
        """
        raise NotImplementedError(self.__class__.__name__)
