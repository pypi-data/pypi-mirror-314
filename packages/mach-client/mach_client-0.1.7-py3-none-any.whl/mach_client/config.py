from __future__ import annotations
from decimal import Decimal
from importlib import resources
from importlib.resources.abc import Traversable
import json
import os
from pathlib import Path
from typing import Any, Annotated

from pydantic import BaseModel, PlainValidator
import yaml

from .account import AccountManager
from .chain import Chain, constants


def add_backend_url[Model: BaseModel](model: Model, backend_url: str) -> Model:
    return type(model)(
        **{key: f"{backend_url}{value}" for key, value in model.model_dump().items()}
    )


class BackendAPIRoutes(BaseModel):
    orders: str = "/v1/orders"
    order_status: str = "/v1/orders/status"
    gas: str = "/v1/orders/gas"
    quotes: str = "/v1/quotes"
    points: str = "/v1/points"
    token_balances: str = "/tokenBalances"
    get_config: str = "/get_config"
    get_all_tokens_from_db: str = "/v1/tokens/get_all_tokens_from_db"

    def add_backend_url(self, backend_url: str) -> BackendAPIRoutes:
        return add_backend_url(self, backend_url)


class BackendConfig(BaseModel):
    url: str
    endpoints: BackendAPIRoutes = BackendAPIRoutes()


class TokenServerAPIRoutes(BaseModel):
    assets: str = "/v1/assets"
    prices: str = "/v1/prices"
    users: str = "/v1/users"

    def add_backend_url(self, backend_url: str) -> TokenServerAPIRoutes:
        return add_backend_url(self, backend_url)


class TokenServerConfig(BaseModel):
    url: str
    endpoints: TokenServerAPIRoutes = TokenServerAPIRoutes()


class TradingConfig(BaseModel):
    slippage_tolerance: Decimal


def parse_endpoint_uris(data: dict[str, str]) -> dict[Chain, str]:
    return {
        Chain.from_id(*chain_id.split(":")): endpoint_uri
        for chain_id, endpoint_uri in data.items()
        if chain_id in constants.CHAIN_ID_TO_CHAIN
    }


class Config(BaseModel):
    backend: BackendConfig
    token_server: TokenServerConfig
    trading: TradingConfig
    endpoint_uris: Annotated[dict[Chain, str], PlainValidator(parse_endpoint_uris)]


def load_abi(path: Traversable) -> Any:
    with path.open("r") as abi:
        return json.load(abi)


config_path = Path(os.environ.get("CONFIG_PATH", "config.yaml"))
with open(config_path) as config_file:
    full_config = yaml.safe_load(config_file)

config = Config.model_validate(full_config["mach_client"])

account_manager = (
    None
    if "secrets" not in full_config
    else AccountManager(**full_config["secrets"])
)

abi_path = resources.files("abi")

ethereum_order_book_abi = load_abi(abi_path / "ethereum" / "order_book.json")
tron_order_book_abi = load_abi(abi_path / "tron" / "order_book.json")

erc20_abi = load_abi(abi_path / "ethereum" / "erc20.json")
trc20_abi = load_abi(abi_path / "tron" / "trc20.json")
