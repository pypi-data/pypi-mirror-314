import requests
import json

class Client:
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url

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
        return response.json()['result']

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
        return self._send_request("eth_gasPrice")

    def eth_getTransactionCount(self, address):
        params = [address]
        return self._send_request("eth_getTransactionCount", params)

    def eth_sendRawTransaction(self, raw_transaction):
        return self._send_request("eth_sendRawTransaction", [raw_transaction])

    def net_version(self):
        return self._send_request("net_version")

    def eth_getTransactionReceipt(self, tx_index):
        return self._send_request("eth_getTransactionReceipt", [tx_index])

# Example Usage
if __name__ == "__main__":
    rpc = Client("https://xyl-testnet.glitch.me/rpc/")  # Replace with your actual RPC URL
    print(rpc.eth_chainId())

