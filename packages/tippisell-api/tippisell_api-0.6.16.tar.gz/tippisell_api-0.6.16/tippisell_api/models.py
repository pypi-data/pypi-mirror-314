import typing
import datetime
import pydantic
import decimal


class User(pydantic.BaseModel):
    id: int
    telegram_id: typing.Optional[int]
    username: typing.Optional[str]
    balance: decimal.Decimal
    purchases_amount: typing.Optional[decimal.Decimal] = pydantic.Field(
        None, description="Сумма покупок"
    )
    refills_amount: typing.Optional[decimal.Decimal] = pydantic.Field(
        None, description="Сумма пополнений"
    )
    language: typing.Literal["ru", "en"]
    joined_timestamp: datetime.datetime
    last_use_timestamp: datetime.datetime


class Product(pydantic.BaseModel):
    id: int
    name: str
    description: str
    type: str
    price: float
    category_id: typing.Optional[int]
    min_buy: int
    max_buy: int
    is_infinitely: bool


class HttpResponse(pydantic.BaseModel):
    status_code: int
    result: dict


class Shop(pydantic.BaseModel):
    id: int
    web: bool
    web_background: str
    web_favicon: str
    web_telegram_bot_link: bool
    bot_username: str
    uuid: pydantic.UUID4
    currency: str
    create_timestamp: datetime.datetime
    tg_bot_token: typing.Optional[str] = None
    is_blocked: bool


class GetUsersResponse(pydantic.BaseModel):
    total_count: pydantic.NonNegativeInt = pydantic.Field(
        ge=0, description="Общее количество пользователей"
    )
    data: typing.List[User]


class Purchase(pydantic.BaseModel):
    id: int
    product: Product
    user: User
    sum: decimal.Decimal
    data: typing.List[str]
    timestamp: datetime.datetime


class RequestOnMoneyBack(pydantic.BaseModel):
    id: int
    purchase: Purchase
    count_goods_invalid: int
    is_satisfied: typing.Optional[bool]
    timestamp: datetime.datetime


class GetMoneyBackRequestsResponse(pydantic.BaseModel):
    total_count: pydantic.NonNegativeInt = pydantic.Field(
        ge=0, description="Общее количество заявок"
    )
    data: typing.List[RequestOnMoneyBack]


class GetPurchasesResponse(pydantic.BaseModel):
    total_count: pydantic.NonNegativeInt = pydantic.Field(
        ge=0, description="Общее количество покупок"
    )
    data: typing.List[Purchase]


class CheckActivator(pydantic.BaseModel):
    user: User
    timestamp: datetime.datetime


class Check(pydantic.BaseModel):
    id: int
    code: str
    activations: int
    amount: decimal.Decimal
    only_for_new_users: bool
    activators: typing.List[CheckActivator]


class GetChecksResponse(pydantic.BaseModel):
    total_count: pydantic.NonNegativeInt = pydantic.Field(
        ge=0, description="Общее количество чеков"
    )
    data: typing.List[Check]
