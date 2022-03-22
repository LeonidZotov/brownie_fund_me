from os import access
from scripts.helpfulScripts import getAccount, LOCAL_BLOCKCHAIN_ENV
from scripts.deploy import deployFundMe
from brownie import network, accounts, exceptions
import pytest


def test_can_fund():
    account = getAccount()
    fund_me = deployFundMe()
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("omly for local testing")
    fund_me = deployFundMe()
    bad_acc = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_acc})
