from schema.ingestion_object_schema import IngestionObjectSchema

from model.table_raw import TableRaw
from model.table_trusted import TableTrusted
from model.glue_connection import GlueConnection

from repository.table_raw_repository import TableRawRepository
from repository.table_trusted_repository import TableTrustedRepository
from repository.glue_connection_repository import GlueConnectionRepository

from util.inconsistence_exception import InconsistenceException
import util.client as client

from datetime import datetime

class IngestionService:

    def __init__(self) -> None:
        self.tableRawRepository = TableRawRepository()
        self.tableTrustedRepository = TableTrustedRepository()
        self.glueConnectionRepository = GlueConnectionRepository()
        self.glue_client = client.glue_client

    def save(self, objSave: IngestionObjectSchema):

        if objSave.full_table_name is None or len(objSave.full_table_name) < 1:
            raise InconsistenceException("Por favor, informe o campo full_table_name.")
        
        if objSave.connection_id is None or len(objSave.connection_id) < 1:
            raise InconsistenceException("Por favor, informe o campo connection_id.")
        
        if objSave.active is None:
            raise InconsistenceException("Por favor, informe o campo active.")

        if(objSave.id is not None and len(objSave.id) > 0):
            tableRaw = self.tableRawRepository.get_by_id(TableRaw(id=objSave.id))
            tableTrusted = self.tableTrustedRepository.get_by_id(TableTrusted(id=objSave.id))
        else:
            tableRaw = TableRaw(
                id=datetime.now().strftime("%Y%m%d%H%M%S"),
                incremental_template="",
                status="",
                last_execution="1899-12-29 00:00:00")
            tableTrusted = TableTrusted(
                id=tableRaw.id,
                status="",
                last_execution=tableRaw.last_execution)
    
        if (self.tableRawRepository.check_ingestion_exists(
            TableRaw(
                id=tableRaw.id,
                full_table_name=objSave.full_table_name,
                connection_id=objSave.connection_id))
            ):
            raise InconsistenceException(
                f"A tabela {objSave.full_table_name} já foi cadastrada para a esta conexão."
            )
        
        if len(objSave.full_table_name.split(".")) > 1:
            tableRaw.table_name = objSave.full_table_name.split(".")[1]
        else:
            tableRaw.table_name = objSave.full_table_name
        tableTrusted.table_name = tableRaw.table_name

        tableRaw.write_mode = "overwrite"
        tableRaw.column_incremental = ""
        tableRaw.columns_hash = ""
        tableTrusted.columns_deduplication = ""
        tableTrusted.order_deduplication = ""

        if objSave.columns_hash is not None and len(objSave.columns_hash) > 0:
            tableRaw.columns_hash = objSave.columns_hash

        if objSave.column_incremental is not None and len(objSave.column_incremental) > 0:
            tableRaw.write_mode = "append"
            tableRaw.column_incremental = objSave.column_incremental
            if objSave.columns_deduplication is None or len(objSave.columns_deduplication) < 1:
                raise InconsistenceException("É preciso informar o campo columns_deduplication ao preencher o campo column_incremental")
            else:
                tableTrusted.columns_deduplication = objSave.columns_deduplication
                tableTrusted.order_deduplication = "dh_ingestion desc"

        glueConnection = self.glueConnectionRepository.get_by_id(GlueConnection(id=objSave.connection_id))
        
        tableRaw.raw_uri = f"s3://prod-sankhya-data-platform-raw/{glueConnection.connection_name}/{tableRaw.table_name}"
        tableTrusted.raw_uri = tableRaw.raw_uri 
        tableTrusted.trusted_uri = f"s3://prod-sankhya-data-platform-trusted/{glueConnection.connection_name}/{tableTrusted.table_name}"

        tableRaw.connection_id = objSave.connection_id
        tableRaw.env = "prod"
        tableRaw.full_table_name = objSave.full_table_name
        tableRaw.active = objSave.active

        tableTrusted.env = tableRaw.env
        tableTrusted.column_incremental = ""
        tableTrusted.write_mode = "overwrite"
        tableTrusted.active = objSave.active

        self.tableRawRepository.save(tableRaw)
        self.tableTrustedRepository.save(tableTrusted)

        return IngestionObjectSchema(
            id = tableRaw.id,
            connection_id = tableRaw.connection_id,
            full_table_name = tableRaw.full_table_name,
            column_incremental = tableRaw.column_incremental,
            columns_hash = tableRaw.columns_hash,
            columns_deduplication = tableTrusted.columns_deduplication,
            active = tableRaw.active
        )

    def get_by_id(self, obj):

        tableTrusted = self.tableTrustedRepository.get_by_id(TableTrusted(id=obj.id))
        tableRaw = self.tableRawRepository.get_by_id(TableRaw(id=obj.id))
        glueConnection = self.glueConnectionRepository.get_by_id(GlueConnection(id=tableRaw.connection_id))

        return IngestionObjectSchema(
            id = tableRaw.id,
            connection_id = tableRaw.connection_id,
            connection_name=glueConnection.connection_name,
            full_table_name = tableRaw.full_table_name,
            column_incremental = tableRaw.column_incremental,
            columns_hash = tableRaw.columns_hash,
            columns_deduplication = tableTrusted.columns_deduplication,
            active = tableRaw.active
        )

    def get_all(self):

        lst_table_trusted = self.tableTrustedRepository.get_all()
        lst_table_raw = self.tableRawRepository.get_all()
        lst_glue_conn = self.glueConnectionRepository.get_all()

        lst = []
        for tableTrusted in lst_table_trusted:
            tableRaw = list(filter(lambda x: x.id == tableTrusted.id, lst_table_raw))[0]
            glueConnection = list(filter(lambda x: x.id == tableRaw.connection_id, lst_glue_conn))[0]
            lst.append(
                IngestionObjectSchema
                (
                    id = tableRaw.id,
                    connection_id = tableRaw.connection_id,
                    connection_name=glueConnection.connection_name,
                    full_table_name = tableRaw.full_table_name,
                    column_incremental = tableRaw.column_incremental,
                    columns_hash = tableRaw.columns_hash,
                    columns_deduplication = tableTrusted.columns_deduplication,
                    active = tableRaw.active,
                )
            )
        lst.sort(key=lambda x: x.connection_name)
        return lst
    
    def start_process(self, lst):

        if self.is_workflow_processing():
            raise InconsistenceException("O pipeline de ingestão ainda está em execução. Por favor, tente novamente mais tarde.")
        
        if len(lst) < 1:
            raise InconsistenceException("Por favor, informe ao menos uma ingestão para iniciar o processo.")

        lst_raw = self.tableRawRepository.get_all()
        for item in lst:
            raw = list(filter(lambda x: x.id == item.id, lst_raw))[0]
            raw.status = "READY"
            self.tableRawRepository.update(raw)
            
        self.glue_client.start_workflow_run(Name='workflow_job_ingestion')

    def is_workflow_processing(self):
        response = self.glue_client.batch_get_workflows(
            Names=['workflow_job_ingestion'],
            IncludeGraph=False
        )
        return (response.get("Workflows")[0]
                        .get("LastRun")
                        .get("Status") in ["RUNNING", "STOPPING"])
              