from schema.data_user_schema import DataUserSchema

class IngestionObjectSchema:
    def __init__(self,
                 id: str = None,
                 connection_id: str = None,
                 connection_name: str = None,
                 full_table_name: str = None,
                 column_incremental: str = None,
                 columns_hash: str = None,
                 columns_deduplication: str = None,
                 active: bool = None,
                 current_user: DataUserSchema = None,
                 ) -> None:
        self.id = id
        self.connection_id = connection_id
        self.connection_name = connection_name
        self.full_table_name = full_table_name
        self.column_incremental = column_incremental
        self.columns_hash = columns_hash
        self.columns_deduplication = columns_deduplication
        self.active = active
        self.current_user = current_user