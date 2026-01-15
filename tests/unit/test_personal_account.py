from src.personal_account import PersonalAccount

import pytest
import datetime


@pytest.fixture
def account():
    return PersonalAccount("John", "Doe", "99039666673")

class TestPersonalAccount:

    @pytest.mark.parametrize(
        "balance, amount, expected",
        [
            (0.0, 10.0, 0.0),
            (20.0, -10.0, 20.0),
            (20.0, True, 20.0),
            (20.0, 10.0, 9.0),
        ]
    )
    def test_outgoing_express_transfer(self, account, balance, amount, expected):
        account.ingoing_transfer(balance)
        account.outgoing_express_transfer(amount)
        assert account.balance == expected

    @pytest.mark.parametrize(
        "history, amount, expected, expected_value",
        [
            ([30.0, 30.0, 30.0, 30.0, 30.0], 10.0, 10.0, True),
            ([10.0, 10.0, 10.0, 10.0, 10.0], -500.0, 0.0, False),
            ([130.0, 30.0, 30.0, -30.0, -30.0, -30.0], 10.0, 0.0, False),
            ([30.0], 10.0, 0.0, False)
        ]
    )
    def test_submit_for_loan(self, account, history, amount, expected, expected_value):
        account.history = history
        result = account.submit_for_loan(amount)
        assert result == expected_value
        assert account.balance == expected


    def test_personal_account_send_history_success(self, mocker):
        mock_send = mocker.patch("smtp.smtp.SMTPClient.send", return_value=True)

        account = PersonalAccount(
            first_name="Jan",
            last_name="Kowalski",
            pesel="01234567890",
            promotion_code="PROM_123"
        )

        account.history = [100.0, -50.0]

        result = account.send_history_via_email("test@mail.com")
        assert result is True

        mock_send.assert_called_once()
        subject, text, email = mock_send.call_args[0]

        assert "Account Transfer History" in subject
        assert "Personal account history" in text
        assert email == "test@mail.com"