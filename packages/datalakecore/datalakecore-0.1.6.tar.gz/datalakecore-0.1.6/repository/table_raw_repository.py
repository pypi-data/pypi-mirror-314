from model.table_raw import TableRaw
from util.not_found_exception import NotFoundException
import util.client as client

class TableRawRepository:

    def __init__(self) -> None:
        self.dynamodb = client.dynamo_client

    def get_by_id(self, obj: TableRaw):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM table_raw WHERE id=?",
           Parameters=[{"S": obj.id}]
        )
        lst = self.__read(resp)
        if len(lst) < 1:
            raise NotFoundException(f"Registro não encontrado na tabela table_raw com id={obj.id}")
        return lst[0]

    def get_all(self):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM table_raw"
        )
        return self.__read(resp)
    
    def __read(self, resp):
        lst = []
        for item in resp['Items']:
            lst.append(
                TableRaw(
                    id=item["id"]["S"],
                    connection_id=item["connection_id"]["S"],
                    env=item["env"]["S"],
                    table_name=item["table_name"]["S"],
                    full_table_name=item["full_table_name"]["S"],
                    raw_uri=item["raw_uri"]["S"],
                    column_incremental=item["column_incremental"]["S"],
                    columns_hash=item["columns_hash"]["S"],
                    write_mode=item["write_mode"]["S"],
                    last_execution=item["last_execution"]["S"],
                    incremental_template=item["incremental_template"]["S"],
                    active=bool(item["active"]["BOOL"]),
                    status=item["status"]["S"]
                )
            )
        return lst

    def check_ingestion_exists(self, obj: TableRaw):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM table_raw WHERE full_table_name=? and connection_id=? and id!=?",
           Parameters=[{"S": obj.full_table_name},
                       {"S": obj.connection_id},
                       {"S": obj.id}]
        )
        return True if len(resp['Items']) > 0 else False

    def save(self, obj: TableRaw):
        self.dynamodb.put_item(
            TableName="table_raw", 
            Item={
                "id": {"S": obj.id},
                "connection_id": {"S": obj.connection_id},
                "env": {"S": obj.env},
                "table_name": {"S": obj.table_name},
                "full_table_name": {"S": obj.full_table_name},
                "raw_uri": {"S": obj.raw_uri},
                "column_incremental": {"S": obj.column_incremental},
                "columns_hash": {"S": obj.columns_hash},
                "write_mode":  {"S": obj.write_mode},
                "last_execution": {"S": obj.last_execution},
                "incremental_template": {"S": obj.incremental_template},
                "active": {"BOOL": obj.active},
                "status": {"S": obj.status}
            }
        )

    def update(self, obj: TableRaw):
        self.dynamodb.execute_statement(
           Statement="UPDATE table_raw set status=? WHERE id=? and connection_id=?",
           Parameters=[
               {"S": obj.status},
               {"S": obj.id},
               {"S": obj.connection_id}
            ]
        )