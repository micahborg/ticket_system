"""
    A class implementation of a wallet account for the NFTicket project.
    Created by Micah Borghese on 4/15/2023
"""

from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.models.transactions.nftoken_mint import NFTokenMint
from xrpl.models.transactions.nftoken_create_offer import NFTokenCreateOffer
from xrpl.models.requests import AccountNFTs
from xrpl.models.requests.account_info import AccountInfo
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.utils import str_to_hex

from xrpl.clients import JsonRpcClient # Define the network client

class Account:
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(JSON_RPC_URL)

    def __init__(self, seed=0):
        if seed != 0:
            self.wallet = Wallet(seed=seed, sequence=1)
        else:
            self.wallet = generate_faucet_wallet(client=self.client)
        self.address = self.wallet.classic_address
        self.seed = self.wallet.seed

    def account_info(self):
        # Look up info about your account
        acct_info = AccountInfo(
            account=self.address,
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

    def get_nfts(self):
        # Query the minted account for its NFTs
        get_account_nfts = self.client.request(
            AccountNFTs(account=self.address)
        )

        # nft_int = 1                                             # parse the nft
        # print(f"\n - NFTs owned by {self.issuer_address}:")
        # for nft in get_account_nfts.result['account_nfts']:
        #     print(f"\n{nft_int}. NFToken metadata:"
        #         f"\n    Issuer: {nft['Issuer']}"
        #         f"\n    NFT ID: {nft['NFTokenID']}"
        #         f"\n NFT Taxon: {nft['NFTokenTaxon']}"
        #         f"\n       URI: {nft['URI']}")
        #     nft_int += 1
        return get_account_nfts.result['account_nfts']
    
class Buyer_Account(Account):
    def __init__(self, seed=0):
        super().__init__(seed)
        self.is_seller = False

class Seller_Account(Account):
    def __init__(self, seed=0):
        super().__init__(seed)
        self.is_seller = True
    
    def issue_ticket(self, eventID: int, uuid: str):
        # Construct NFTokenMint transaction to mint 1 NFT
        print(f"Minting a NFT...")
        mint_tx = NFTokenMint(
            account=self.address,
            nftoken_taxon=eventID,
            uri=str_to_hex(uuid),
        )
        # Sign mint_tx using the issuer account
        mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=self.wallet, client=self.client)
        mint_tx_signed = send_reliable_submission(transaction=mint_tx_signed, client=self.client)
        mint_tx_result = mint_tx_signed.result

        print(f"\n  Mint tx result: {mint_tx_result['meta']['TransactionResult']}")
        print(f"     Tx response: {mint_tx_result}")
        return mint_tx_result

    def sell_ticket(self, price, eventID: int, uuid: str, buyer_account: Buyer_Account):
        issue_ticket = self.issue_ticket(eventID, uuid)

        
        buy_tx = NFTokenCreateOffer(
            account=buyer_account,
            owner=self.address,
            nftoken_id=issue_ticket['meta']['TransactionResult'],
            amount=price,
        )

        buy_tx_signed = safe_sign_and_autofill_transaction(transaction=buy_tx, wallet=Wallet(buyer_account.seed, sequence=1), client=self.client)
        buy_tx_signed = send_reliable_submission(transaction=buy_tx_signed, client=self.client)
        buy_tx_result = buy_tx_signed.result
        return buy_tx_result