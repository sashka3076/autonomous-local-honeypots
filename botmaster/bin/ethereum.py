from web3 import Web3, HTTPProvider
from solcx import compile_source
from web3.middleware import geth_poa_middleware
from sys import argv
from keys import infura_api, private_key

def compile_contract(file_path):
    with open(file_path, 'r') as f:
      source = f.read()
      source = source.replace('ip_address', argv[1])

    return compile_source(source)


def deploy_contract(w3, contract_interface, private_key):
    contract_ = w3.eth.contract(
	    abi=contract_interface['abi'],
	    bytecode=contract_interface['bin'])
    
    acct = w3.eth.account.privateKeyToAccount(private_key)
    
    construct_txn = contract_.constructor().buildTransaction({
	    'from': acct.address,
	    'nonce': w3.eth.getTransactionCount(acct.address),
	    'gas': w3.toHex(1728712),
	    'gasPrice': w3.eth.gasPrice
    })
	    
    signed = acct.signTransaction(construct_txn)
    
    txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)  
    address = w3.eth.waitForTransactionReceipt(txn_hash)['contractAddress']
    return address

if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider(infura_api))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    compiled = compile_contract('resources/ethereum/contract.sol')

    contract_id, contract_interface = compiled.popitem()
    
    print('\nDeploying contract . . .\n')
    address = deploy_contract(w3, contract_interface, private_key)
    print('Deployed to: %s' % (address))

    
