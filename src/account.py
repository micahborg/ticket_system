"""
    An original implementation of an account class for the NFTicket project.
    Created by Micah Borghese on 4/15/2023
"""

from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.models.transactions.nftoken_mint import NFTokenMint, NFTokenMintFlag
from xrpl.models.requests import AccountNFTs
import xrpl.wallet

from xrpl.clients import JsonRpcClient # Define the network client

def main():
    my_account = Account()
    print("Hi")
    print(my_account.account_info())
    print(my_account.get_balance())

class Account:
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(JSON_RPC_URL)

    def __init__(self, seed=None):
        if seed != None:
            self.issuer_wallet = xrpl.wallet.Wallet(seed=seed)
        else:
            self.issuer_wallet = xrpl.wallet.generate_faucet_wallet(client=self.client)
        self.issuer_address = self.issuer_wallet.classic_address

    def account_info(self):
        # Look up info about your account
        from xrpl.models.requests.account_info import AccountInfo

        acct_info = AccountInfo(
            account=self.issuer_address,
            ledger_index="validated",
            strict=True,
        )

        response = self.client.request(acct_info)
        result = response.result
        print("response.status: ", response.status)
        return result
    
    def get_balance(self):
        result = self.account_info()
        return result['account_data']['Balance']
    
    def issue_ticket(self):
        # Construct NFTokenMint transaction to mint 1 NFT
        print(f"Minting a NFT...")
        mint_tx = NFTokenMint(
            account=self.issuer_address,
            nftoken_taxon=1,
            flags=NFTokenMintFlag.TF_TRANSFERABLE
        )
        # Sign mint_tx using the issuer account
        mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=self.issuer_wallet, client=client)
        mint_tx_signed = send_reliable_submission(transaction=mint_tx_signed, client=self.client)
        mint_tx_result = mint_tx_signed.result

        print(f"\n  Mint tx result: {mint_tx_result['meta']['TransactionResult']}")
        print(f"     Tx response: {mint_tx_result}")
        return mint_tx_result
    
    def get_account_nfts(self):
        # Query the minted account for its NFTs
        get_account_nfts = self.client.request(
            AccountNFTs(account=issuer_address)
        )

        nft_int = 1
        print(f"\n - NFTs owned by {self.issuer_address}:")
        for nft in get_account_nfts.result['account_nfts']:
            print(f"\n{nft_int}. NFToken metadata:"
                f"\n    Issuer: {nft['Issuer']}"
                f"\n    NFT ID: {nft['NFTokenID']}"
                f"\n NFT Taxon: {nft['NFTokenTaxon']}")
            nft_int += 1
    

if __name__ == "__main__":
    main()