from model.data_user import DataUser
from datetime import datetime

class DataAccessRequest:
    def __init__(self,
                 id: str = None,
                 data_user_request: DataUser = None,
                 dh_request: datetime = None,
                 database: str = None,
                 table_name: str = None,
                 arn_table: str = None,
                 request_description: str = None,
                 level_request: str = None,
                 group_name: str = None,
                 data_user_response: DataUser = None,
                 dh_response: datetime = None,
                 response_description: str = None,
                 level_response: str = None,
                 status: str = None,
                 token: str = None,
                 token_valid: bool = None,
                 dh_last_updated: datetime = None
                 ) -> None:
        self.id = id
        self.data_user_request = data_user_request
        self.dh_request = dh_request
        self.database = database
        self.table_name = table_name
        self.arn_table = arn_table
        self.request_description = request_description
        self.level_request = level_request
        self.group_name = group_name
        self.data_user_response = data_user_response
        self.dh_response = dh_response
        self.response_description = response_description
        self.level_response = level_response
        self.status = status
        self.token = token
        self.token_valid = token_valid
        self.dh_last_updated = dh_last_updated