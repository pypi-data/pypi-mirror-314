import io
import http
import typing
import aiohttp
import decimal
import json

from tippisell_api import exceptions, methods, models


class Client:
    def __init__(
        self,
        shop_id: typing.Optional[typing.Union[str, int]],
        api_key: str,
        endpoint: str = "https://tippisell.xyz/api",
    ):
        if shop_id is not None:
            self.shop_id = str(shop_id)

        self.shop_id = shop_id
        self.api_key = api_key

        self._endpoint = endpoint

    async def get_user(self, user_id=None, telegram_id=None) -> models.User:
        result = await self._request(
            methods.GetUser(user_id=user_id, telegram_id=telegram_id)
        )
        return models.User(**result)

    async def upload_goods(self, product_id: int, data: typing.List[str]) -> int:
        result = await self._request(
            methods.UploadGoods(product_id=product_id, data=data)
        )
        return result["count"]

    async def upload_goods_files(
        self, product_id: int, file: io.BytesIO, file_name: str
    ) -> int:
        data = aiohttp.FormData()
        data.add_field("file", file, filename=file_name)
        data.add_field(
            "payload",
            json.dumps(
                self._clear_dict({"product_id": product_id, "shop_id": self.shop_id})
            ),
        )

        result = await self._request(
            path="/v2/product/upload-file", http_method="post", data=data
        )
        return result["count"]

    async def get_purchases(
        self,
        user_id: typing.Optional[typing.Union[str, int]] = None,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
    ) -> models.GetPurchasesResponse:
        path = "/v2/purchase/all"
        params = {
            "user_id": user_id,
            "limit": limit,
            "offset": offset,
            "shop_id": self.shop_id,
        }
        result = await self._request(
            path=path, http_method="get", params=self._clear_dict(params)
        )
        return models.GetPurchasesResponse(**result)

    async def get_shop(self, shop_id: typing.Optional[int] = None) -> models.Shop:
        if shop_id is not None and self.shop_id is None:
            shop_id = str(shop_id)
        if shop_id is None and self.shop_id is None:
            raise RuntimeError("shop_id is None")
        if shop_id is None and self.shop_id is not None:
            shop_id = self.shop_id

        result = await self._request(
            path="/v2/shop", http_method="get", params={"shop_id": shop_id}
        )
        return models.Shop(**result)

    async def get_products(
        self, offset: typing.Optional[int] = None, limit: typing.Optional[int] = None
    ) -> dict:
        result = await self._request(
            methods.GetProducts(shop_id=self.shop_id, offset=offset, limit=limit)
        )
        return result

    async def get_refills(
        self,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
    ) -> dict:
        path = "/v2/refill/all"
        params = {"offset": offset, "limit": limit, "shop_id": self.shop_id}
        result = await self._request(
            path=path, http_method="get", params=self._clear_dict(params)
        )
        return result

    async def get_categories(
        self, offset: typing.Optional[int] = None, limit: typing.Optional[int] = None
    ) -> dict:
        result = await self._request(
            path="/v2/category/all",
            http_method="get",
            params=self._clear_dict(
                {"offset": offset, "limit": limit, "shop_id": self.shop_id}
            ),
        )
        return result

    async def get_positions(self, product_id: typing.Union[str, int]):
        result = await self._request(
            path="/v2/position/all",
            http_method="get",
            params=self._clear_dict(
                {"shop_id": self.shop_id, "product_id": product_id}
            ),
        )
        return result

    async def create_product(
        self,
        name: str,
        description: str,
        product_type: typing.Literal["text", "file"],
        price: float,
        category_id: typing.Optional[int] = None,
        min_buy: typing.Optional[int] = 1,
        max_buy: typing.Optional[int] = 9999,
        message_after_byu: typing.Optional[str] = None,
        is_infinitely: bool = False,
    ) -> dict:
        result = await self._request(
            methods.CreateProduct(
                shop_id=self.shop_id,
                name=name,
                description=description,
                type=product_type,
                price=price,
                category_id=category_id,
                min_buy=min_buy,
                max_buy=max_buy,
                message_after_byu=message_after_byu,
                is_infinitely=is_infinitely,
            )
        )
        return result

    async def delete_product(self, product_id: int):
        await self._request(methods.DeleteProduct(id=product_id))

    async def get_count_positions_in_product(self, product_id: int) -> int:
        result = await self._request(
            methods.GetCountPositionsInProduct(product_id=product_id)
        )
        return result["count"]

    async def get_users(
        self,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        order: typing.Optional[str] = None,
        direction: typing.Optional[typing.Literal["asc", "desc"]] = None,
        search: typing.Optional[str] = None,
        add_purchases_amount: typing.Optional[bool] = None,
        add_refills_amount: typing.Optional[bool] = None,
    ) -> models.GetUsersResponse:
        if add_purchases_amount is not None:
            add_purchases_amount = int(add_purchases_amount)
        if add_refills_amount is not None:
            add_refills_amount = int(add_refills_amount)
        params = {
            "offset": offset,
            "limit": limit,
            "order": order,
            "direction": direction,
            "search": search,
            "shop_id": self.shop_id,
            "add_purchases_amount": add_purchases_amount,
            "add_refills_amount": add_refills_amount,
        }
        result = await self._request(
            path="/v2/user/all",
            http_method="get",
            params=self._clear_dict(params),
        )
        return models.GetUsersResponse(**result)

    async def user_balance_decrease(
        self, user_id: int, amount: typing.Union[int, float, decimal.Decimal]
    ) -> models.User:
        result = await self._request(
            path="/v2/user/{}/decrease-balance".format(user_id),
            http_method="put",
            json={"amount": str(amount), "shop_id": self.shop_id},
        )
        return models.User(**result)

    async def get_request_on_money_backs(
        self,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        order: typing.Optional[str] = None,
        direction: typing.Optional[typing.Literal["asc", "desc"]] = None,
        search: typing.Optional[str] = None,
        user_id: typing.Optional[int] = None,
    ) -> models.GetMoneyBackRequestsResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "order": order,
            "direction": direction,
            "search": search,
            "shop_id": self.shop_id,
            "user_id": user_id,
        }

        result = await self._request(
            path="/v2/request-on-money-back/all",
            http_method="get",
            params=self._clear_dict(params),
        )
        return models.GetMoneyBackRequestsResponse(**result)

    async def get_checks(
        self,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        order: typing.Optional[str] = None,
        direction: typing.Optional[typing.Literal["asc", "desc"]] = None,
    ) -> models.GetChecksResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "order": order,
            "direction": direction,
            "shop_id": self.shop_id,
        }
        result = await self._request(
            path="/v2/check/all",
            http_method="get",
            params=self._clear_dict(params),
        )
        return models.GetChecksResponse(**result)

    async def check_delete(self, check_id: int):
        path = "/v2/check/{}".format(check_id)
        result = await self._request(
            path=path, http_method="delete", json={"shop_id": self.shop_id}
        )
        return result

    async def positions_delete_by_product_id(self, product_id: int) -> int:
        path = "/v2/position/{}/by-product-id".format(product_id)
        result = await self._request(
            path=path, http_method="delete", json={"shop_id": self.shop_id}
        )
        return result["count"]

    async def create_category(
        self, name: str, description: str, parent_id: typing.Optional[int] = None
    ):
        path = "/category"
        payload = {
            "shop_id": self.shop_id,
            "name": name,
            "description": description,
            "parent_id": parent_id,
        }

        async with aiohttp.ClientSession(headers={"api-key": self.api_key}) as session:
            response = await session.post(
                self._endpoint + path, json=self._clear_dict(payload)
            )
            await response.read()

        return await response.json()

    async def get_pre_orders(self, limit: typing.Optional[int] = None) -> dict:
        path = "/v2/pre-order/all"
        params = {"limit": limit, "shop_id": self.shop_id}
        result = await self._request(
            path=path, http_method="get", params=self._clear_dict(params)
        )
        return result

    async def pre_order_cancel(self, pre_order_id: int) -> dict:
        path = "/v2/pre-order/cancel"
        payload = {"pre_order_id": pre_order_id, "shop_id": self.shop_id}
        await self._request(
            path=path, http_method="put", json=self._clear_dict(payload)
        )

    async def _request(
        self,
        method: typing.Optional[methods.BaseMethod] = None,
        path: typing.Optional[str] = None,
        http_method: typing.Optional[
            typing.Literal["get", "post", "put", "delete"]
        ] = None,
        **kwargs,
    ):
        if method is not None:
            method.attach_shop_id(self.shop_id)
            method.attach_api_key(self.api_key)
            method.validate()

            async with aiohttp.ClientSession() as session:
                data = self._http_request_kwargs(method)
                response = await session.request(**data)
                await response.read()
        else:
            async with aiohttp.ClientSession(
                headers={"api-key": self.api_key}
            ) as session:
                response = await session.request(
                    http_method, self._endpoint + path, **kwargs
                )
                await response.read()

        result = await response.json()
        self._check_response(
            models.HttpResponse(status_code=response.status, result=result)
        )

        return result["result"]

    def _http_request_kwargs(self, method: methods.BaseMethod) -> dict:
        if "get" == method.http_method:
            kwargs = {
                "params": method.get_params(),
            }
        elif method.http_method in ["post", "delete"]:
            kwargs = {"json": method.get_json()}
        else:
            raise NameError

        kwargs["method"] = method.http_method
        kwargs["headers"] = method.get_headers()
        kwargs["url"] = self._endpoint + method.path
        return kwargs

    @classmethod
    def _check_response(cls, http_response: models.HttpResponse):
        if http.HTTPStatus.UNAUTHORIZED == http_response.status_code:
            raise exceptions.InvalidApiKey

        if http_response.result["ok"] is False:
            raise exceptions.BaseTippisellException(http_response.result["message"])

    @classmethod
    def _clear_dict(cls, data: dict) -> dict:
        return {key: value for key, value in data.items() if value is not None}
