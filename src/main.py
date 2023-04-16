from account import Account

def main():
    # Create an account
    account = Account()
    print(f"Account address: {account.address}")
    print(f"Account balance: {account.get_balance()}")

    # Issue a ticket
    eventID = 1
    uuid = "1234567890"
    account.issue_ticket(eventID, uuid)

    # Get the NFTs
    account.get_nfts()

if __name__ == "__main__":
    main()