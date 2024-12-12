class TableRaw:
    def __init__(self,
                 id: str = None,
                 connection_id: str = None,
                 env: str = None,
                 table_name: str = None,
                 full_table_name: str = None,
                 raw_uri: str = None,
                 column_incremental: str = None,
                 columns_hash: str = None,
                 write_mode: str = None,
                 last_execution: str = None,
                 incremental_template: str = None,
                 active: bool = None,
                 status: str = None
                 ) -> None:
        self.id = id
        self.connection_id = connection_id
        self.env = env
        self.table_name = table_name
        self.full_table_name = full_table_name
        self.raw_uri = raw_uri
        self.column_incremental = column_incremental
        self.columns_hash = columns_hash
        self.write_mode = write_mode
        self.last_execution = last_execution
        self.incremental_template = incremental_template
        self.active = active
        self.status = status