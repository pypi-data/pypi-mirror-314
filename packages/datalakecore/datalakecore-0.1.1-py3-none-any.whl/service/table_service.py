from model.database import Database
from repository.table_repository import TableRepository

from util.inconsistence_exception import InconsistenceException

class TableService:

    def __init__(self, glue_client, dynamo_client) -> None:
        self.tableRepository = TableRepository(glue_client, dynamo_client)

    def get_by_database_name(self, obj: Database):

        if obj.name is None or len(obj.name) < 0:
            raise InconsistenceException("O atributo name deve ser informado!")

        return self.tableRepository.get_by_database_name(obj)