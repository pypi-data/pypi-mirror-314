#!/usr/bin/env python3
# coding: utf-8

from asyncio import run as asyncio_run
from httpx import AsyncClient
from enum import Enum
from decouple import config


class Product:
    class RequestMethod(Enum):
        GET = 1
        POST = 2
        DELETE = 3
        PATCH = 4
        PUT = 5

    def __init__(self, *, base_url: str | None = None, secret_token: str | None = None):
        self.BASE_URL = base_url or config("PRODUCT_BASE_URL")
        self.HEADER = {
            "Authorization": secret_token or f"Bearer {config("PRODUCT_SECRET_TOKEN")}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    # Make the Request Methods
    async def get(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.get(url=url, headers=self.HEADER, params=data)
            return response.json()

    async def post(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.post(url=url, headers=self.HEADER, json=data)
            return response.json()

    async def put(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.put(url=url, headers=self.HEADER, json=data)
            return response.json()

    async def delete(self, url: str) -> dict:
        async with AsyncClient() as client:
            response = await client.delete(url=url, headers=self.HEADER)
            return response.json()

    async def request(self, url: str, method: int, data: dict | None = None) -> dict | None:
        match method:
            case Product.RequestMethod.GET.value:
                return await self.get(url, data)

            case Product.RequestMethod.POST.value:
                return await self.post(url, data)

            case Product.RequestMethod.PUT.value:
                return await self.put(url, data)

            case Product.RequestMethod.DELETE.value:
                return await self.delete(url)

    # Product endpoints
    async def list_products_async(self) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/product",
            method=Product.RequestMethod.GET.value,
        )

    def list_products_sync(self) -> dict | None:
        return asyncio_run(self.list_products_async())

    async def get_product_async(self, product_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/product/{product_id}",
            method=Product.RequestMethod.GET.value,
        )

    def get_product_sync(self, product_id: str) -> dict | None:
        return asyncio_run(self.get_product_async(product_id=product_id))

    async def create_product_async(self, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/product",
            method=Product.RequestMethod.POST.value,
            data=data,
        )

    def create_product_sync(self, data: dict) -> dict | None:
        return asyncio_run(self.create_product_async(data=data))

    async def update_product_async(self, product_id: str, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/product/{product_id}",
            method=Product.RequestMethod.PUT.value,
            data=data,
        )

    def update_product_sync(self, product_id: str, data: dict) -> dict | None:
        return asyncio_run(self.update_product_async(product_id=product_id, data=data))

    async def delete_product_async(self, product_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/product/{product_id}",
            method=Product.RequestMethod.DELETE.value,
        )

    def delete_product_sync(self, product_id: str) -> dict | None:
        return asyncio_run(self.delete_product_async(product_id=product_id))

    # Custom Field endpoints
    async def create_custom_field_async(self, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customField",
            method=Product.RequestMethod.POST.value,
            data=data,
        )

    def create_custom_field_sync(self, data: dict) -> dict | None:
        return asyncio_run(self.create_custom_field_async(data=data))

    async def list_custom_fields_async(self) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customField",
            method=Product.RequestMethod.GET.value,
        )

    def list_custom_fields_sync(self) -> dict | None:
        return asyncio_run(self.list_custom_fields_async())

    async def get_custom_field_async(self, field_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customField/{field_id}",
            method=Product.RequestMethod.GET.value,
        )

    def get_custom_field_sync(self, field_id: str) -> dict | None:
        return asyncio_run(self.get_custom_field_async(field_id=field_id))

    async def update_custom_field_async(self, field_id: str, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customField/{field_id}",
            method=Product.RequestMethod.PUT.value,
            data=data,
        )

    def update_custom_field_sync(self, field_id: str, data: dict) -> dict | None:
        return asyncio_run(self.update_custom_field_async(field_id=field_id, data=data))

    async def delete_custom_field_async(self, field_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customField/{field_id}",
            method=Product.RequestMethod.DELETE.value,
        )

    def delete_custom_field_sync(self, field_id: str) -> dict | None:
        return asyncio_run(self.delete_custom_field_async(field_id=field_id))

    # Group endpoints
    async def create_group_async(self, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/groups",
            method=Product.RequestMethod.POST.value,
            data=data,
        )

    def create_group_sync(self, data: dict) -> dict | None:
        return asyncio_run(self.create_group_async(data=data))

    async def list_groups_async(self) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/groups",
            method=Product.RequestMethod.GET.value,
        )

    def list_groups_sync(self) -> dict | None:
        return asyncio_run(self.list_groups_async())

    async def get_group_async(self, group_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/groups/{group_id}",
            method=Product.RequestMethod.GET.value,
        )

    def get_group_sync(self, group_id: str) -> dict | None:
        return asyncio_run(self.get_group_async(group_id=group_id))

    async def update_group_async(self, group_id: str, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/groups/{group_id}",
            method=Product.RequestMethod.PUT.value,
            data=data,
        )

    def update_group_sync(self, group_id: str, data: dict) -> dict | None:
        return asyncio_run(self.update_group_async(group_id=group_id, data=data))

    async def delete_group_async(self, group_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/groups/{group_id}",
            method=Product.RequestMethod.DELETE.value,
        )

    def delete_group_sync(self, group_id: str) -> dict | None:
        return asyncio_run(self.delete_group_async(group_id=group_id))

    # Custom Field Value endpoints
    async def create_custom_field_value_async(self, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customFieldValue",
            method=Product.RequestMethod.POST.value,
            data=data,
        )

    def create_custom_field_value_sync(self, data: dict) -> dict | None:
        return asyncio_run(self.create_custom_field_value_async(data=data))

    async def list_custom_field_values_async(self) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customFieldValue",
            method=Product.RequestMethod.GET.value,
        )

    def list_custom_field_values_sync(self) -> dict | None:
        return asyncio_run(self.list_custom_field_values_async())

    async def get_custom_field_value_async(self, value_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customFieldValue/{value_id}",
            method=Product.RequestMethod.GET.value,
        )

    def get_custom_field_value_sync(self, value_id: str) -> dict | None:
        return asyncio_run(self.get_custom_field_value_async(value_id=value_id))

    async def update_custom_field_value_async(self, value_id: str, data: dict) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customFieldValue/{value_id}",
            method=Product.RequestMethod.PUT.value,
            data=data,
        )

    def update_custom_field_value_sync(self, value_id: str, data: dict) -> dict | None:
        return asyncio_run(self.update_custom_field_value_async(value_id=value_id, data=data))

    async def delete_custom_field_value_async(self, value_id: str) -> dict | None:
        return await self.request(
            url=f"{self.BASE_URL}/customFieldValue/{value_id}",
            method=Product.RequestMethod.DELETE.value,
        )

    def delete_custom_field_value_sync(self, value_id: str) -> dict | None:
        return asyncio_run(self.delete_custom_field_value_async(value_id=value_id))
