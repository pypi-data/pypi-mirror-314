# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-07-26 上午10:03
# @Author : 毛鹏
import aiohttp
import time

from mangokit.models.models import ResponseModel


class AsyncRequests:
    proxies: dict = None
    timeout: int = None

    @classmethod
    async def request(cls, method, url, headers=None, **kwargs) -> ResponseModel:
        """
        处理请求的数据，写入到request对象中
        @return:
        """
        async with aiohttp.ClientSession() as session:
            s = time.time()
            async with session.request(
                    method=method,
                    url=url,
                    headers=headers or {},
                    proxy=cls.proxies.get("http") if cls.proxies else None,
                    timeout=cls.timeout if cls.timeout is not None else aiohttp.ClientTimeout(total=None),
                    **kwargs
            ) as response:
                response_text = await response.text()
                response_json = await response.json() if response.content_type == 'application/json' else None

                return ResponseModel(
                    response_time=time.time() - s,
                    headers=dict(response.headers),
                    status_code=response.status,
                    text=response_text,
                    json_data=response_json
                )

    @classmethod
    async def get(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('GET', url, headers, **kwargs)

    @classmethod
    async def post(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('POST', url, headers, **kwargs)

    @classmethod
    async def delete(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('DELETE', url, headers, **kwargs)

    @classmethod
    async def put(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('PUT', url, headers, **kwargs)


async_requests = AsyncRequests
