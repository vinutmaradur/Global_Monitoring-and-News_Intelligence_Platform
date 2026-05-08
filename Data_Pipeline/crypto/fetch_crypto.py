import requests
from Data_Pipeline.utils import save_json

def fetch_crypto():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    data = requests.get(url).json()

    save_json(data, "data\\raw\\crypto.json")
    print("Crypto saved!")

if __name__ == "__main__":
    fetch_crypto()