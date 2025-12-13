from flask import Flask, request, jsonify

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    required_fields = {"first_name", "last_name", "pesel"}
    if not required_fields.issubset(data):
        return jsonify({"message": "Missing required fields"}), 400

    if registry.find_account(data["pesel"]):
        return jsonify({"message": "Account already exists"}), 409

    account = PersonalAccount(
        data["first_name"],
        data["last_name"],
        data["pesel"]
    )

    if not registry.add_account(account):
        return jsonify({"message": "Invalid account data"}), 400

    return jsonify({"message": "Account created"}), 201


@app.route("/api/accounts", methods=["GET"])
def get_all_accounts():
    accounts = registry.get_accounts()
    return jsonify([
        {
            "first_name": acc.first_name,
            "last_name": acc.last_name,
            "pesel": acc.pesel,
            "balance": acc.balance
        }
        for acc in accounts
    ]), 200


@app.route("/api/accounts/count", methods=["GET"])
def get_account_count():
    return jsonify({"count": registry.get_accounts_number()}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def get_account_by_pesel(pesel):
    account = registry.find_account(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404

    return jsonify({
        "first_name": account.first_name,
        "last_name": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    account = PersonalAccount(
        data.get("first_name"),
        data.get("last_name"),
        pesel
    )

    if not registry.update_account(pesel, account):
        return jsonify({"message": "Account not found"}), 404

    return jsonify({"message": "Account updated"}), 200


@app.route("/api/accounts/<pesel>", methods=["DELETE"])
def delete_account(pesel):
    if not registry.remove_account(pesel):
        return jsonify({"message": "Account not found"}), 404

    return jsonify({"message": "Account deleted"}), 200