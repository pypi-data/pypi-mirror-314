from model.jobs_log import JobsLog
from repository.jobs_log_repository import JobsLogRepository

from datetime import datetime
import pytz


class JobsLogService:
    
    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.jobsLogRepository = JobsLogRepository(self.dynamodb)

    def get_ingestion_home_statistics(self):
        sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')

        obj = JobsLog(job_name="RAW_JOB")
        lst_logs = self.jobsLogRepository.get_last_ten_days_ago(obj)

        lst_today = list(filter(lambda x: (x.dt_ref == int(datetime.now(sao_paulo_timezone).strftime("%Y%m%d"))), lst_logs))
        lst_success = list(filter(lambda x: x.success, lst_today))
        total_success_tables = len(lst_success)
        total_error_tables = len(lst_today) - total_success_tables

        distinct_dt = []
        for x in lst_logs:
            if x.dt_ref not in distinct_dt: distinct_dt.append(x.dt_ref)
        distinct_dt.sort()
        
        total_rows_sucess_by_dt = []
        total_tables_success_by_dt = []
        total_tables_error_by_dt = []
        for dt in distinct_dt:

            lst_temp_success = list(filter(lambda x: (x.dt_ref == dt and x.success), lst_logs))
            total = 0
            for success in lst_temp_success:
                total += success.rows_affected

            total_rows_sucess_by_dt.append(total)
            total_tables_success_by_dt.append(len(lst_temp_success))

            lst_temp_error = list(filter(lambda x: (x.dt_ref == dt and x.success == False), lst_logs))
            total_tables_error_by_dt.append(len(lst_temp_error))

        serie_rows_success_by_day = {
            "type": "line",
            "smooth": True,
            "areaStyle": {},
            "data": total_rows_sucess_by_dt
        }
        serie_tables_success_by_day = {
            "type": "bar",
            "smooth": True,
            "areaStyle": {},
            "data": total_tables_success_by_dt
        }
        serie_tables_error_by_day = {
            "type": "bar",
            "smooth": True,
            "areaStyle": {},
            "data": total_tables_error_by_dt
        }  

        lst_date_format = []
        week = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
        for x in distinct_dt:
            xs = str(x)
            dt = datetime(int(xs[0:4]), int(xs[4:6]), int(xs[6:8]), 0, 0, 0)
            lst_date_format.append(week[dt.weekday()])

        return {
            "total_success_tables": total_success_tables,
            "total_error_tables": total_error_tables,
            "xAxis": lst_date_format,
            "serie_rows_success_by_day": serie_rows_success_by_day,
            "serie_tables_success_by_day": serie_tables_success_by_day,
            "serie_tables_error_by_day": serie_tables_error_by_day
        }  

    def get_ingestion_logs_by_dt_ref_and_success(self, obj: JobsLog):

        lst_base = self.jobsLogRepository.get_by_dt_ref_and_success(obj)

        if obj.full_table_name is not None and len(obj.full_table_name) > 0:
            lst_base = list(filter(lambda x: (obj.full_table_name.upper() in x.full_table_name.upper()), lst_base))

        lst_base.sort(key=lambda x: x.dh_log, reverse=True)

        return lst_base

    def get_transformation_home_statistics(self):
        sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')

        obj = JobsLog(job_name="ANALYTICS_JOB")
        lst_logs = self.jobsLogRepository.get_last_ten_days_ago(obj)
        
        lst_today = list(filter(lambda x: (x.dt_ref == int(datetime.now(sao_paulo_timezone).strftime("%Y%m%d"))), lst_logs))
        lst_success = list(filter(lambda x: x.success, lst_today))
        total_success_tables = len(lst_success)
        total_error_tables = len(lst_today) - total_success_tables

        distinct_dt = []
        for x in lst_logs:
            if x.dt_ref not in distinct_dt: distinct_dt.append(x.dt_ref)
        distinct_dt.sort()
        
        total_tables_success_by_dt = []
        total_tables_error_by_dt = []
        for dt in distinct_dt:

            lst_temp_success = list(filter(lambda x: (x.dt_ref == dt and x.success), lst_logs))
            total = 0
            for success in lst_temp_success:
                total += success.rows_affected

            total_tables_success_by_dt.append(len(lst_temp_success))

            lst_temp_error = list(filter(lambda x: (x.dt_ref == dt and x.success == False), lst_logs))
            total_tables_error_by_dt.append(len(lst_temp_error))

        serie_tables_success_by_day = {
            "type": "bar",
            "smooth": True,
            "areaStyle": {},
            "data": total_tables_success_by_dt
        }
        serie_tables_error_by_day = {
            "type": "bar",
            "smooth": True,
            "areaStyle": {},
            "data": total_tables_error_by_dt
        }  

        lst_date_format = []
        week = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
        for x in distinct_dt:
            xs = str(x)
            dt = datetime(int(xs[0:4]), int(xs[4:6]), int(xs[6:8]), 0, 0, 0)
            lst_date_format.append(week[dt.weekday()])

        return {
            "total_success_tables": total_success_tables,
            "total_error_tables": total_error_tables,
            "xAxis": lst_date_format,
            "serie_tables_success_by_day": serie_tables_success_by_day,
            "serie_tables_error_by_day": serie_tables_error_by_day
        }

    def get_transformation_logs_by_dt_ref_and_success(self, obj: JobsLog):

        lst_base = self.jobsLogRepository.get_by_dt_ref(obj)

        lst_base = list(filter(lambda x: x.success == obj.success, lst_base))

        if obj.full_table_name is not None and len(obj.full_table_name) > 0:
            lst_base = list(filter(lambda x: (obj.full_table_name.upper() in x.full_table_name.upper()), lst_base))

        lst_base.sort(key=lambda x: x.dh_log, reverse=True)
        
        return lst_base