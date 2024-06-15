from algosdk import transaction, account,encoding
from algosdk.v2client import algod
import os
from dotenv import load_dotenv
load_dotenv()


private_key = os.getenv("PRIVATE_KEY")
address = account.address_from_private_key(private_key)
print("Address:", address)

algod_token = os.getenv("TESTNET_ALGOD_TOKEN")
algod_url = os.getenv("TESTNET_ALGOD_URL")

algod_client = algod.AlgodClient(algod_token, algod_url)

suggested_params = algod_client.suggested_params()

total = 100
decimals = 4

total_supply = total * 10**decimals

tokenCreateTxn = transaction.AssetCreateTxn(sender=address, sp=suggested_params, total=total_supply, decimals=decimals, default_frozen=False,
                                            asset_name="MLRIT Token", unit_name="MLRIT", manager=address, reserve=address, clawback=address, freeze=address)


signedTxn = tokenCreateTxn.sign(private_key=private_key)

txid = algod_client.send_transaction(signedTxn)

print(f"Token Create Txn sent : https://app.dappflow.org/explorer/transaction/{txid}")

result = transaction.wait_for_confirmation(algod_client, txid, 4)

asset_id = result['asset-index']

print(f"Token Create Txn Confirmed in round {result['confirmed-round']} with asset id {asset_id} [https://app.dappflow.org/explorer/asset/{asset_id}/transactions]")

