import asyncio
import logging
import unittest

from bubot.buject.OcfDevice.subtype.Device.Device import Device
from bubot.core.TestHelper import wait_run_device, wait_cancelled_device
from bubot_webserver.buject.OcfDevice.subtype.OcfCloudTcpServer.OcfCloudTcpServer import OcfCloudTcpServer

logging.basicConfig()
logger = logging.getLogger('Bubot_CoAP')
logger.setLevel(logging.DEBUG)


class TestCloudOcfTcpServer(unittest.IsolatedAsyncioTestCase):
    # async def test_1(self):
    #     server = OcfCloudTcpServer()
    #     await server.start_ocf_tcp_server()
    #     client1 = CloudOcfTcpClient()
    #     client2 = CloudOcfTcpClient()

    async def asyncSetUp(self) -> None:
        self.device = Device.init_from_file(di='e0', class_name='OcfCloudTcpServer')
        self.task = await wait_run_device(self.device)
        await self.device.start_cloud_endpoint()
        self.echo1_device = Device.init_from_file(di='00000000-0000-0000-0000-eeeeeeeeeee1', class_name='EchoDevice')
        self.echo1_task = await wait_run_device(self.echo1_device)
        # self.echo2_device = Device.init_from_file(di='00000000-0000-0000-0000-eeeeeeeeeee2', class_name='EchoDevice')
        # self.echo2_task = await wait_run_device(self.echo2_device)

    async def asyncTearDown(self) -> None:
        await wait_cancelled_device(self.echo1_device, self.echo1_task)
        await wait_cancelled_device(self.device, self.task)

    async def test_simple(self):
        ...

    async def test_reconnect_client(self):
        clec1 = self.echo1_device.get_param('/CoAPCloudConfResURI', 'clec')
        self.assertEqual('', clec1)
        echo1_server_connect = await self.device.stop_cloud_endpoint()
        await asyncio.sleep(10)
        clec2 = self.echo1_device.get_param('/CoAPCloudConfResURI', 'clec')
        self.assertIsNot('', clec2)
        await self.device.start_cloud_endpoint()
        await asyncio.sleep(10)
        clec3 = self.echo1_device.get_param('/CoAPCloudConfResURI', 'clec')
        self.assertEqual('', clec3)
        pass