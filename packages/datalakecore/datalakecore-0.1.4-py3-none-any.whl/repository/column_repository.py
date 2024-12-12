from model.table import Table
from model.column import Column

import util.client as client

class ColumnRepository:

    def __init__(self) -> None:
        self.glue_client = client.glue_client

    def get_by_table_name(self, obj: Table):
        response = self.glue_client.get_table(
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