class DataDomain:
    def __init__(self,
                 id: str = None,
                 domain_name: str = None,
                 domain_description: str = None,
                 bussines_owner: str = None
                 ) -> None:
        self.id = id
        self.domain_name = domain_name
        self.domain_description = domain_description
        self.bussines_owner = bussines_owner