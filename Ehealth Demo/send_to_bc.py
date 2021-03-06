from web3 import Web3
import ipfsApi
import sha3
from ecdsa import SigningKey, SECP256k1


#add = '0x5d35F8Df974BEF29216cC6c0d5be652229383bA3'
#data_from_RFID_tag = { 'pKey':'0x8a0b04ca2719556663246e28b9ac1d20f042be8c6dc3963245d69260fd33b416', 
#'add' : '0x9da0a2cC9b25EEeF70aaEf3A9f653597E827cB89' }
filename = '317743463985.json'
api = ipfsApi.Client('https://ipfs.infura.io', 5001)
res = api.add(filename)
startTime = 'str1'
endTime = 'str2'
IPhash = res['Hash']
#api.cat(res['Hash'])
truffle_team_url = "https://sandbox.truffleteams.com/722037ca-297e-428d-bc7c-9ebb636d280e"
web3 = Web3(Web3.HTTPProvider(truffle_team_url))
print(web3.isConnected())

#in IoT we read this data using RFID
data_of_RFID = { 'pKey' : '0x8a0b04ca2719556663246e28b9ac1d20f042be8c6dc3963245d69260fd33b416',
 'address' : '0x9da0a2cC9b25EEeF70aaEf3A9f653597E827cB89'}

account_1 = data_of_RFID['address']
private_key = data_of_RFID['pKey']
nonce = web3.eth.getTransactionCount(account_1)
contract_address = Web3.toChecksumAddress('0xDa3315953330DB3AAbE7B035dB7337e0F4fE2437')

abi = '''[
	{
		"constant": true,
		"inputs": [
			{
				"name": "pec1",
				"type": "address"
			}
		],
		"name": "getData",
		"outputs": [
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "name",
				"type": "string"
			},
			{
				"name": "bloodgroup",
				"type": "string"
			}
		],
		"name": "setProfile",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getrequest",
		"outputs": [
			{
				"name": "",
				"type": "address[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "hash1",
				"type": "string"
			},
			{
				"name": "stime",
				"type": "string"
			},
			{
				"name": "etime",
				"type": "string"
			}
		],
		"name": "addHash",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "padd",
				"type": "address"
			}
		],
		"name": "addrequest",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "pec1",
				"type": "address"
			}
		],
		"name": "getIPFSHash",
		"outputs": [
			{
				"name": "",
				"type": "string[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "a1",
				"type": "address"
			}
		],
		"name": "addallowed",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	}
]'''

unicorns = web3.eth.contract(address=contract_address, abi=abi)

unicorn_txn = unicorns.functions.addHash(
     IPhash,
	 startTime,
	 endTime).buildTransaction({
         'gas': 300000,
         'gasPrice': web3.toWei('1', 'gwei'),
         'nonce': nonce,})

print('generated')
signed_tx = web3.eth.account.signTransaction(unicorn_txn, private_key)
print('signed')
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print('transacted')
print()
print('TR hash : '+str(web3.toHex(tx_hash)))
print()
print('#####################################################################')
print()
print('\t\tTRANSACTION HASH\t\t')
print(web3.eth.waitForTransactionReceipt(web3.toHex(tx_hash)))

