from account import Account

seller_account = 0
buyer_account = 0

def main():

    print(f"seller_account: {seller_account.address}")
    print(f"buyer_account: {buyer_account.address}")

    eventID = 1
    uuid = "1234567890"

    seller_account.issue_ticket(eventID, uuid)
    buyer_account.issue_ticket(eventID, uuid)

def seller_sign_in(seed=0):
    if seed != 0:
        seller_account = Account(seed)
    else:
        seller_account = Account()

def buyer_sign_in(seed=0):
    if seed != 0:
        buyer_account = Account(seed)
    else:
        buyer_account = Account()
    return buyer_account

def get_ticket(seller_account, buyer_account, eventID, uuid):
    seller_account.issue_ticket(eventID, uuid)
    buyer_account.issue_ticket(eventID, uuid)

if __name__ == "__main__":
    main()