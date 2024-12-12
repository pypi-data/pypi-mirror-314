from model.data_user import DataUser
from model.data_access_request import DataAccessRequest
import boto3

class DataUserRepository:

    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.iam_client = boto3.client('iam')

    def save(self, obj: DataUser):
        self.dynamodb.put_item(
            TableName="data_user", 
            Item={
                "id": {"S": obj.id},
                "user_email": {"S": obj.user_email},
                "user_identifier": {"S": obj.user_identifier},
                "user_name": {"S": obj.user_name},
                "aws_user_name": {"S": obj.aws_user_name},
                "active": {"BOOL": obj.active}
            }
        )

        # Cria o usuário na AWS
        self.iam_client.create_user(
            UserName=obj.aws_user_name
        )

    def add_user_to_group(self, obj: DataUser):
        self.iam_client.add_user_to_group(
            GroupName=obj.group_name,
            UserName=obj.aws_user_name
        )

    def get_all(self):
        resp = self.dynamodb.execute_statement(
           Statement="select * from data_user"
        )
        return self.__read(resp)

    def get_by_id(self, obj: DataUser):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_user WHERE id=?",
           Parameters=[{"S": obj.id}]
        )
        lst = self.__read(resp)
        if len(lst) < 1: return None
        return lst[0]

    def get_by_user_identifier(self, obj: DataUser):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_user WHERE user_identifier=?",
           Parameters=[{"S": obj.user_identifier}]
        )
        lst = self.__read(resp)
        if len(lst) < 1: return None
        return lst[0]
    
    def get_by_user_email(self, obj: DataUser):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_user WHERE user_email=?",
           Parameters=[{"S": obj.user_email}]
        )
        lst = self.__read(resp)
        if len(lst) < 1: return None
        return lst[0]

    def update(self, obj: DataUser):
        self.dynamodb.execute_statement(
           Statement="UPDATE data_user set user_identifier=?, active=? WHERE id=? and user_email=?",
           Parameters=[
               {"S": obj.user_identifier},
               {"BOOL": obj.active},
               {"S": obj.id},
               {"S": obj.user_email}
            ]
        )
    
    def __read(self, resp):
        lst = []
        for item in resp['Items']:
            lst.append(
                DataUser(
                    id=item["id"]["S"],
                    user_email=item["user_email"]["S"],
                    user_identifier=item["user_identifier"]["S"],
                    user_name=item["user_name"]["S"],
                    aws_user_name=item["aws_user_name"]["S"],
                    aws_groups=self.__get_aws_groups(item["aws_user_name"]["S"]),
                    active=item["active"]["BOOL"]
                )
            )
        return lst
    
    def __get_aws_groups(self, aws_user_name):
        lst = []
        if aws_user_name != "":
            response = self.iam_client.list_groups_for_user(
                UserName=aws_user_name
            )
            for item in response["Groups"]:
                lst.append(item.get("GroupName"))
        return lst