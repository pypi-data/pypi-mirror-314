from repository.database_repository import DatabaseRepository

class DatabaseService:

    def __init__(self) -> None:
        self.databaseRepository = DatabaseRepository()

    def get_all(self):
        return self.databaseRepository.get_all()