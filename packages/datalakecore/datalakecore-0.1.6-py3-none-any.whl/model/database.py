from model.data_user import DataUser

class Database:
    def __init__(self,
                 name: str = None,
                 current_user: DataUser = None
                 ) -> None:
        self.name = name
        self.current_user = current_user