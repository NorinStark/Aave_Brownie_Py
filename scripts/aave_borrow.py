from brownie import network, config, interface
from scripts.helpful_script import get_account
from scripts.get_weth import get_weth
from web3 import Web3

amount = Web3.to_wei(1, "ether")

def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    
    if network.show_active() in ["mainnet-fork", "sepolia"]:
        get_weth()

    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    
    balance = Web3.from_wei(account.balance(), "ether")
    print(f"Account balance: {balance} ETH")
    
    print("Depositing...")
    
    try:
        lending_pool.deposit(erc20_address, amount, account.address, 0, {"from": account})
    except Exception as e:
        print(f"Transaction failed: {e}")
        
    print("Deposited!")
    
    # borrowable_eth, total_debt = get_borrowable_data(lending_pool, account) 


def get_lending_pool():
    pool_addresses_provider = interface.IPoolAddressesProvider(config["networks"][network.show_active()]["pool_addresses_provider"])
    lending_pool_address = pool_addresses_provider.getPool()
    print(f"LendingPool address on {network.show_active()}: {lending_pool_address}")
    lending_pool = interface.IPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, lending_pool_address, erc20_address, account):
    print("Approving ERC20...")
    erc20 = interface.IERC20(erc20_address)
    
    allowance = erc20.allowance(account.address, lending_pool_address)
    print(f"Allowance: {Web3.from_wei(allowance, 'ether')} tokens")
    
    tx_hash = erc20.approve(lending_pool_address, amount, {"from": account})
    tx_hash.wait(1)
    print(f"Approved {Web3.from_wei(amount, 'ether')} ETH to {lending_pool_address}")
    return True

# def get_borrowable_data(lending_pool, account):
#     (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_theshold, ltv, health_factor) = lending_pool.getUserAccountData(account.address)
#     available_borrow_eth = Web3.from_wei(available_borrow_eth, "ether")
#     total_collateral_eth = Web3.from_wei(total_collateral_eth, "ether")
#     total_debt_eth = Web3.from_wei(total_debt_eth, "ether")
#     print(f"You have {total_collateral_eth} worth of ETH deposited.")
#     print(f"You have {total_debt_eth} worth of ETH borrowed.")
#     print(f"You can borrow {available_borrow_eth} worth of ETH deposited.")
#     return (float(available_borrow_eth), float(total_debt_eth))
