import unittest
from aiohttp import web
from bubot_helpers.preemption import delta_seconds, wait_dest_time

from bubot_helpers.ServerTimeDifference import ServerTimeDifference
import asyncio


class TestPreemption(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        pass

    async def asyncSetUp(self) -> None:
        pass

    async def test_preemption(self):
        await self.start_web_server()
        for debug_time_offset, delay in [
            (0.1, 0.1),
            (3, 0.1),
            (-2.15432, 1.2),
            (2.15432, 1.2),
            (5.456234, 0.2),
        ]:
            preemption = await self.calc_preemption(debug_time_offset, delay)
            print(preemption - debug_time_offset, debug_time_offset, preemption)
        pass

    async def calc_preemption(self, debug_time_offset, delay):
        server_time = ServerTimeDifference(
            {
                'url': 'http://localhost:8765',
                'method': 'get',
                'params': {'delay': delay}
            }, debug_time_offset=debug_time_offset)
        preemption = await server_time.calc()
        return preemption

    async def start_web_server(self):
        async def hello(request):
            delay = float(request.query.get('delay', 0.1))
            await asyncio.sleep(delay)
            return web.Response(text="Hello, world")

        app = web.Application()
        app.add_routes([web.get('/', hello)])
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, None, 8765)
        await site.start()
