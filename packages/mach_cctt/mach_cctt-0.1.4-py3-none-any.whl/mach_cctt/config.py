from decimal import Decimal
from importlib import resources
from pathlib import Path
from typing import Annotated

from mach_client import (
    AccountIDManager,
    Chain,
    SupportedChain,
    config as client_config,
)
import pydantic
from pydantic import BaseModel, PlainValidator


def parse_pool_addresses_providers(
    pool_addresses_providers: dict[str, str],
) -> dict[Chain, str]:
    return {
        Chain.from_id(*chain.split(":")): address
        for chain, address in pool_addresses_providers.items()
    }


class AaveConfig(BaseModel):
    symbols: list[str]
    supply_duration: int
    rebalance_threshold: Decimal
    pool_addresses_provider: Annotated[
        dict[Chain, str], PlainValidator(parse_pool_addresses_providers)
    ]


def parse_excluded_chains(excluded_chains: list[str]) -> frozenset[Chain]:
    return frozenset(Chain.from_id(*chain.split(":")) for chain in excluded_chains)


class PathsConfig(BaseModel):
    log_file: Path = Path("logs") / "app.log"

    @pydantic.field_validator("log_file")
    @classmethod
    def create_directory(cls, path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path


def parse_account_id_manager(private_keys: dict[str, str]) -> AccountIDManager:
    return AccountIDManager(
        **private_keys,
    )


class Config(BaseModel):
    withdraw: Annotated[AccountIDManager, PlainValidator(parse_account_id_manager)] = AccountIDManager()
    aave: AaveConfig
    excluded_chains: Annotated[
        frozenset[Chain], PlainValidator(parse_excluded_chains)
    ] = frozenset(
        (
            SupportedChain.BLAST.value,
            SupportedChain.CELO.value,
            SupportedChain.ETHEREUM.value,
            SupportedChain.MODE.value,
            SupportedChain.POLYGON.value,
        )
    )
    paths: PathsConfig = PathsConfig()


config = Config.model_validate(client_config.full_config["mach_cctt"])

# Relative to the root of the repository
abi_path = resources.files("abi")

solidity_uint_max = 2**256 - 1

aave_pool_addresses_provider_abi = client_config.load_abi(
    abi_path / "aave" / "pool_addresses_provider.json"
)

aave_protocol_data_provider_abi = client_config.load_abi(
    abi_path / "aave" / "protocol_data_provider.json"
)

aave_pool_abi = client_config.load_abi(abi_path / "aave" / "pool.json")
