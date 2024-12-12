from model.data_access_request import DataAccessRequest
from model.data_user import DataUser

from repository.data_user_repository import DataUserRepository

from datetime import datetime

class DataAccessRequestRepository:

    def __init__(self, client) -> None:
        self.dynamodb = client
        self.dataUserRepository = DataUserRepository(client)

    def save(self, obj: DataAccessRequest):
        self.dynamodb.put_item(
            TableName="data_access_request", 
            Item={
                "id": {"S": obj.id},
                "data_user_id_request": {"S": obj.data_user_request.id},
                "dh_request": {"S": obj.dh_request.strftime("%Y-%m-%d %H:%M:%S")},
                "database": {"S": obj.database},
                "table_name": {"S": obj.table_name},
                "arn_table": {"S": obj.arn_table},
                "request_description": {"S": obj.request_description},
                "level_request": {"S": obj.level_request},
                "group_name": {"S": obj.group_name},
                "data_user_id_response": {"S": obj.data_user_response.id},
                "dh_response": {"S": obj.dh_response.strftime("%Y-%m-%d %H:%M:%S") if obj.dh_response is not None else ""},
                "response_description": {"S": obj.response_description},
                "level_response": {"S": obj.level_response},
                "status": {"S": obj.status},
                "token": {"S": obj.token},
                "token_valid": {"BOOL": obj.token_valid},
                "dh_last_updated":{"S": obj.dh_last_updated.strftime("%Y-%m-%d %H:%M:%S")}
            }
        )

    def get_by_id(self, obj: DataAccessRequest):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_access_request WHERE id=?",
           Parameters=[{"S": obj.id}]
        )
        lst = self.__read(resp)
        if len(lst) < 1: return None
        return lst[0]
    
    def get_by_approved_groups(self, obj: DataAccessRequest):
        resp = self.dynamodb.execute_statement(
           Statement="""SELECT *
                          FROM data_access_request
                         WHERE level_response = 'GROUP'
                           AND status = 'APPROVED'
                           AND group_name=?
                     """,
           Parameters=[{"S": obj.group_name}]
        )
        return self.__read(resp)
    
    def get_by_token(self, obj: DataAccessRequest):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_access_request WHERE token=?",
           Parameters=[{"S": obj.token}]
        )
        lst = self.__read(resp)
        if len(lst) < 1: return None
        return lst[0]
    
    def get_by_data_user_id_request(self, obj: DataAccessRequest):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM data_access_request WHERE data_user_id_request=?",
           Parameters=[{"S": obj.data_user_request.id}]
        )
        return self.__read(resp)
    
    def check_exists_request_awaiting_approval_for_user(self, obj: DataAccessRequest):
        resp = self.dynamodb.execute_statement(
           Statement="""
                        SELECT *
                          FROM data_access_request
                         WHERE data_user_id_request=?
                           AND status = 'AWAITING APPROVAL'
                           AND database=?
                           AND table_name=?
                     """,
           Parameters=[
               {"S": obj.data_user_request.id},
               {"S": obj.database},
               {"S": obj.table_name}
            ]
        )
        return True if len(resp['Items']) > 0 else False
    
    def __read(self, resp):
        lst = []
        for item in resp['Items']:
            data_user_request = self.dataUserRepository.get_by_id(
                DataUser(id=item["data_user_id_request"]["S"])
            )
            data_user_response = self.dataUserRepository.get_by_id(
                DataUser(id=item["data_user_id_response"]["S"])
            )
            lst.append(
                DataAccessRequest(
                    id=item["id"]["S"],
                    data_user_request=data_user_request,
                    dh_request=datetime.strptime(item["dh_request"]["S"], "%Y-%m-%d %H:%M:%S") if len(item["dh_request"]["S"]) > 0 else None,
                    database=item["database"]["S"],
                    table_name=item["table_name"]["S"],
                    arn_table=item["arn_table"]["S"],
                    request_description=item["request_description"]["S"],
                    level_request=item["level_request"]["S"],
                    group_name=item["group_name"]["S"],
                    data_user_response=data_user_response,
                    dh_response=datetime.strptime(item["dh_response"]["S"], "%Y-%m-%d %H:%M:%S") if len(item["dh_response"]["S"]) > 0 else None,
                    response_description=item["response_description"]["S"],
                    level_response=item["level_response"]["S"],
                    status=item["status"]["S"],
                    token=item["token"]["S"],
                    token_valid=bool(item["token_valid"]["BOOL"]),
                    dh_last_updated=datetime.strptime(item["dh_last_updated"]["S"], "%Y-%m-%d %H:%M:%S") if len(item["dh_last_updated"]["S"]) > 0 else None
                )
            )
        return lst