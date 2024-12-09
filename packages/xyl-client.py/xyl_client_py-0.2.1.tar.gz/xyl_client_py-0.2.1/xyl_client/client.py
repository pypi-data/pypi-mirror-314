import requests
import json
from web3 import Web3

class Eth:
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        
    def _send_request(self, method, params=None):
        """Helper function to send a JSON-RPC request."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.rpc_url, json=payload, headers=headers)
        response.raise_for_status()
        try:
            res = response.json()
        except:
            res = response.text
        else:
            res = response.json()['result']
        finally:
            return res


    def eth_chainId(self):
        return self._send_request("eth_chainId")

    def eth_blockNumber(self):
        return self._send_request("eth_blockNumber")

    def eth_getBlockByNumber(self, block_number, full_transactions=False):
        params = [hex(block_number)] # [hex(block_number) if isinstance(block_number, int) else block_number, full_transactions]
        return self._send_request("eth_getBlockByNumber", params)

    def eth_getBalance(self, address):
        params = [address]
        return self._send_request("eth_getBalance", params)

    def eth_getTransactionByHash(self, tx_hash):
        return self._send_request("eth_getTransactionByHash", [tx_hash])

    def eth_getBlockByHash(self, block_hash, full_transactions=False):
        params = [block_hash]
        return self._send_request("eth_getBlockByHash", params)

    def eth_getCode(self, address, block_number="latest"):
        params = [address, block_number]
        return self._send_request("eth_getCode", params)

    def eth_estimateGas(self, transaction):
        """
        Syntax: {"gasPrice": gas price per unit in xei, "value": transaction amount in xei}
        """
        return self._send_request("eth_estimateGas", [transaction])

    def eth_gasPrice(self):
        return int(self._send_request("eth_gasPrice"), 16)

    def eth_getTransactionCount(self, address):
        params = [address]
        return self._send_request("eth_getTransactionCount", params)

    def eth_sendRawTransaction(self, raw_transaction):
        return self._send_request("eth_sendRawTransaction", [raw_transaction])

    def net_version(self):
        return self._send_request("net_version")

    def eth_getTransactionReceipt(self, tx_index):
        return self._send_request("eth_getTransactionReceipt", [tx_index])        

class Client:
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url
        self.eth = Eth(rpc_url)
        self.chainId = self.eth.eth_chainId() 

    # Define a function to create a transaction
    def create_transaction(self, sender, to, value: int, data=None):
        if not Web3.is_checksum_address(sender):
            sender = Web3.to_checksum_address(sender)
            
        gas_price = self.eth.eth_gasPrice()
        gas = self.eth.eth_estimateGas({"gasPrice": hex(gas_price), "value": hex(value)})
        
        tx = {
            'nonce': self.eth.eth_getTransactionCount(sender),
            'to': to,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
            'chainId': self.chainId
        }
        if not data==None: tx['data'] = data
        return tx
    
    def send_transaction(self, transaction, private_key):
        signed_tx = self.eth.web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.send_raw_transaction(signed_tx)
        return tx_hash

    def send_raw_transaction(self, signed_tx):
        try:
            data = {
              "jsonrpc": "2.0",
              "method": "eth_sendRawTransaction",
              "params": [str(signed_tx.raw_transaction.hex())],
              "id": 1
            }
            result = requests.post(self.rpc_url, json = data)
            return result.json()['result'] # expected block number
        except Exception as e:
            print(f"Error sending transaction: {e}")
            return None


