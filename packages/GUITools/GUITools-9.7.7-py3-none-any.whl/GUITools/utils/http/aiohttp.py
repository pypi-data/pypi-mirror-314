# -*- coding: latin -*-

import asyncio
from time import perf_counter
import aiohttp, json
from .models import HttpMethod, UnavailableService, DataFetchHttpResult, DataFetchHttp
from typing import overload

class AioHttp(object):

    def __init__(self, base_url = "http://127.0.0.1:8000/", raise_error = False):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
        self.endpoint_test_connection = 'test-connection'
        self.raise_error = raise_error

    async def test_connection(self):
        data = DataFetchHttp("test-connection", self.endpoint_test_connection, HttpMethod.GET )
        try:
            res = await self.fetch(data)
            if res.success:
                return True
        except:
            ...

    @overload
    async def fetch(self, data: DataFetchHttp, session: aiohttp.ClientSession) -> DataFetchHttpResult:
        pass

    @overload
    async def fetch(self, data: DataFetchHttp) -> DataFetchHttpResult:
        pass

    @overload
    async def fetch(self, endpoint : str, http_method : HttpMethod, data : dict = {}) -> DataFetchHttpResult:
         pass

    @overload
    async def fetch(self, endpoint : str, http_method : HttpMethod) -> DataFetchHttpResult:
         pass

    async def fetch(self, *args) -> DataFetchHttpResult:
        if type(args[0]) == str:
            if len(args) == 3:
                endpoint, http_method, data = args 
            else:
                endpoint, http_method = args
                data = {}
            data_fetch_http = DataFetchHttp("", endpoint, http_method, data)
            async with aiohttp.ClientSession() as session:
                return await self._do_fetch(data_fetch_http, session)
        else:
            data_fetch_http = args[0]
            if len(args) == 1:
                async with aiohttp.ClientSession() as session:
                    return await self._do_fetch(data_fetch_http, session)
            else:
                session = args[1]
                return await self._do_fetch(data_fetch_http, session)

    async def _do_fetch(self, data_fetch_http: DataFetchHttp, session: aiohttp.ClientSession) -> DataFetchHttpResult:
        url = f'{self.base_url}{data_fetch_http.endpoint}'

        method = session.get 
        if data_fetch_http.http_method == HttpMethod.POST:
            method = session.post
        elif data_fetch_http.http_method == HttpMethod.PUT:
            method = session.put
        elif data_fetch_http.http_method == HttpMethod.DELETE:
            method = session.delete

        start = perf_counter()
        if data_fetch_http.http_method == HttpMethod.GET or data_fetch_http.http_method == HttpMethod.DELETE:
            async with method(url, headers=self.headers) as r:
                content = await r.text()
        else:
            async with method(url, headers=self.headers, json=data_fetch_http.data) as r:
                content = await r.text()

        content = json.loads(content)

        stop = perf_counter()
        delay = round(stop - start, 3)
        if r.status == 200:
            return DataFetchHttpResult(name=data_fetch_http.name, success=True, content=content, status_code=r.status, delay=delay)
        elif r.status == 503:
            if self.raise_error:
                raise UnavailableService()
            else:
                return DataFetchHttpResult(name=data_fetch_http.name, success=False, status_code=503, content={'error': 'Database unavailable'}, delay=delay)
        return DataFetchHttpResult(name=data_fetch_http.name, success=False, content=content, status_code=r.status, delay=delay)

    async def fetch_all(self, list_data_fetch_http: list[DataFetchHttp]) -> dict[str, DataFetchHttpResult]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(data, session) for data in list_data_fetch_http]
            res = await asyncio.gather(*tasks)
            return {t.name: t for t in res}




