from distutils.command.config import config
from brownie import accounts, config, SimpleStorage
import os


def deploy_simple_storage():
    #geth random account
    account = accounts[0] 
    # print(account)
    # brownie saved account with name acca and password 1234
    # account = accounts.load("acca")
    # print(account)

    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # print(account)
    # acc brownie from yaml 
    # account = accounts.add(config["wallets"]["from_key"])
    # print (account)

    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    tx = simple_storage.store(15, {"from": account})
    tx.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def main():
    deploy_simple_storage()