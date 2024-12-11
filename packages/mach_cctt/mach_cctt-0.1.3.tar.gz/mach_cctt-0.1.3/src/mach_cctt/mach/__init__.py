from typing import AsyncGenerator

from mach_client import (
    AccountManager,
    AssetServer,
    ChainClient,
    MachClient,
    RiskManager,
    Token,
)
from mach_client.client.event import (
    DestinationNotReceived,
    InsufficientSourceBalance,
    Trade,
)

from .. import utility
from ..log import Logger
from .destination_policy import DestinationPolicy
from .event import (
    GasEstimateFailed,
    InsufficientDestinationGas,
    NoViableDestination,
    TestEvent,
)


async def run(
    *,
    client: MachClient,
    asset_server: AssetServer,
    src_token: Token,
    destination_policy: DestinationPolicy,
    account_manager: AccountManager,
    risk_manager: RiskManager,
    check_destination_gas: bool = True,
    logger: Logger,
) -> AsyncGenerator[TestEvent, None]:
    destination_policy.exclude_token(src_token)

    while dest_token := destination_policy():
        destination_policy.exclude_token(dest_token)
        dest_account = account_manager[dest_token.chain]

        if check_destination_gas:
            try:
                gas_response = await client.estimate_gas(dest_token.chain)
            except Exception as e:
                logger.error("Gas estimate failed:", exc_info=e)
                yield GasEstimateFailed(dest_token.chain, e)
                continue

            logger.debug(f"Gas estimate: {gas_response}")
            estimated_gas = gas_response.gas_estimate * gas_response.gas_price
            logger.debug(f"Estimated gas cost: {estimated_gas}")

            dest_client = await ChainClient.create(dest_token.chain)
            gas_available = await dest_client.get_gas_balance(dest_account.downcast())
            logger.debug(f"Available gas: {gas_available}")

            if gas_available < estimated_gas:
                logger.info(
                    f"Insufficient gas on chain {dest_token.chain}, will be excluded from future selection"
                )
                destination_policy.permanently_exclude_chain(dest_token.chain)
                yield InsufficientDestinationGas(
                    dest_token, gas_response, gas_available
                )
                continue

        src_account = account_manager[src_token.chain]
        amount = await src_token.get_balance(src_account.downcast())

        event = await client.place_trade(
            src_token=src_token,
            dest_token=dest_token,
            amount=amount,
            account=src_account,
            recipient=dest_account.downcast(),
            risk_manager=risk_manager,
            logger=logger,
        )

        match event:
            case InsufficientSourceBalance():
                yield event
                break

            # Our funds were pulled but we didn't get anything back on the destination chain
            # We have to choose a completely different source token to be able to continue trading
            case DestinationNotReceived():
                yield event

                destination_policy.reset()

                src_token = await utility.choose_source_token(
                    asset_server,
                    destination_policy.token_choices,
                    src_account.downcast(),
                )

            case Trade():
                yield event
                src_token = dest_token
                destination_policy.reset()

            case _:
                yield event
                continue

        destination_policy.exclude_token(src_token)

    yield NoViableDestination(destination_policy)
