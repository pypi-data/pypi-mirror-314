from model.database import Database

class Table:
    def __init__(self,
                 name: str = None,
                 database: Database = None,
                 arn_table: str = None,
                 current_user_has_access: bool = None,
                 current_user_last_request_status: str = None,
                 last_request_id: str = None
                 ) -> None:
        self.name = name
        self.database = database
        self.arn_table = arn_table
        self.current_user_has_access = current_user_has_access
        self.current_user_last_request_status = current_user_last_request_status
        self.last_request_id = last_request_id