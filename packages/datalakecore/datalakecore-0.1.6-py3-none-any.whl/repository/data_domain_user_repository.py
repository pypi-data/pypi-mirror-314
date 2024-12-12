from model.data_domain_user import DataDomainUser
import util.client as client

class DataDomainUserRepository:
    
    def __init__(self) -> None:
        self.dynamodb = client.dynamo_client

    def get_by_data_user_id(self, obj: DataDomainUser):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_domain_user WHERE data_user_id=?",
           Parameters=[{"S": obj.data_user_id}]
        )
        lst = []
        for item in resp['Items']:
            lst.append(
                DataDomainUser(
                    data_user_id=item["data_user_id"]["S"],
                    data_domain_id=item["data_domain_id"]["S"]
                )
            )
        return lst