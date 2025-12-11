import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    account = PersonalAccount(data["first_name"], data["last_name"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    accounts_data = [{"first_name": account.first_name, "last_name": account.last_name, "pesel":account.pesel, "balance": account.balance} for account in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.get_accounts_number()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.find_account(pesel)
    if account:
        account_data = {"first_name": account.first_name, "last_name": account.last_name, "pesel":account.pesel, "balance": account.balance}
        return jsonify(account_data), 200
    else:
        return jsonify({"message": "No account"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = PersonalAccount(data["first_name"], data["last_name"], data["pesel"])
    registry.update_account(pesel, account)
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    registry.remove_account(pesel)
    return jsonify({"message": "Account deleted"}), 200