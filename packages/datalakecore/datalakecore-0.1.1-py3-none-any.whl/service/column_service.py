from model.table import Table
from repository.column_repository import ColumnRepository

from util.inconsistence_exception import InconsistenceException

class ColumnService:

    def __init__(self, client) -> None:
        self.client = client
        self.columnRepository = ColumnRepository(self.client)

    def get_by_table_name(self, obj: Table):

        if obj.database is None or obj.database.name is None or len(obj.database.name) < 0:
            raise InconsistenceException("O atributo database_name deve ser informado!")
        
        if obj.name is None or len(obj.name) < 0:
            raise InconsistenceException("O atributo table_name deve ser informado!")

        return self.columnRepository.get_by_table_name(obj)