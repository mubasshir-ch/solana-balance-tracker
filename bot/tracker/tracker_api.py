import json
import requests

class TrackerAPI:
    def __init__(self, walletAddress, tokenMintAddress):
        self.walletAddress =  walletAddress
        self.tokenMintAddress = tokenMintAddress

    def get_balance(self):
        # Define the URL
        url = "https://api.mainnet-beta.solana.com"

        # Define the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Define the payload
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                self.walletAddress,
                {
                    "mint": self.tokenMintAddress,
                },
                {
                    "encoding": "jsonParsed",
                },
            ],
        }

        # Send POST request
        response = requests.post(url, headers=headers, json=data)

        # Check if the request was successful
        if response.ok:
            try:
                # Get the balance
                print(json.dumps(response.json(), indent=4))
                balance = response.json()["result"]["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
                return balance
            except Exception as e:
                raise Exception(f"Failed to get balance: {e}")
        else:
            raise Exception(f"Failed to get balance: {response.status_code} - {response.reason}")
