from model.glue_connection import GlueConnection
from util.not_found_exception import NotFoundException
import util.client as client

class GlueConnectionRepository:

    def __init__(self) -> None:
        self.dynamodb = client.dynamo_client

    def get_by_id(self, obj: GlueConnection):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM glue_connection WHERE id=?",
           Parameters=[{"S": obj.id}]
        )
        lst = self.__read(resp)
        if len(lst) < 1:
            raise NotFoundException(f"Registro não encontrado na tabela glue_connection com id={obj.id}")
        return lst[0]
    
    def get_all(self):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM glue_connection"
        )
        return self.__read(resp)
    
    def __read(self, resp):
        lst = []
        for item in resp['Items']:
            lst.append(
                GlueConnection(
                    id=item["id"]["S"],
                    connection_type=item["connection_type"]["S"],
                    connection_name=item["connection_name"]["S"],
                    incremental_template=item["incremental_template"]["S"],
                    active=bool(item["active"]["BOOL"])
                )
            )
        return lst