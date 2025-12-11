from src.personal_account import PersonalAccount

class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        if isinstance(account, PersonalAccount):
            self.accounts.append(account)
        return self.accounts

    def find_account(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_accounts(self):
        return self.accounts
    
    def get_accounts_number(self):
        return len(self.accounts)
    
    def remove_account(self, pesel):
        self.accounts = [account for account in self.accounts if account.pesel != pesel]
        return self.accounts
    
    def update_account(self, pesel, new):
        if isinstance(new, PersonalAccount):
            for index in range(len(self.accounts)):
                if self.accounts[index].pesel == pesel:
                    self.accounts[index] = new
        return self.accounts
            