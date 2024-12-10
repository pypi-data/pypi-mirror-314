import unittest
import asyncio
import logging
from aiohttp import web
from buject.OcfDevice.subtype.WebServer.WebServer import WebServer as Device
from bubot.core.TestHelper import async_test, wait_run_device, get_config_path
from buject.OcfDevice.subtype.EchoDevice.EchoDevice import EchoDevice


class TestWebServer(unittest.TestCase):
    @async_test
    async def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.device = Device.init_from_config()

    #
    @async_test
    async def test_init_without_config(self):
        device = Device.init_from_config()
        device.run()
        while device.get_param('/oic/mnt', 'status') == 'init':
            await asyncio.sleep(0.1)
        await asyncio.get_event_loop().run_forever()
        a = 1
        pass

    @async_test
    async def test_import_ui_handlers(self):
        self.device = Device.init_from_config()
        app = web.Application()
        local_devices, schemas_dir = self.device.find_drivers()
        res = self.device.add_routes(app)

    @async_test
    async def test_add_delete_device_from_update_running_device(self):
        await self.add_delete_device_from_update_running_device(Device)

    @async_test
    async def test_add_device_from_driver(self):
        test_device = EchoDevice.init_from_file()
        test_device.save_config()
        device_task = asyncio.create_task(self.device.main())
        while self.device.get_param('/oic/mnt', 'status') == 'init':
            try:
                device_task.result()
            except asyncio.InvalidStateError:
                pass
            await asyncio.sleep(0.1)

        test_device_id = test_device.di
        await self.device.action_add_device(dict(di=test_device_id, dmno=test_device.__class__.__name__))
        test_device = self.device._devices[test_device_id]
        while test_device[0].get_param('/oic/mnt', 'status') == 'init':
            try:
                test_device[1].result()
            except asyncio.InvalidStateError:
                pass
            await asyncio.sleep(0.1)
        pass

    @async_test
    async def test_load_schema(self):
        self.device.installed_devices, self.device.schemas_dir = self.device.find_drivers()
        rt = ['bubot.modbus.message']
        rt = ["bubot.serialport.con"]
        schema = self.device.get_schema_by_rt(rt)
        print(schema)


if __name__ == '__main__':
    unittest.main()
