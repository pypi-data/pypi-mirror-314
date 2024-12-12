class GlueConnection:
    def __init__(self,
                 id: str = None,
                 connection_type: str = None,
                 connection_name: str = None,
                 incremental_template: str = None,
                 active: bool = None
                 ) -> None:
        self.id = id
        self.connection_type = connection_type
        self.connection_name = connection_name
        self.incremental_template = incremental_template
        self.active = active