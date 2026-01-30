from src.personal_account import PersonalAccount

class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        if isinstance(account, PersonalAccount):
            self.accounts.append(account)
            return True
        return False

    def find_account(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def clear_accounts(self):
        self.accounts = []

    def get_accounts(self):
        return self.accounts
    
    def get_accounts_number(self):
        return len(self.accounts)
    
    def remove_account(self, pesel):
        for index, account in enumerate(self.accounts):
            if account.pesel == pesel:
                del self.accounts[index]
                return True
        return False

    def update_account(self, pesel, new):
        if not isinstance(new, dict):
            return False

        for account in self.accounts:
            if account.pesel == pesel:
                account.first_name = new["first_name"] if "first_name" in new else account.first_name
                account.last_name = new["last_name"] if "last_name" in new else account.last_name
                return True

        return False
            