import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from web3 import Web3

#connect to RPC
truffle_team_url = "https://sandbox.truffleteams.com/722037ca-297e-428d-bc7c-9ebb636d280e"
web3 = Web3(Web3.HTTPProvider(truffle_team_url))
print(web3.isConnected())

#create wallet
generated_account = web3.eth.account.create()
private_key_of_patient = generated_account.privateKey.hex()
patient_account_address = generated_account.address
print("patient's acc address : " + patient_account_address)
print("patient's private key : " + private_key_of_patient)
data = str({'pKey': private_key_of_patient, 'add' : patient_account_address})

#writing patient's acc details in RFID tag
GPIO.setwarnings(False)
reader = SimpleMFRC522()
try:
    print("place tag")
    reader.write(data)
    print("write done")
finally:
    GPIO.cleanup()
    
print('Tap master RFID card:')
try:
    id,master_data = reader.read()
    
finally:
    GPIO.cleanup()
print('data : ',text)
#print('ID:',id)


#transfer ethers to patients account
master_key = data_of_master_RFID['pKey']
master_address = data_of_master_RFID['address']

nonce = web3.eth.getTransactionCount(master_address)
transaction = {
    'to': patient_account_address,
    'value': web3.toWei(2, 'ether'),
    'gas': 300000,
    'gasPrice': web3.toWei('1', 'gwei'),
    'nonce': nonce  }

print('generated')
signed_tx = web3.eth.account.signTransaction(transaction, master_key)
print('signed')
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print('transacted')
print('TR hash : '+str(web3.toHex(tx_hash)))
print()
print('TR hash : '+str(web3.toHex(tx_hash)))
print()
print('#####################################################################')
print()
print('\t\tTRANSACTION HASH\t\t')
print(web3.eth.waitForTransactionReceipt(web3.toHex(tx_hash)))
print('tokens transfer successfully')

#############################################################################################################################
nonce = web3.eth.getTransactionCount(patient_account_address)

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

unicorn_txn = unicorns.functions.setProfile(
     'dharmveer',
     'o+').buildTransaction({
         'gas': 300000,
         'gasPrice': web3.toWei('1', 'gwei'),
         'nonce': nonce,})

print('generated')
signed_tx = web3.eth.account.signTransaction(unicorn_txn, private_key_of_patient)
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