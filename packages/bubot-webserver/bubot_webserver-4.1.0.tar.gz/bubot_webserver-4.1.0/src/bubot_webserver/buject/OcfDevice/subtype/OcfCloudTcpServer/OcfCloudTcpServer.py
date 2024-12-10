# from bubot_thermostat_sml1000 import __version__ as device_version
import asyncio
import logging

from Bubot_CoAP.server import Server
from bubot_helpers.ExtException import KeyNotFound

from bubot.buject.OcfDevice.subtype.Device.Device import Device
from bubot.core.DataBase.Mongo import Mongo as Storage
from .OicRd import OicRd
from .OicSecAccount import OicSecAccount
from .OicSecSession import OicSecSession

_logger = logging.getLogger(__name__)


class OcfCloudTcpServer(Device):
    file = __file__
    db = 'Bubot'
    device_table = 'device'

    def __init__(self, **kwargs):
        Device.__init__(self, **kwargs)
        self.resource_layer.add_handler('/oic/sec/account', OicSecAccount)
        self.resource_layer.add_handler('/oic/sec/session', OicSecSession)
        self.resource_layer.add_handler('/oic/rd', OicRd)
        self.connections = {}
        self.cloud = None
        self.storage = None

    # async def on_pending(self):
    #     await self.start_ocf_tcp_server()

    async def start_cloud_endpoint(self):
        cloud_url = self.get_param('/oic/con', 'cloudEndpoint', None)  # "cloudEndpoint": "coap+tcp://:8777",
        if not cloud_url:
            return
        self.cloud = Server(client_manager=self)
        await self.clear_session()
        for href in self.res:
            self.cloud.root[href] = self.res[href]
        loop = asyncio.get_running_loop()
        endpoints = await self.cloud.add_endpoint(cloud_url)
        port = endpoints[0].address[1]

        self.storage = await Storage.connect(self)

    async def stop_cloud_endpoint(self):
        if self.cloud:
            await self.cloud.close()

    async def clear_session(self):
        await self.storage.update(self.db, self.device_table, {'login': False}, filter={'server': self.di}, create=False)

    async def device_login(self, payload, address):
        di = payload['di']
        login = payload['login']
        data = {
            'login': login,
        }
        if login:
            data['server'] = self.di
        res = await self.storage.update(self.db, self.device_table, data, filter={'di': di}, create=False)
        if not res.result.matched_count:
            raise KeyNotFound(message='Device not register', detail=f'di={di}')
        if login:
            self.connections[address] = di
        return payload

    async def connection_made(self, protocol):
        pass

    async def connection_lost(self, protocol, exc):
        address = protocol.remote_address
        di = self.connections.pop(address, None)
        if di:
            await self.device_login({'di': di, "login": False}, address)
