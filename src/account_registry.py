from src.personalaccount import PersonalAccount

class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        if isinstance(account, PersonalAccount):
            self.accounts.append(account)

    def find_account(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_accounts(self):
        return self.accounts
    
    def get_accounts_number(self):
        return len(self.accounts)