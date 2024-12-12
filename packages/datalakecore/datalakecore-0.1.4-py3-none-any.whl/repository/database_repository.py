from model.database import Database
import util.client as client

class DatabaseRepository:

    def __init__(self) -> None:
        self.glue_client = client.glue_client

    def get_all(self):
        response = self.glue_client.get_databases(
            ResourceShareType='ALL',
            AttributesToGet=['NAME']
        )
        lst = []
        for item in response["DatabaseList"]:
            lst.append(
                Database(
                    name=item["Name"]
                )
            )
        return lst