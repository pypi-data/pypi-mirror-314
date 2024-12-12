from model.jobs_log import JobsLog
from model.table_analytics import TableAnalytics
from model.data_domain_user import DataDomainUser
from model.data_user import DataUser

from repository.table_analytics_repository import TableAnalyticsRepository
from repository.jobs_log_repository import JobsLogRepository
from repository.data_domain_user_repository import DataDomainUserRepository

from util.inconsistence_exception import InconsistenceException
from util.unauthorized_exception import UnauthorizedException

from schema.process_schema import ProcessSchema

import pytz
from datetime import datetime
import boto3
import json
import re
import time

class AnalyticsJobService:
     
    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.tableAnalyticsRepository = TableAnalyticsRepository(dynamodb)
        self.jobsLogRepository = JobsLogRepository(dynamodb)
        self.dataDomainUserRepository = DataDomainUserRepository(dynamodb)
        self.resource_s3 = boto3.resource('s3', region_name="sa-east-1")
        self.sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')
        session = boto3.session.Session()
        self.client_secretsmanager = session.client(
            service_name='secretsmanager',
            region_name="sa-east-1"
        )

    def start_process(self, objEntrada: ProcessSchema = None):
        
        if objEntrada is None:
            lst_tables = self.tableAnalyticsRepository.get_actives()
        else:
            lst_tables = self.tableAnalyticsRepository.get_by_id(objEntrada.transformation_id)
            lst = self.dataDomainUserRepository.get_by_data_user_id(DataDomainUser(data_user_id=objEntrada.data_user_id))
            if len(list(filter(lambda x: (x.data_domain_id == lst_tables[0].data_domain.id), lst))) < 1:
                raise UnauthorizedException("Você não tem permissao para processar esta transformação")

        lst_credentials = []    
        uniqList = {x.data_user.aws_user_name: x for x in lst_tables}.values()
        for item in uniqList:
            aws_access_key_id, aws_secret_access_key = self.__get_keys(item.data_user.aws_user_name)
            lst_credentials.append(
                DataUser(
                    aws_user_name=item.data_user.aws_user_name,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key
                )
            )

        for table in lst_tables:
            try:
                date_now = datetime.now(self.sao_paulo_timezone)
                bucket = self.resource_s3.Bucket('prod-sankhya-data-platform-analytics')
                bucket.objects.filter(Prefix=f"{table.data_domain.domain_name}/{table.name}").delete()
                lf = list(filter(lambda x: x.aws_user_name == table.data_user.aws_user_name, lst_credentials))
                if len(lf) != 1:
                    continue
                client_athena = boto3.client('athena',
                                             aws_access_key_id=lf[0].aws_access_key_id,
                                             aws_secret_access_key=lf[0].aws_secret_access_key,
                                             region_name="sa-east-1")
                sql_athena = f"""
                                UNLOAD ({table.query}) 
                                    TO 's3://prod-sankhya-data-platform-analytics/{table.data_domain.domain_name}/{table.name}' 
                                  WITH (format = 'PARQUET')
                             """
                start_response = client_athena.start_query_execution(
                    QueryString = sql_athena,
                    ResultConfiguration = {"OutputLocation": f"s3://sankhya-athena-files/{table.data_domain.domain_name}"}
                )
                table.last_execution = date_now
                self.tableAnalyticsRepository.update(table)
                self.__write_log(table, True, 0, start_response["QueryExecutionId"], "Execução finalizada com sucesso!")
                time.sleep(1)
            except Exception as ex:
                self.__write_log(table, False, 0, "", f"Erro no processo: {ex.args[0]}")

    def save(self, objSave: TableAnalytics):

        if objSave.active is None:
            raise InconsistenceException("Por favor, informe o campo active.")

        if objSave.id is not None and len(objSave.id) > 0: # alteracao
            if objSave.data_domain is not None and objSave.data_domain.id is not None:
                raise UnauthorizedException("Não é permitida a alteração do domínio. Por favor, não informe o campo data_domain_id.")
            table = self.tableAnalyticsRepository.get_by_id(objSave.id)[0]
            if table.data_user.id != objSave.data_user.id:
                if objSave.query is not None and len(objSave.query) > 0:
                    raise UnauthorizedException("Somente o proprietário desta transformação pode alterar o campo query.")
                if objSave.name is not None and len(objSave.name) > 0:
                    raise UnauthorizedException("Somente o proprietário desta transformação pode alterar o campo name.")
            else:
                if objSave.query is None or len(objSave.query) < 1:
                    raise InconsistenceException("Por favor, informe o campo query.")
                if objSave.name is None or len(objSave.name) < 1:
                    raise InconsistenceException("Por favor, informe o campo name.")
                if not re.search("^[a-zA-Z0-9\-_]*$", objSave.name):
                    raise InconsistenceException("Não utilize caracteres especiais no atributo name! Apenas - e _ são permitidos!")
                table.query = objSave.query
                table.name = objSave.name
        else: #inclusao
            if objSave.query is None or len(objSave.query) < 1:
                raise InconsistenceException("Por favor, informe o campo query.")
            if objSave.name is None or len(objSave.name) < 1:
                raise InconsistenceException("Por favor, informe o campo name.")
            if not re.search("^[a-zA-Z0-9\-_]*$", objSave.name):
                raise InconsistenceException("Não utilize caracteres especiais no atributo name! Apenas - e _ são permitidos!")
            if objSave.data_domain is None or objSave.data_domain.id is None:
                raise InconsistenceException("Por favor, informe o campo data_domain_id.")
            table = TableAnalytics(
                id=datetime.now().strftime("%Y%m%d%H%M%S"),
                data_user = objSave.data_user, # usuário definido na inclusão nao pode ser alterado (owner da transformação.)
                data_domain = objSave.data_domain, # dominio definido na inclusao não pode ser alterado (evita duplicidade por conta das chaves da tabela table_analytics)
                env = "prod",
                query = objSave.query,
                name = objSave.name,
                last_execution = datetime.strptime("1899-12-29 00:00:00", "%Y-%m-%d %H:%M:%S")
            )
            try:
                self.__get_keys(table)
            except:
                raise InconsistenceException("Atenção: Seu usuário não possui chaves de acesso cadastradas. Solicite a criação!")
            
        table.active = objSave.active

        if self.tableAnalyticsRepository.check_exists(table):
            raise InconsistenceException("Antenção! Já existe uma tabela com este nome cadastrada para este domínio.")
        
        self.tableAnalyticsRepository.save(table)

    def get_by_data_domain_user(self, obj: DataDomainUser):
        lst_domains = self.dataDomainUserRepository.get_by_data_user_id(obj)
        lst = self.tableAnalyticsRepository.get_by_domain_id(lst_domains)
        lst.sort(key=lambda x: (x.data_domain.domain_name, x.last_execution), reverse=True)
        return lst
    
    def get_by_id(self, obj: DataDomainUser, id: str):
        lst = self.dataDomainUserRepository.get_by_data_user_id(obj)
        table = self.tableAnalyticsRepository.get_by_id(id)[0]
        if len(list(filter(lambda x: (x.data_domain_id == table.data_domain.id), lst))) < 1:
            raise UnauthorizedException("Você não tem permissao para visualizar esta transformação")
        return table

    def __write_log(self, table, success, rows_affected, query_execution_id, message):
        log = JobsLog(
            id=datetime.now(self.sao_paulo_timezone).strftime("%Y%m%d%H%M%S"),
            dt_ref=int(datetime.now(self.sao_paulo_timezone).strftime("%Y%m%d")),
            job_name="ANALYTICS_JOB",
            ingestion_id=table.id,
            connection_name=query_execution_id,
            connection_type="",
            full_table_name=table.name,
            write_mode="overwrite",
            success=success,
            rows_affected=rows_affected,
            message=message,
            dh_log=datetime.now(self.sao_paulo_timezone)
        )
        self.jobsLogRepository.save(log)

    def __get_keys(self, aws_user_name):
         get_secret_value_response = self.client_secretsmanager.get_secret_value(
            SecretId=aws_user_name
         )
         values = json.loads(get_secret_value_response['SecretString'])
         return values.get("aws_access_key_id"), values.get("aws_secret_access_key")