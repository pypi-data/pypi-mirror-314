import argparse
import asyncio
from enum import Enum
import itertools
import logging
import typing

from mach_client import (
    AccountManager,
    AssetServer,
    BalancesProvider,
    Chain,
    SupportedChain,
    MachClient,
    RiskManager,
    Token,
    config as client_config,
)
from mach_client.client.risk_manager import SlippageManager
import uvloop

from . import aave, config, mach, utility, withdraw
from .aave.rebalance_manager import FrequentRebalanceManager
from .mach.destination_policy import (
    CheapChainFixedSymbolPolicy,
    DestinationPolicy,
    RandomChainFixedSymbolPolicy,
    RandomChainRandomSymbolPolicy,
    SingleChainPolicy,
)


USAGE = """
First create a `config.yaml` file following the `template.config.yaml` template and fill in your private keys for each chain under the `accounts` map.

cctt balances
    Display balances of all tokens on all supported chains from accounts specified in the config.

cctt run --source Arbitrum-USDC --destination USDC
    Perform the test using the account in the account file. 
    The first trade is made by selling the token specified by the --source argument.
    In each trade, a random chain is chosen as the destination chain and the entire balance of the source token is sold for the destination token.
    The choice of destination token is controlled by the --destination argument.
    In the next trade, the destination token becomes the new source token.
    This repeats until the program is stopped.

    Note: currently does not support trading the gas token (ETH) on any chain.

cctt aave
    Run the AAVE testing script. Constantly moves balances between the highest interest pool.
    Uses only stablecoins on a couple of low-gas chains.

cctt withdraw
    Withdraw all non-gas funds from the accounts specified in the config into the accounts specified in the `mach_cctt.withdraw` section of the config.
"""

DESCRIPTION = "Cross chain trade test (CCTT) - test swaps between random chains"

DEFAULT_SOURCE_TOKEN = "Base-USDC"

DEFAULT_DESTINATION_POLICY = "USDC"

SOURCE_TOKEN_DESCRIPTION = """
The initial token to be sold in the first trade in the form of "<chain>-<symbol>". If left empty, a random one will be chosen for you.
"""

DESTINATION_POLICY_DESCRIPTION = f"""
Controls how the destination token is chosen in each trade.
If set to "random", then a completely random chain and symbol will be chosen.
If set to "fixed:SYMBOL", then a token on a random chain with the given symbol will be chosen.
If set to "cheap:SYMBOL", then the token with the given symbol on only Arbitrum or Optimism will be chosen.
If set to "chain:CHAIN", then it trades all tokens on CHAIN one-by-one in a random order.
Defaults to `{DEFAULT_DESTINATION_POLICY}`.
"""


class Command(Enum):
    BALANCES = "balances"
    RUN = "run"
    AAVE = "aave"
    WITHDRAW = "withdraw"


async def show_balances(
    client: BalancesProvider, account_manager: AccountManager
) -> None:
    match client:
        case MachClient():
            chains = (
                SupportedChain.ETHEREUM.value,
                SupportedChain.SOLANA.value,
            )
        case AssetServer():
            chains = (
                SupportedChain.ETHEREUM.value,
                SupportedChain.SOLANA.value,
                SupportedChain.TRON.value,
            )
        case _ as arg:
            typing.assert_never(arg)

    accounts = map(
        lambda chain: account_manager[chain],
        chains,
    )

    balances = await asyncio.gather(
        *map(
            lambda account: client.get_token_balances(account.downcast()),
            accounts,
        )
    )

    iter = itertools.chain(*map(lambda balance: balance.items(), balances))

    print("Balances:")

    for _, chain_balances in iter:
        non_zero = [item for item in chain_balances.items() if item[1] > 0]

        if len(non_zero) == 0:
            continue

        print()

        for token, balance in non_zero:
            print(token.format_amount(balance))

    return


async def run() -> None:
    parser = argparse.ArgumentParser(
        prog="cctt",
        usage=USAGE,
        description=DESCRIPTION,
    )

    parser.add_argument(
        "command",
        choices=tuple(Command),
        help="Command to perform",
        nargs=1,
        type=Command,
    )

    parser.add_argument(
        "--source",
        "-s",
        default=DEFAULT_SOURCE_TOKEN,
        dest="src_token",
        help=SOURCE_TOKEN_DESCRIPTION,
        required=False,
        nargs="?",
        type=str,
    )

    parser.add_argument(
        "--destination-policy",
        "-d",
        default=DEFAULT_DESTINATION_POLICY,
        dest="destination_policy",
        help=DESTINATION_POLICY_DESCRIPTION,
        required=False,
        nargs="?",
        type=str,
    )

    arguments = parser.parse_args()

    command: Command = arguments.command[0]
    assert command, "Command required"

    asset_server = await AssetServer.create()
    logger = logging.getLogger("cctt")
    assert (account_manager := client_config.account_manager)

    if command == Command.BALANCES:
        await show_balances(asset_server, account_manager)
        await asset_server.close()
        return

    elif command == Command.WITHDRAW:
        await withdraw.withdraw(
            client=asset_server,
            account_manager=account_manager,
            recipients=config.config.withdraw,
        )
        await asset_server.close()
        return

    client = await MachClient.create()
    risk_manager: RiskManager = SlippageManager(
        asset_server,
        client_config.config.trading.slippage_tolerance,
        logger,
    )

    if command == Command.RUN:
        if arguments.src_token:
            src_token = Token.from_str(arguments.src_token)
        else:
            src_token = await utility.choose_source_token(
                client,
                client.tokens,
                account_manager[SupportedChain.ETHEREUM.value].downcast(),
            )

        logger.info(f"Source token: {src_token}")

        assert (
            arguments.destination_policy
        ), "Destination policy must be provided to run test"

        match arguments.destination_policy.split(":"):
            case ["random"]:
                logger.info("Destination token policy: randomize")
                destination_policy: DestinationPolicy = RandomChainRandomSymbolPolicy(
                    client
                )

            case ["fixed", symbol]:
                logger.info(f"Destination token policy: fixed symbol {symbol}")
                destination_policy: DestinationPolicy = RandomChainFixedSymbolPolicy(
                    client, symbol
                )

            case ["cheap", symbol]:
                logger.info(f"Destination token policy: cheap chain {symbol}")
                destination_policy: DestinationPolicy = CheapChainFixedSymbolPolicy(
                    client, symbol
                )

            case ["chain", chain]:
                logger.info(f"Destination token policy: {chain} single chain only")
                chain = Chain.from_str(chain)
                destination_policy: DestinationPolicy = SingleChainPolicy(client, chain)

            case _ as arg:
                raise ValueError(f"Invalid destination policy: {arg}")

        runner = mach.run(
            client=client,
            asset_server=asset_server,
            src_token=src_token,
            destination_policy=destination_policy,
            account_manager=account_manager,
            risk_manager=risk_manager,
            check_destination_gas=True,
            logger=logger,
        )

        async for _ in runner:
            pass

    elif command == Command.AAVE:
        async for _ in aave.run(
            client=client,
            asset_server=asset_server,
            account_manager=account_manager,
            rebalance_manager=FrequentRebalanceManager(logger),
            filter_lower_rate_tokens=False,
            risk_manager=risk_manager,
            logger=logger,
        ):
            pass

    else:
        typing.assert_never(command)

    await asyncio.gather(client.close(), asset_server.close())


def main() -> None:
    logging.getLogger().setLevel(logging.DEBUG)

    # Silence annoying aiohttp warning about unclosed client session originating from web3's code
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)

    uvloop.run(run())


if __name__ == "__main__":
    main()
