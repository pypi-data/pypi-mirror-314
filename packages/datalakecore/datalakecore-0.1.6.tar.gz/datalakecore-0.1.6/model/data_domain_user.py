class DataDomainUser:
    def __init__(self,
                 data_domain_id: str = None,
                 data_user_id: str = None
                 ) -> None:
        self.data_domain_id = data_domain_id
        self.data_user_id = data_user_id