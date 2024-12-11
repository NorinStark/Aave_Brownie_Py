from scripts.helpful_script import get_account
from brownie import interface, config, network
from web3 import Web3

def main():
    get_weth()
    
def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    account = get_account()
    
    # Fetch the WETH contract address for the active network
    weth_address = config["networks"][network.show_active()]["weth_token"]
    weth = interface.IWeth(weth_address)
    
    # Check account balance
    balance = account.balance()
    print(f"Account balance: {Web3.from_wei(balance, 'ether')} ETH")
    
    # Ensure the account has enough balance
    if balance < Web3.to_wei(1, "ether"):
        raise ValueError("Insufficient funds to mint WETH.")
    
    # Deposit 0.1 ETH to mint WETH
    tx = weth.deposit({"from": account, "value": Web3.to_wei(1, "ether")})
    tx.wait(1)  # Wait for the transaction to be mined
    print(f"Received 1 WETH!")