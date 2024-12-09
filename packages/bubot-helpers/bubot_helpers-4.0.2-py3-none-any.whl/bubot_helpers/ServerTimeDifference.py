from datetime import datetime, timedelta, UTC
from bubot_helpers.preemption import wait_dest_time, delta_seconds, dest_time_with_preemption


class ServerTimeDifference:
    def __init__(self, request_param, *, debug_time_offset=None):
        self.request_param = request_param
        self.debug_time_offset = debug_time_offset

    async def _test_request(self, preemption):
        import aiohttp
        t0 = (datetime.now(UTC) + timedelta(seconds=1)).replace(microsecond=0)
        start_time = dest_time_with_preemption(t0, preemption)
        await wait_dest_time(start_time)

        t1 = datetime.now(UTC)
        async with aiohttp.ClientSession() as session:
            async with session.request(**self.request_param) as response:
                t2 = datetime.now(UTC)
                headers_date = response.headers['Date']
                ts = datetime.strptime(headers_date, '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=UTC)
                if self.debug_time_offset:
                    ts = dest_time_with_preemption(t2, self.debug_time_offset).replace(microsecond=0)
        return t0, t1, t2, ts

    @classmethod
    async def calc(cls, request_param, *, debug_time_offset=None):
        self = cls(request_param, debug_time_offset=debug_time_offset)

        preemption = 0.0
        t0, t1, t2, ts = await self._test_request(preemption)
        zero_delta = delta_seconds(ts, t0)
        delta = zero_delta
        step = 0.4
        k = 1
        preemptions = [preemption]
        while step >= 0.025:
            preemption0 = round(preemption + step * k, 2)
            if preemption0 in preemptions:
                if zero_delta == delta:
                    if k < 0:
                        k *= -1
                else:
                    if k > 0:
                        k *= -1
                step /= 2
                preemption = round(preemption + step * k, 2)
            else:
                preemption = preemption0
            preemptions.append(preemption)
            t0, t1, t2, ts = await self._test_request(preemption * -1)
            delta = delta_seconds(ts, t0)
            if zero_delta == delta:
                if k < 0:
                    k *= -1
                    step /= 2
            else:
                if k > 0:
                    k *= -1
                    step /= 2
        if zero_delta == delta:
            ts0 = ts + timedelta(seconds=1 - step * 2)
        else:
            ts0 = ts - timedelta(seconds=step * 2)
        result = delta_seconds(t2, ts0)
        return result
