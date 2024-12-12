from model.data_domain import DataDomain
from util.not_found_exception import NotFoundException
import util.client as client

class DataDomainRepository:

    def __init__(self) -> None:
        self.dynamodb = client.dynamo_client

    def get_all(self):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_domain"
        )
        return self.__read(resp)

    def get_by_id(self, obj: DataDomain):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_domain WHERE id=?",
           Parameters=[{"S": obj.id}]
        )
        lst = self.__read(resp)
        if len(lst) < 1:
            raise NotFoundException(f"Registro não encontrado na tabela data_domain com id={obj.id}")
        return lst[0]
    
    def __read(self, resp):
        lst = []
        for item in resp['Items']:
            lst.append(
                DataDomain(
                    id=item["id"]["S"],
                    domain_name=item["domain_name"]["S"],
                    domain_description=item["domain_description"]["S"],
                    bussines_owner=item["bussines_owner"]["S"]
                )
            )
        return lst