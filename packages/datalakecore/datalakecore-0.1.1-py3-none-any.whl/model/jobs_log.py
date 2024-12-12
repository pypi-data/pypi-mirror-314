from datetime import datetime

class JobsLog:
    def __init__(self,
                 id: str = None,
                 dt_ref: int = None,
                 job_name: str = None,
                 ingestion_id: str = None,
                 connection_name: str = None,
                 connection_type: str = None,
                 full_table_name: str = None,
                 write_mode: str = None,
                 success: bool = None,
                 rows_affected: int = None,
                 message: str = None,
                 dh_log: datetime = None
                 ) -> None:
        self.id = id
        self.dt_ref = dt_ref
        self.job_name = job_name
        self.ingestion_id = ingestion_id
        self.connection_name = connection_name
        self.connection_type = connection_type
        self.full_table_name = full_table_name
        self.write_mode = write_mode
        self.success = success
        self.rows_affected = rows_affected
        self.message = message
        self.dh_log = dh_log