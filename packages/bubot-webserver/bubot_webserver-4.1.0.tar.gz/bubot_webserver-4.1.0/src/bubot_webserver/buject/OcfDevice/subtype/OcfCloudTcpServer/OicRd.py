from bubot.OcfResource.OcfResource import OcfResource


class OicRd(OcfResource):
    async def on_post(self, request, response):
        self.debug('post', request)
        payload = request.decode_payload()
        res = await self.device_register_resource(payload)
        self.encode_json_response(response, res)
        return self, response

    async def device_register_resource(self, payload):
        di = payload['di']

        data = {'res': payload['links']}

        res = await self.device.storage.update(self.device.db, self.device.device_table, data, filter={
            'di': di,
        })

        result = {
            'di': di,
        }
        return result

    def render_GET(self, request, response):
        """
        Method to be redefined to render a GET request on the resource.

        :param response: the partially filled response
        :param request: the request
        :return: a tuple with (the resource, the response)
        """
        raise NotImplementedError(self.__class__.__name__)
