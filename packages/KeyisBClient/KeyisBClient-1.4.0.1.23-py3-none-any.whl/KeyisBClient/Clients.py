
import os
import httpx
import asyncio
import typing as _typing
import logging as logging2
logging2.basicConfig(level=logging2.INFO)
from concurrent.futures import ThreadPoolExecutor

from KeyisBLogging import logging

from .Exceptions import Exceptions
from .core import DNS, ProtocolsManager
from .models import Url, Request, Response








class AsyncClient:
    def __init__(self):
        pass

    async def get(self,
                url: _typing.Union[Url, str],
                data=None,
                json: _typing.Optional[dict] = None,
                headers=None) -> Response:
        return await self.request("GET", url=url, data=data, json=json, headers=headers)

    async def request(self,
                      method: str,
                      url: _typing.Union[Url, str],
                      data: _typing.Mapping[str, _typing.Any] | None = None,
                      json: dict | None = None,
                      protocolVersion: _typing.Optional[str] = None,
                      **kwargs,
                      ) -> Response:
        
        if isinstance(url, str):
            url = Url(url)
        logging.info(f'Url -> {url}')

        request = Request(
            method,
            url,
            data=data,
            json=json
            )
        

        return await ProtocolsManager.requestAsync(request)

        


    async def stream(self,
                     method: str,
                     url: _typing.Union[Url, str],
                     **kwargs
                     ) -> _typing.AsyncIterator[Response]:
        
        if isinstance(url, str):
            url = Url(url)

        logging.info(f'Url -> {url}')

        request = Request(
            method,
            url,
            **kwargs
            )
        
        async for response in ProtocolsManager.streamAsync(request):
            yield response






class Client:
    def __init__(self):
        pass

    def get(self,
                url: _typing.Union[Url, str],
                data=None,
                json: _typing.Optional[dict] = None,
                headers=None) -> Response:
        return self.request("GET", url=url, data=data, json=json, headers=headers)

    def request(self,
                      method: str,
                      url: _typing.Union[Url, str],
                      data: _typing.Mapping[str, _typing.Any] | None = None,
                      json: dict | None = None,
                      protocolVersion: _typing.Optional[str] = None,
                      **kwargs,
                      ) -> Response:
        
        if isinstance(url, str):
            url = Url(url)
        logging.info(f'Url -> {url}')

        request = Request(
            method,
            url,
            data=data,
            json=json
            )
        

        return ProtocolsManager.requestSync(request)