from model.table import Table
from model.column import Column

class ColumnRepository:

    def __init__(self, client) -> None:
        self.client = client

    def get_by_table_name(self, obj: Table):
        response = self.client.get_table(
            DatabaseName=obj.database.name,
            Name=obj.name
        )
        lst = []
        for item in response["Table"]["StorageDescriptor"]["Columns"]:
            lst.append(
                Column(
                    name=item["Name"],
                    type=item["Type"]
                )
            )
        return lst