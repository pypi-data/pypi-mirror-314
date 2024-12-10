from bubot.OcfResource.OcfResource import OcfResource


class OicSecSession(OcfResource):

    async def _on_post(self, request, payload, response):
        res = await self.device.device_login(payload, request.source)
        return self.payload

    def render_GET(self, request, response):
        """
        Method to be redefined to render a GET request on the resource.

        :param response: the partially filled response
        :param request: the request
        :return: a tuple with (the resource, the response)
        """
        raise NotImplementedError(self.__class__.__name__)
