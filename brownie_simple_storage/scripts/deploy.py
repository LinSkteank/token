from brownie import accounts


def deploy_simple_storage():
    # account = accounts[0]
    # print(account)
    account = accounts.load("acca")
    print(account)


def main():
    deploy_simple_storage()