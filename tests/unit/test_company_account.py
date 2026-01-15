from src.company_account import CompanyAccount

import pytest


@pytest.fixture
def account(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}

    mocker.patch("requests.get", return_value=mock_response)

    return CompanyAccount("SupCompany", "1021010102")


class TestCompanyAccount:

    @pytest.mark.parametrize(
        "balance, amount, expected",
        [
            (0.0, 10.0, 0.0),
            (20.0, -10.0, 20.0),
            (20.0, True, 20.0),
            (20.0, 10.0, 5.0),
        ]
    )
    def test_outgoing_express_transfer(self, account, balance, amount, expected):
        account.ingoing_transfer(balance)
        account.outgoing_express_transfer(amount)
        assert account.balance == expected


    @pytest.mark.parametrize(
        "history, balance, amount, expected, expected_value",
        [
            ([10.0, -1775.0, 10.0], 20.0, 10.0, 30.0, True),
            ([10.0, 10.0, 10.0], 20.0, 10.0, 20.0, False),
            ([10.0, -1775.0, 10.0], 20.0, 15.0, 20.0, False),
            ([10.0, -1775.0, 10.0], 20.0, True, 20.0, False),
            ([10.0, -1775.0, 10.0], 20.0, -10.0, 20.0, False)
        ]
    )
    def test_take_loan(self, account, balance, history, amount, expected, expected_value):
        account.history = history
        account.balance = balance
        result = account.take_loan(amount)
        assert result == expected_value
        assert account.balance == expected


    def test_company_account_send_history_success(self, mocker):
        mock_nip = mocker.patch("src.company_account.CompanyAccount.is_nip_valid", return_value=True)
        mock_exists = mocker.patch("src.company_account.CompanyAccount.does_nip_exist", return_value=True)

        mock_send = mocker.patch("smtp.smtp.SMTPClient.send", return_value=True)

        account = CompanyAccount(name="Firma Sp. z o.o.", nip="1234567890")
        account.history = [1000.0, -200.0]

        result = account.send_history_via_email("firma@mail.com")

        assert result is True
        mock_send.assert_called_once()
        mock_nip.assert_called_once_with("1234567890")
        mock_exists.assert_called_once_with("1234567890")


    def test_does_nip_exist_api_error(self, mocker):
        from src.company_account import CompanyAccount
        import requests

        account = CompanyAccount.__new__(CompanyAccount)

        mocker.patch("src.company_account.requests.get", side_effect=requests.RequestException("API failure"))

        result = account.does_nip_exist("1234567890")

        assert result is False





