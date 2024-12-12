from model.data_domain import DataDomain
from model.data_user import DataUser
from datetime import datetime

class TableAnalytics:
    def __init__(self,
                 id: str = None,
                 data_domain: DataDomain = None,
                 data_user: DataUser = None,
                 env: str = None,
                 query: str = None,
                 name: str = None,
                 last_execution: datetime = None,
                 active: bool = None
                 ) -> None:
        self.id = id
        self.data_domain = data_domain
        self.data_user = data_user
        self.env = env
        self.query = query
        self.name = name
        self.last_execution = last_execution
        self.active = active