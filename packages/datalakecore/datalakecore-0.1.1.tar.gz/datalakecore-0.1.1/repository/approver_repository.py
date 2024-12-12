from model.data_user import DataUser
from repository.data_user_repository import DataUserRepository

class ApproverRepository:

    def __init__(self, client) -> None:
        self.dynamodb = client
        self.dataUserRepository =  DataUserRepository(client)

    def get_approver(self, layer, sufix):
        id = self.__get_approver_id(layer, sufix)
        usr= self.dataUserRepository.get_by_id(
            DataUser(id=id)
        )
        return usr

    def __get_approver_id(self, layer, sufix):
        if layer.upper() == "TRUSTED":
            resp = self.dynamodb.execute_statement(
                Statement="select * from glue_connection where connection_name=?",
                Parameters=[{"S": sufix}]
            )
        else:
            resp = self.dynamodb.execute_statement(
                Statement="SELECT * FROM data_domain WHERE domain_name=?",
                Parameters=[{"S": sufix}]
            )
        return resp['Items'][0]["approver_user_id"]["S"]