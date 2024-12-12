from repository.database_repository import DatabaseRepository

class DatabaseService:

    def __init__(self, client) -> None:
        self.client = client
        self.databaseRepository = DatabaseRepository(self.client)

    def get_all(self):
        return self.databaseRepository.get_all()