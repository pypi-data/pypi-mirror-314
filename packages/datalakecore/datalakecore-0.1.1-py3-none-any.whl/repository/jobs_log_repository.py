from model.jobs_log import JobsLog

from datetime import datetime, timedelta
import pytz
import boto3

class JobsLogRepository:

    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.client_athena = boto3.client('athena', region_name="sa-east-1")

    def save(self, log):
        self.dynamodb.put_item(
            TableName="jobs_log", 
            Item={
                "id": {"S": log.id},
                "dt_ref": {"N": str(log.dt_ref)},
                "job_name": {"S": log.job_name},
                "ingestion_id": {"S": log.ingestion_id},
                "connection_name": {"S": log.connection_name},
                "connection_type": {"S": log.connection_type},
                "full_table_name": {"S": log.full_table_name},
                "write_mode": {"S": log.write_mode},
                "success": {"BOOL": log.success},
                "rows_affected": {"N": str(log.rows_affected)},
                "message": {"S": log.message},
                "dh_log": {"S": log.dh_log.strftime("%Y-%m-%d %H:%M:%S")}
            }
        )

    def get_last_ten_days_ago(self, obj: JobsLog):
        sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')
        resp = self.dynamodb.execute_statement(
           Statement=f"""
                     select * 
                       from jobs_log
                      where job_name=?
                        and dt_ref >= {(datetime.now(sao_paulo_timezone) - timedelta(days=10)).strftime("%Y%m%d")}
                     """,
           Parameters=[
               {"S": obj.job_name}
            ]
        )
        return self.__read(resp)

    def get_by_dt_ref_and_success(self, obj: JobsLog):
        resp = self.dynamodb.execute_statement(
           Statement=f"""
                     select * 
                       from jobs_log
                      where job_name = 'RAW_JOB'
                        and dt_ref=?
                        and success=?
                     """,
           Parameters=[
               {"N": obj.dt_ref},
               {"BOOL": obj.success}
            ]
        )
        return self.__read(resp)


    def get_by_dt_ref(self, obj: JobsLog):
        resp = self.dynamodb.execute_statement(
           Statement=f"""
                     select * 
                       from jobs_log
                      where job_name = 'ANALYTICS_JOB'
                        and dt_ref=?
                     """,
           Parameters=[
               {"N": obj.dt_ref}
            ]
        )
        return self.__read(resp)


    def __read(self, resp):
        lst = []
        for item in resp['Items']:
            success = bool(item["success"]["BOOL"])
            msg = item["message"]["S"]
            if success and item["job_name"]["S"] == "ANALYTICS_JOB":
                response = self.client_athena.get_query_execution(QueryExecutionId=item["connection_name"]["S"])
                if response["QueryExecution"]["Status"]["State"] == "SUCCEEDED":
                    success = True
                    msg = "Execução finalizada com sucesso!"
                else:
                    success = False
                    msg = response["QueryExecution"]["Status"]["StateChangeReason"]
            lst.append(
                JobsLog(
                    id=item["id"]["S"],
                    dt_ref=int(item["dt_ref"]["N"]),
                    job_name=item["job_name"]["S"],
                    ingestion_id=item["ingestion_id"]["S"],
                    connection_name=item["connection_name"]["S"],
                    connection_type=item["connection_type"]["S"],
                    full_table_name=item["full_table_name"]["S"],
                    write_mode=item["write_mode"]["S"],
                    success=success,
                    rows_affected=int(item["rows_affected"]["N"]),
                    message=msg,
                    dh_log=datetime.strptime(item["dh_log"]["S"], "%Y-%m-%d %H:%M:%S") if len(item["dh_log"]["S"]) > 0 else None
                )
            )
        return lst
