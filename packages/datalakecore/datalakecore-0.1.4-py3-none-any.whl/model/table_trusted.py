class TableTrusted:
    def __init__(self,
                 id: str = None,
                 status: str = None,
                 env: str = None,
                 table_name: str = None,
                 raw_uri: str = None,
                 trusted_uri: str = None,
                 column_incremental: str = None,
                 write_mode: str = None,
                 last_execution: str = None,
                 columns_deduplication: str = None,
                 order_deduplication: str = None,
                 active: bool = None
                 ) -> None:
        self.id = id
        self.status = status
        self.env = env
        self.table_name = table_name
        self.raw_uri = raw_uri
        self.trusted_uri = trusted_uri
        self.column_incremental = column_incremental
        self.write_mode = write_mode
        self.last_execution = last_execution
        self.columns_deduplication = columns_deduplication
        self.order_deduplication = order_deduplication
        self.active = active