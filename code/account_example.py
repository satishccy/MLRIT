from algosdk import account, encoding, mnemonic
import os
from dotenv import load_dotenv
load_dotenv()

# generate an account
private_key, address = account.generate_account()

print("Private key:", private_key)
print("Address:", address)


mnemon = mnemonic.from_private_key(private_key)
print("Mnemonic:",mnemon)

derived_private_key = mnemonic.to_private_key(mnemon)
print("Private Key Derived from mnemonic:",derived_private_key)

print("Comparision Between two Private Keys:",private_key==derived_private_key)

env_private = os.getenv("PRIVATE_KEY")
print("Private Key From .env:",env_private)

print(mnemonic.from_private_key(env_private))

# check if the address is valid
if encoding.is_valid_address(address):
    print("The address is valid!")
else:
    print("The address is invalid.")