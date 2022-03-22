from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpfulScripts import getAccount, deploy_mocks, LOCAL_BLOCKCHAIN_ENV


def deployFundMe():
    account = getAccount()
    # pass price feed address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    return fund_me


def main():
    deployFundMe()
