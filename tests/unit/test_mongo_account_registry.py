import pytest
from src.mongo_account_registry import MongoAccountsRepository
from src.personal_account import PersonalAccount

@pytest.fixture
def sample_accounts():
    return [
        PersonalAccount("Jan", "Kowalski", "12345678901"),
        PersonalAccount("Anna", "Nowak", "98765432109")
    ]

@pytest.fixture
def repo(mocker):
    repo = MongoAccountsRepository()
    repo.collection = mocker.Mock()
    return repo

class TestMongoAccountsRepository:

    def test_save_all_calls_delete_and_update(self, repo, sample_accounts):
        repo.save_all(sample_accounts)

        repo.collection.delete_many.assert_called_once_with({})
        assert repo.collection.update_one.call_count == len(sample_accounts)

    def test_load_all_returns_data_from_mongo(self, repo, sample_accounts):
        repo.collection.find.return_value = [acc.to_dict() for acc in sample_accounts]

        result = repo.load_all()

        repo.collection.find.assert_called_once_with({}, {"_id": 0})
        assert result == [acc.to_dict() for acc in sample_accounts]

    def test_save_and_load_empty_list(self, repo):
        repo.save_all([])
        repo.collection.delete_many.assert_called_once_with({})
        assert repo.collection.update_one.call_count == 0

        repo.collection.find.return_value = []
        result = repo.load_all()
        assert result == []
