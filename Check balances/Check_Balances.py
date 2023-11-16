from web3 import Web3
import requests

def get_balance(address, web3):
    try:
        balance_wei = web3.eth.getBalance(address)
        balance = web3.fromWei(balance_wei, 'ether')
        return balance
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_balance(network_name, address, node_url, threshold):
    web3 = Web3(Web3.HTTPProvider(node_url))
    
    if web3.isConnected():
        balance = get_balance(address, web3)
        if balance is not None:
            result = f"Balance for {network_name} address {address}: {balance} {network_name.upper()}"
            print(result)
            
            # Send to webhook only if balance is under the specified threshold
            if balance < threshold:
                result = f"Balance on {network_name} too low: {balance} {network_name.upper()}"
                send_to_webhook(result)
    else:
        print(f"Unable to connect to {network_name} network.")

def send_to_webhook(message):
    webhook_url = "YOUR_WEBHOOK_URL"  # Replace with your webhook url

    data = {"content": message}

    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending to webhook: {e}")

# Enter your node address and balance thresholds in the network definitions below
def main():
    networks = {
        'Ethereum': {'address': 'YOUR_NODE_ADDRESS', 'node_url': 'https://rpc.ankr.com/eth_goerli', 'threshold': 0.2},
        'Polygon': {'address': 'YOUR_NODE_ADDRESS', 'node_url': 'https://rpc.ankr.com/polygon_mumbai', 'threshold': 0.4},
        'Avalanche': {'address': 'YOUR_NODE_ADDRESS', 'node_url': 'https://avalanche-fuji-c-chain.publicnode.com', 'threshold': 1},
        'Cronos': {'address': 'YOUR_NODE_ADDRESS', 'node_url': 'https://evm-t3.cronos.org', 'threshold': 50},
        'Celo': {'address': 'YOUR_NODE_ADDRESS', 'node_url': 'https://alfajores-forno.celo-testnet.org', 'threshold': 1},
        'BSC': {'address': 'YOUR_NODE_ADDRESS', 'node_url': 'https://data-seed-prebsc-1-s1.binance.org:8545', 'threshold': 0.5},
        'Fantom': {'address': 'YOUR_NODE_ADDRESS', 'node_url': 'https://rpc.ankr.com/fantom_testnet', 'threshold': 5},
    }

    for network_name, details in networks.items():
        print(f"\nChecking balance for {network_name}...")
        check_balance(network_name, details['address'], details['node_url'], details['threshold'])

if __name__ == "__main__":
    main()
