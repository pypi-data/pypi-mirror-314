from __future__ import annotations
import logging
from pprint import pformat
import typing
from typing import Any, Iterator, NamedTuple, TypedDict

from aiohttp import ClientSession, ClientResponse
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3

from . import config
from .constants import ChainId


# Note: we should really just be deserializing the backend types with BaseModel.validate_from_json
# - https://github.com/tristeroresearch/cache-half-full/blob/62b31212f0456e4fad564021289816d39345b49b/backend/api/v1/endpoints/quotes.py#L51
# - https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate_json


class Order(TypedDict):
    id: str
    taker_address: ChecksumAddress
    maker_address: ChecksumAddress
    src_asset_address: ChecksumAddress
    dst_asset_address: ChecksumAddress
    src_chain: str
    dst_chain: str
    src_amount: int
    dst_amount: int
    created_at: str
    filled_at: str
    expires_at: str
    completed: bool
    place_tx: HexBytes
    fill_tx: HexBytes
    eta: int


class GasEstimate(TypedDict):
    gas_estimate: int
    gas_price: int


class Quote(TypedDict):
    wallet_address: str
    src_chain: str
    dst_chain: str
    src_amount: int
    dst_amount: int
    bond_amount: int
    bond_fee: int
    src_asset_address: ChecksumAddress
    dst_asset_address: ChecksumAddress
    bond_asset_address: ChecksumAddress
    challenge_offset: int
    challenge_window: int
    invalid_amount: bool
    liquidity_source: str
    created_at: str
    expires_at: str


class WalletPoints(NamedTuple):
    wallet: ChecksumAddress
    points: int

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> WalletPoints:
        return cls(Web3.to_checksum_address(json["wallet"]), int(json["points"]))


# This class is made to be used as a singleton (see below)
class MachClient:
    backend_url = config.backend_url

    # Routes
    orders = config.backend_url + config.endpoints["orders"]
    gas = config.backend_url + config.endpoints["gas"]
    quotes = config.backend_url + config.endpoints["quotes"]
    points = config.backend_url + config.endpoints["points"]
    token_balances = config.backend_url + config.endpoints["token_balances"]
    get_config = config.backend_url + config.endpoints["get_config"]

    # Make some configuration accessible to the user
    endpoint_uris = config.endpoint_uris

    def __init__(self):
        self.logger = logging.getLogger("mach-client")

        # Contains data for all chains
        self.deployments: dict[ChainId, dict[str, Any]] = {}

        # Contains only data for supported chains
        self.gas_tokens: dict[ChainId, str] = {}
        self.chains: set[ChainId] = set()
        self.symbol_by_contract: dict[tuple[ChainId, ChecksumAddress], str] = {}

    _singleton = None

    @classmethod
    async def create(cls):
        if MachClient._singleton:
            return MachClient._singleton

        MachClient._singleton = cls()
        await MachClient._singleton.init()
        return MachClient._singleton

    async def init(self) -> None:
        self.session = ClientSession()
        self.session.headers.update(
            {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        await self.refresh()

    async def refresh(self) -> None:
        # Fetch config from API
        async with self.session.get(self.get_config) as response:
            self.raw_deployments: dict[str, dict[str, Any]] = (
                await self._validate_response(response)
            )["deployments"]

        # Initialize attributes
        for chain_name, chain_data in self.raw_deployments.items():
            chain_id = ChainId.from_name(chain_name)

            if chain_id not in self.endpoint_uris:
                self.logger.warning(f"{chain_id} endpoint URI missing from config")
                continue

            # Convert from chain names to chain IDs
            del chain_data["chain_id"]
            self.deployments[chain_id] = chain_data

            self.symbol_by_contract.update(
                {
                    (chain_id, token_data["address"]): symbol
                    for symbol, token_data in chain_data["assets"].items()
                }
            )

            self.chains.add(chain_id)

            # The gas token has "wrapped": True
            gas_tokens: Iterator = filter(
                lambda item: item[1].get("wrapped"), chain_data["assets"].items()
            )

            # Maps (symbol name, symbol data) -> symbol name
            gas_tokens = map(lambda item: item[0], gas_tokens)

            try:
                gas_token = next(gas_tokens)
            except StopIteration:
                self.logger.warning(f"No gas token in config of {chain_id}")
                continue

            self.gas_tokens[chain_id] = gas_token

            assert not (
                gas_token_2 := next(gas_tokens, None)
            ), f"Multiple gas tokens on {chain_id}: {gas_token}, {gas_token_2}"

    async def close(self) -> None:
        if hasattr(self, "session"):
            await self.session.close()

    async def _validate_response(self, response: ClientResponse) -> Any:
        match response.status:
            case 200:
                return await response.json()

            case 422:
                raise ValueError(
                    f"Validation error - invalid request: {pformat(await response.json())}"
                )

            case _:
                raise RuntimeError(
                    f"Unknown status code {response.status}: {pformat(await response.json())}"
                )

    def _format_order(self, order: Order) -> Order:
        order["place_tx"] = HexBytes(order["place_tx"])

        if fill_tx := order.get("fill_tx", None):
            order["fill_tx"] = HexBytes(fill_tx)

        return order

    async def submit_order(self, chain: ChainId, place_taker_tx: HexBytes) -> Order:
        json = {
            "chain": str(chain),
            "place_taker_tx": place_taker_tx.hex(),
        }

        async with self.session.post(self.orders, json=json) as response:
            return self._format_order(await self._validate_response(response))

    async def get_orders(self, wallet: ChecksumAddress) -> list[Order]:
        params = {
            "wallet": wallet,
        }

        async with self.session.get(self.orders, params=params) as response:
            orders = await self._validate_response(response)

        return list(map(self._format_order, orders))

    async def estimate_gas(self, chain: ChainId) -> GasEstimate:
        params = {"chain": str(chain)}

        async with self.session.get(self.gas, params=params) as response:
            json = await self._validate_response(response)

        return typing.cast(GasEstimate, json)

    async def request_quote(
        self,
        src_token: Token,
        dest_token: Token,
        src_amount: int,
        wallet: ChecksumAddress,
    ) -> Quote:
        json = {
            "dst_asset_address": dest_token.contract_address,
            "dst_chain": dest_token.chain.name,
            "src_amount": src_amount,
            "src_asset_address": src_token.contract_address,
            "src_chain": src_token.chain.name,
            "wallet_address": wallet,
        }

        async with self.session.post(self.quotes, json=json) as response:
            json = await self._validate_response(response)

        return typing.cast(Quote, json)

    async def get_all_points(self, limit: int = 10) -> list[WalletPoints]:
        params = {
            "limit": limit,
        }

        async with self.session.get(self.points, params=params) as response:
            json = await self._validate_response(response)

        return [WalletPoints.from_json(item) for item in json]

    async def get_points(self, wallet: ChecksumAddress) -> int:
        async with self.session.get(self.points + f"/{wallet}") as response:
            json = await self._validate_response(response)

        return int(json["points"])

    async def get_token_balances(
        self, wallet_address: ChecksumAddress
    ) -> dict[ChainId, dict[str, int]]:
        params = {"wallet_address": wallet_address}

        async with self.session.get(self.token_balances, params=params) as response:
            raw_balances: dict[str, dict[str, int]] = (
                await self._validate_response(response)
            )["balances"]

        return dict(
            # Filter out chains we don't support
            filter(
                lambda item: item[0] in self.chains,
                # Map chain names to IDs
                map(
                    lambda item: (ChainId.from_name(item[0]), item[1]),
                    raw_balances.items(),
                ),
            )
        )


# Singleton - call await client.init() from your application
client = MachClient()
