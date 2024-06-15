from algosdk import transaction, account, encoding
from algosdk.v2client import algod
import os
import hashlib
import json
import requests
from dotenv import load_dotenv
load_dotenv()

PINATA_KEY = os.getenv("PINATA_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")


def sha256_hash_file(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def pin_json(json_):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    res = dict()
    res['pinataContent'] = json_
    payload = json.dumps(res)
    headers = {
        'Content-Type': 'application/json',
        'pinata_api_key': PINATA_KEY,
        'pinata_secret_api_key': PINATA_SECRET_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def pin_image(filepath, image_name):

    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    payload = {'pinataOptions': '{"cidVersion": 1}',
               'pinataMetadata': '{"name":"'+image_name+'", "keyvalues": {"company": "Pinata"}}'}

    files = [
        ('file', (image_name, open(filepath, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'pinata_api_key': PINATA_KEY,
        'pinata_secret_api_key': PINATA_SECRET_KEY
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    return json.loads(response.text)


def create_digest(json_):
    # Convert the metadata to a JSON string
    metadata_json = json.dumps(json_)

    # Compute the SHA-256 digest
    hash_object = hashlib.sha256(metadata_json.encode("utf-8"))
    digest = hash_object.digest()

    # Print the digest as a hexadecimal string
    return digest.hex()


private_key = os.getenv("PRIVATE_KEY")
address = account.address_from_private_key(private_key)
print("Address:", address)

algod_token = os.getenv("TESTNET_ALGOD_TOKEN")
algod_url = os.getenv("TESTNET_ALGOD_URL")

algod_client = algod.AlgodClient(algod_token, algod_url)

suggested_params = algod_client.suggested_params()

total = 1
decimals = 0

total_supply = total * 10**decimals

img_name = 'moon.jpg'
res = pin_image("./images/"+img_name, img_name)
image_integrity = sha256_hash_file("./images/"+img_name)
image_mimetype = img_name.split(".")[-1]
print(res)

if (res['IpfsHash']):
    metadata = dict()
    metadata['name'] = 'Moon'
    metadata['description'] = "Algorand on Moon"
    metadata['image'] = "ipfs://{}#arc3".format(res['IpfsHash'])
    metadata['image_integrity'] = "sha256-{}".format(image_integrity)
    metadata['image_mimetype'] = "image/{}".format(image_mimetype)
    metadata['properties'] = dict()
    metadata['properties']['Sample Key'] = "Sample Value"
    jsres = pin_json(metadata)
    if (jsres['IpfsHash']):
        digest = create_digest(metadata)
        nft_mint = transaction.AssetCreateTxn(address, suggested_params, total_supply, decimals, False, unit_name="MOONS",
                                              asset_name="ALGO-MOON", url="ipfs://"+jsres['IpfsHash']+"#arc3", metadata_hash=bytes.fromhex(digest), manager=address, freeze=address, clawback=address, reserve=address)
        signed_nft_mint = nft_mint.sign(private_key)
        txid = algod_client.send_transaction(signed_nft_mint)
        results = transaction.wait_for_confirmation(algod_client, txid, 4)

        created_asset = results["asset-index"]

        print(
            f"NFT Create Txn sent : https://app.dappflow.org/explorer/transaction/{txid}")

        result = transaction.wait_for_confirmation(algod_client, txid, 4)

        asset_id = result['asset-index']

        print(f"NFT Create Txn Confirmed in round {result['confirmed-round']} with asset id {asset_id} [https://app.dappflow.org/explorer/asset/{asset_id}/transactions]")
