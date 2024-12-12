from model.table_trusted import TableTrusted
from util.not_found_exception import NotFoundException

class TableTrustedRepository:

    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb

    def get_by_id(self, obj: TableTrusted):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM table_trusted WHERE id=?",
           Parameters=[{"S": obj.id}]
        )
        lst = self.__read(resp)
        if len(lst) < 1:
            raise NotFoundException(f"Registro não encontrado na tabela table_trusted com id={obj.id}")
        return lst[0]
    
    def get_all(self):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM table_trusted"
        )
        return self.__read(resp)

    def __read(self, resp):
        lst = []
        for item in resp['Items']:
            lst.append(
                TableTrusted(
                    id=item["id"]["S"],
                    status=item["status"]["S"],
                    env=item["env"]["S"],
                    table_name=item["table_name"]["S"],
                    raw_uri=item["raw_uri"]["S"],
                    trusted_uri=item["trusted_uri"]["S"],
                    column_incremental=item["column_incremental"]["S"],
                    write_mode=item["write_mode"]["S"],
                    last_execution=item["last_execution"]["S"],
                    columns_deduplication=item["columns_deduplication"]["S"],
                    order_deduplication=item["order_deduplication"]["S"],
                    active=bool(item["active"]["BOOL"])
                )
            )
        return lst

    def save(self, obj: TableTrusted):
        self.dynamodb.put_item(
            TableName="table_trusted", 
            Item={
                "id": {"S": obj.id},
                "status": {"S": obj.status},
                "env": {"S": obj.env},
                "table_name": {"S": obj.table_name},
                "raw_uri": {"S": obj.raw_uri},
                "trusted_uri": {"S": obj.trusted_uri},
                "column_incremental": {"S": obj.column_incremental},
                "write_mode": {"S": obj.write_mode},
                "last_execution": {"S": obj.last_execution},
                "columns_deduplication": {"S": obj.columns_deduplication},
                "order_deduplication": {"S": obj.order_deduplication},
                "active": {"BOOL": obj.active}
            }
        )