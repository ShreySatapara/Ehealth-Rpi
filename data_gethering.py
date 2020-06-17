from pulsesensor import Pulsesensor
import time
import json
from datetime import datetime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import ipfsApi
from web3 import Web3

GPIO.setwarnings(False)
reader = SimpleMFRC522()
print('Tap your RFID:')
try:
    id,data = reader.read()
    #print(id)
    #print(text)
finally:
    GPIO.cleanup()
print('data :',text)
print('ID:',id)
data = json.loads(data)

p = Pulsesensor()
p.startAsyncBPM()
data = {}
filename = str(id)+'.json'
#print(filename)
data['name'] = text
data['heart'] = []
try:
    startTime = str(datetime.now())
    while True:
        bpm = p.BPM - 156
        if bpm > 0:
            
            curr_time = str(datetime.now())
            print("time : {},  BPM: {}".format(curr_time,bpm))
            data['heart'].append({'timestamp':curr_time,
                                      'heartbeat' : bpm})
            
            with open(filename, 'w') as outfile:
                json.dump(data,outfile)
        else:
            print("Please put your finger properly")
        time.sleep(1)
except KeyboardInterrupt:
    endTime = str(datetime.now())
except:
    p.stopAsyncBPM()
finally:
    api = ipfsApi.Client('https://ipfs.infura.io', 5001)
    res = api.add(filename)
    IPhash = res['Hash']

    truffle_team_url = "https://sandbox.truffleteams.com/722037ca-297e-428d-bc7c-9ebb636d280e"
    web3 = Web3(Web3.HTTPProvider(truffle_team_url))
    print(web3.isConnected())

    account_1 = data['address']
    private_key = data['pKey']
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

