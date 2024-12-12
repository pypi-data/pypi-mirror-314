from model.database import Database
from model.table import Table
from model.data_access_request import DataAccessRequest

from repository.policy_repository import PolicyRepository
from repository.data_access_request_repository import DataAccessRequestRepository

import util.client as client

class TableRepository:

    def __init__(self) -> None:
        self.glue_client = client.glue_client
        self.iam_client = client.iam_client
        self.policyRepository = PolicyRepository()
        self.dataAccessRequestRepository = DataAccessRequestRepository()

    def get_by_database_name(self, obj: Database):
        lst_user_data_access_attached = self.policyRepository.get_user_data_access_attached(obj.current_user)
        last_requests = self.dataAccessRequestRepository.get_by_data_user_id_request(
            DataAccessRequest(
                data_user_request=obj.current_user
            )
        )
        response = self.glue_client.get_tables(
            DatabaseName=obj.name
        )
        lst = []
        for item in response["TableList"]:

            arn_table = f"{item["StorageDescriptor"]["Location"].replace("s3://", "arn:aws:s3:::")}*"

            current_user_has_access = False
            if len(list(filter(lambda x: x.upper() == arn_table.upper(), lst_user_data_access_attached))) > 0:
                current_user_has_access = True

            current_user_last_request_status = "NOT_FOUND"
            last_request_id = ""
            if len(last_requests) > 0:
                filtered_by_path = list(filter(lambda x: x.arn_table.upper() == arn_table.upper(), last_requests))
                if len(filtered_by_path) > 0:
                    filtered_by_path.sort(key=lambda x: x.dh_request, reverse=True)
                    current_user_last_request_status = filtered_by_path[0].status
                    last_request_id=filtered_by_path[0].id

            lst.append(
                Table(
                    name=item["Name"],
                    database=Database(name=item["DatabaseName"]),
                    arn_table=arn_table,
                    current_user_has_access=current_user_has_access,
                    current_user_last_request_status=current_user_last_request_status,
                    last_request_id=last_request_id
                )
            )

        return lst