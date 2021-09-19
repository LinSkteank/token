from dis import Bytecode
import imp
from itertools import chain
from turtle import width

from eth_utils import address
from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv


load_dotenv()

with open("/home/zero/Desktop/myTokenProject/web3_py_simple_storage/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)


# Compilie our Solidity

compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection":{
                "*" : {
                    "*": ["abi","metadata","evm.bytecode", "evm.sourveMap"]
                }
            }
        },
    },
    solc_version="0.6.0"
)
# print(compile_sol)



# save to json file

with open("compiled.code.json", "w") as file:
    json.dump(compile_sol, file)


# get bytecode

bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi

abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# print(abi)


# for connecting ganache

w3 = Web3(Web3.HTTPProvider("HTTP://0.0.0.0:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in pytho

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# get the latest transaction

nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": my_address, "nonce": nonce})
# print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_txn)

#Send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


print("Deployed!")
# Working with the contract, you always need
# Contract Address
# Contract abi

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call
# tr
print(simple_storage.functions.retrieve().call())
print("Updating contract...")
# print(simple_storage.functions.store(15).call())
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce +1
})

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated")
print(simple_storage.functions.retrieve().call())