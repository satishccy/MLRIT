from algosdk import transaction, account,util
from algosdk.v2client import algod
import os
from dotenv import load_dotenv
load_dotenv()


private_key = os.getenv("PRIVATE_KEY")
address = account.address_from_private_key(private_key)
print("Address:",address)

algod_token = os.getenv("TESTNET_ALGOD_TOKEN")
algod_url = os.getenv("TESTNET_ALGOD_URL")
algod_port = os.getenv("TESTNET_ALGOD_PORT")

algod_client = algod.AlgodClient(algod_token, algod_url)

suggested_params = algod_client.suggested_params()

payTxn = transaction.PaymentTxn(sender=address, sp=suggested_params, amt=util.algos_to_microalgos(0.673),
                                receiver="C6CUESFPGPVEUXASHAKTGTTQTFFQO6VGAZGQY3KOQSLFNGRWB76XYWAWG4", note="From Python Code")

signedTxn = payTxn.sign(private_key=private_key)

txid = algod_client.send_transaction(signedTxn)

print(f"Txn sent : https://app.dappflow.org/explorer/transaction/{txid}")

result = transaction.wait_for_confirmation(algod_client,txid,4)

print(f"Txn Confirmed in round {result['confirmed-round']}")