from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.models.transactions.nftoken_mint import NFTokenMint, NFTokenMintFlag
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests import AccountNFTs

from xrpl.clients import JsonRpcClient # Define the network client
import xrpl.wallet # Fetch Wallet

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

def main():
    pass

def get_wallet(seed):
    # seed = "" # NEED TO FETCH the issuer account seed here
    # generate seed from public and private keys
    # but for testing, create a NEW wallet:
    issuer_wallet = xrpl.wallet.generate_faucet_wallet(client=client)
    return issuer_wallet

def get_account_info(issuerAddr):
    # Look up info about your account
    from xrpl.models.requests.account_info import AccountInfo

    acct_info = AccountInfo(
        account=issuerAddr,
        ledger_index="validated",
        strict=True,
    )

    response = client.request(acct_info)
    result = response.result
    print("response.status: ", response.status)
    import json
    print(json.dumps(response.result, indent=4, sort_keys=True)) # what do I wanna do with this?

def issue_ticket():
    # Construct NFTokenMint transaction to mint 1 NFT
    print(f"Minting a NFT...")
    mint_tx = NFTokenMint(
        account=issuerAddr,
        nftoken_taxon=1,
        flags=NFTokenMintFlag.TF_TRANSFERABLE
    )
    # Sign mint_tx using the issuer account
    mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=issuer_wallet, client=client)
    mint_tx_signed = send_reliable_submission(transaction=mint_tx_signed, client=client)
    mint_tx_result = mint_tx_signed.result

    print(f"\n  Mint tx result: {mint_tx_result['meta']['TransactionResult']}")
    print(f"     Tx response: {mint_tx_result}")




for node in mint_tx_result['meta']['AffectedNodes']:
    if "CreatedNode" in list(node.keys())[0]:
        print(f"\n - NFT metadata:"
              f"\n        NFT ID: {node['CreatedNode']['NewFields']['NFTokens'][0]['NFToken']['NFTokenID']}"
              f"\n  Raw metadata: {node}")

# Query the minted account for its NFTs
get_account_nfts = client.request(
    AccountNFTs(account=issuerAddr)
)

nft_int = 1
print(f"\n - NFTs owned by {issuerAddr}:")
for nft in get_account_nfts.result['account_nfts']:
    print(f"\n{nft_int}. NFToken metadata:"
          f"\n    Issuer: {nft['Issuer']}"
          f"\n    NFT ID: {nft['NFTokenID']}"
          f"\n NFT Taxon: {nft['NFTokenTaxon']}")
    nft_int += 1